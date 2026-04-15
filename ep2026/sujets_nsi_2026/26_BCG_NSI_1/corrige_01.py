from PIL import Image

##############
# QUESTION 1 #
##############

"""
Non, la liste obtenue par codage RLE n'est pas forcément de longueur inférieure ou égale à la liste de départ.

Contre-exemple : La liste `[1, 2, 3]` (longueur 3) donne le codage RLE `[1, 1, 1, 2, 1, 3]` (longueur 6), car chaque valeur n'apparaît qu'une seule fois.

En effet, dans le pire des cas (aucune valeur consécutive identique), la liste RLE est de longueur double par rapport à la liste d'origine, puisque chaque valeur isolée génère un couple (1, valeur).

Le codage RLE n'est avantageux que lorsque l'image contient de longues plages de pixels identiques.
"""


def codage_rle(liste_octets):
    '''Renvoie une liste d'octets obtenue par compression RLE'''
    liste_rle = []
    i = 0
    while i < len(liste_octets):
        c = liste_octets[i]
        k = 1
        while i+k < len(liste_octets) and liste_octets[i+k] == c:
            k += 1
        liste_rle.append(k)
        liste_rle.append(c)
        i += k
    return liste_rle

##############
# QUESTION 2 #
##############

def decodage_rle(liste_rle):
    '''Renvoie la liste d'octets obtenue à partir de la liste liste_rle obtenue
    par compression RLE'''
    # Initialiser la liste vide qui contiendra le résultat du décodage
    retour = []
    # Initialiser l'indice de parcours de la liste RLE
    indice = 0
    # Parcourir la liste RLE par paires (nombre, valeur)
    while indice < len(liste_rle):
        # Lire le nombre de répétitions (à l'indice courant)
        nombre = liste_rle[indice]
        # Lire la valeur à répéter (à l'indice suivant)
        valeur = liste_rle[indice + 1]
        # Ajouter à retour 'nombre' copies de 'valeur'
        retour = retour + [valeur]*nombre
        # Avancer de 2 positions pour lire la paire suivante
        indice = indice + 2
    # Retourner la liste décodée complète
    return retour
        
"""
La liste RLE se lit par paires : l'élément d'indice pair est le nombre de répétitions `k`, l'élément d'indice impair suivant est la valeur `c`. On ajoute `k` fois la valeur `c` à la liste résultat, puis on avance de 2 dans la liste RLE.
"""

def test_codage():
    assert codage_rle([255, 255, 0, 255, 255, 255]) == [2, 255, 1, 0, 3, 255]
    assert decodage_rle([2, 255, 1, 0, 3, 255]) == [255, 255, 0, 255, 255, 255]


def enregistrer_octets(nom_fichier, liste_octets):
    '''Enregistre une liste de valeurs numériques entre 0 et 255 dans un
    le fichier nom_fichier. Si une valeur est plus grande que 255 on considère
    que c'est 255. De même pour les valeur plus petite que 0.'''
    # Le fichier est ouvert en mode binaire pour pouvoir écrire sans restriction toute valeur
    # entre 0 et 255
    with open(nom_fichier, 'wb') as fichier:
        # Pour convertir une liste de valeur entre 0 et 255 en une liste d'octets qui peuvent
        # être écrits dans le fichier, on utilise `bytes`
        fichier.write(bytes([max(0, min(255, b)) for b in liste_octets]))


def charger_octets(nom_fichier):
    '''Renvoie la liste des octets présents dans le fichier nom_fichier'''
    with open(nom_fichier, 'rb') as fichier:
        liste_octets = list(fichier.read())
        return liste_octets


def enregistrer_image(nom_image, largeur, liste_niveaux):
    '''Enregistre un fichier image nom_image de la largeur donnée et dont les 
    valeurs de niveaux de gris des pixels sont celles de la liste
    liste_niveaux'''
    hauteur = len(liste_niveaux) // largeur
    im = Image.frombytes('L', (largeur, hauteur), bytes(liste_niveaux))
    im.save(nom_image)


def charger_image(nom_image):
    '''Étant donné une image nom_image, renvoie un couple (largeur, liste_niveaux) où 
    largeur est la largeur de l'image et liste_niveaux est la liste des valeurs de niveaux 
    de gris de l'image ligne par ligne'''

    image = Image.open(nom_image).convert('L')
    return (image.width, list(image.tobytes()))

#############################################################################
# Fonction nécessaire pour les tests de la question 3                       #
#############################################################################


def encoder_decoder_image(nom_image):
    '''Fonction de test permettant d'encoder puis décoder une image avec un
    codage RLE. Le fichier rle est nommé nom_image.rle et le fichier decodé
    est nom_image.dec.png'''
    w, l = charger_image(nom_image)
    enregistrer_octets(nom_image+'.rle', codage_rle(l))
    l = charger_octets(nom_image+'.rle')
    enregistrer_image(nom_image+'.dec.png', w, decodage_rle(l))

##############
# QUESTION 3 #
##############

"""
Avec l'image `bac_nsi_32.png` (petite image, 32 pixels de large), le codage/décodage fonctionne correctement : l'image reconstruite est identique à l'originale.

Avec l'image `bac_nsi_256.png` (plus grande image, 256 pixels de large), l'image reconstruite est déformée ou corrompue.
"""

##############
# QUESTION 4 #
##############

"""
L'idée est de découper les plages de plus de 255 pixels identiques en plusieurs couples successifs `(255, valeur)`, suivis d'un dernier couple avec le reste. La fonction de décodage reste identique car elle additionne naturellement les répétitions de la même valeur.
"""

def codage_rle_v2(liste_octets):
    '''Codage RLE gérant les plages de plus de 255 pixels identiques'''
    # Initialiser la liste qui contiendra le résultat compressé
    liste_rle = []
    # Indice pour parcourir la liste d'octets d'origine
    i = 0
    
    # Parcourir toute la liste d'octets
    while i < len(liste_octets):
        # Récupérer la valeur actuelle
        c = liste_octets[i]
        # Compter combien de fois cette valeur se répète consécutivement
        k = 1
        while i+k < len(liste_octets) and liste_octets[i+k] == c:
            k += 1
        
        # Gérer les plages de plus de 255 pixels identiques
        # Diviser en groupes de 255 pour respecter la limite d'un octet
        for j in range(k//255):
            # Ajouter un couple (255, valeur) pour chaque groupe complet
            liste_rle.append(255)
            liste_rle.append(c)
        
        # Ajouter le reste de la plage (< 255)
        # k%255 donne le nombre de pixels restants après les groupes complets
        liste_rle.append(k % 255)
        liste_rle.append(c)
        
        # Avancer dans la liste d'origine au-delà de la plage traitée
        i += k
    
    return liste_rle


# Tests
test = [42] * 300 + [7] * 10
encoded = codage_rle_v2(test)
assert decodage_rle(encoded) == test
print("Test avec 300 pixels identiques : OK !")