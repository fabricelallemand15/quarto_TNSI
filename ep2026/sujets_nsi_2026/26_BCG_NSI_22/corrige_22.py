import ascii

#############################################################################
# Question 1 et 2 : Écrire les codes des fonctions bin2dec et qrcode2dec
#              Proposer un test de qrcode2dec    
#############################################################################

def bin2dec(binaire: tuple) -> int:
    """
    Convertit un tuple de bits en entier décimal.
    
    Paramètres:
        binaire (tuple): Tuple contenant des bits (0 ou 1)
    
    Retour:
        int: Valeur décimale équivalente
    """
    decimal = 0
    # Parcourt chaque bit du tuple
    for i in range(len(binaire)):
        # Multiplie le bit par 2^(position) en partant de la gauche
        # Position = longueur - 1 - indice courant
        decimal += binaire[i] * 2**(len(binaire) - 1 - i)
    return decimal

# Explications : La fonction bin2dec prend un tuple de bits (0 et 1) et calcule sa valeur décimale en utilisant la formule de conversion binaire-décimal. Elle itère sur chaque bit du tuple, multiplie le bit par 2 élevé à la puissance de sa position (en partant de la droite) et ajoute le résultat à la variable decimal.

# Vérification
print("Question 1 : Test de bin2dec")
print(bin2dec((0, 1, 0, 0, 1, 1, 0, 1)))  # 77

# implémentation du QR Code de la figure 1:
qrcode_fig1 = ascii.figure1
# Décodage du QR code de la figure 1
message = ""
for t in qrcode_fig1:
    val = bin2dec(t)
    car = ascii.dict_ascii[val]
    message += car
    print(f"{t} → {val} → '{car}'")
print(f"Message décodé : {message}")
print("L'inventeur du QR code est Masahiro Hara.")

# Question 2 : qrcode2dec

# Version avec liste de compréhension
def qrcode2dec(qrcode):
    """
    Convertit une liste de tuples binaires en liste de valeurs décimales.
    
    Paramètres:
        qrcode: Liste de tuples de bits
    
    Retour:
        list: Liste des valeurs décimales
    """
    return [bin2dec(t) for t in qrcode]

# Version avec boucle for
def qrcode2dec(qrcode):
    """
    Convertit une liste de tuples binaires en liste de valeurs décimales.
    
    Paramètres:
        qrcode: Liste de tuples de bits
    
    Retour:
        list: Liste des valeurs décimales
    """
    liste = []
    for ligne in qrcode:
        liste.append(bin2dec(ligne))
    return liste

# Test de qrcode2dec

print("Question 2 : Test de qrcode2dec")
# Test avec la figure 1
resultat = qrcode2dec(ascii.figure1)
print(f"Liste d'entiers : {resultat}")

# Test de vérification
assert qrcode2dec(ascii.figure1) == [77, 46, 72, 97, 114, 97], "Erreur sur figure1"
print("Test réussi !")

#############################################################################
# Question 3 : Fonctions dec2str et test_dec2str                             
#############################################################################
def dec2str(liste_dec):
    """ entrée: liste d'entiers décimaux
        sortie: chaine de caractère formée des caractères correspondant
        de la table ascii """
    table_ascii = ascii.dict_ascii
    chaine = ""
    for entier in liste_dec:
        chaine += table_ascii[entier]
    return chaine
        
def test_dec2str():
    """ Teste la fonction dec2str avec des données issues du module fourni """
    tests = [ascii.test1, ascii.test2, ascii.test3]
    for test in tests:
        print(dec2str(test))

def qrcode2str(qrcode):
    return dec2str(qrcode2dec(qrcode))

# Test de qrcode2str
print("Question 3 : Test de qrcode2str")
# test_dec2str() # Décommenter pour voir le problème
# Observation du problème :
# test1 → "Test 1 reussi!" ✓
# test2 → "Test 2 reussi!" ✓
# test3 → KeyError: 233 (car 233 n'est pas dans dict_ascii qui va de 0 à 127)
# Le problème : `test3` contient la valeur 233 (correspondant au caractère `é` en encodage ISO-8859-1), qui n'est pas dans la table ASCII (0 à 127). La fonction `dec2str` génère une erreur `KeyError: 233` car cette clé n'existe pas dans `dict_ascii`.

# La correction : avant d'accéder au dictionnaire, on vérifie que l'entier est bien une clé valide. Sinon, on remplace par un caractère de substitution (par exemple `?`).

# Version corrigée de dec2str
def dec2str(liste_dec):
    chaine = ""
    for entier in liste_dec:
        if entier in ascii.dict_ascii:
            chaine += ascii.dict_ascii[entier]
        else:
            chaine += "?"  # Caractère de remplacement
    return chaine

test_dec2str()  # Maintenant, test3 affichera "Test 3 ? reussi!" au lieu de générer une erreur.

#############################################################################
# Question 4 : Fonction str2qrcode déficiente
#############################################################################
# Version initiale de str2qrcode
def str2qrcode(message):
    """
    Convertit une chaine de caractères en liste de tuples binaires.
    """
    qrcode = []
    table_inverse = {valeur: cle for cle, valeur in ascii.dict_ascii.items()}

    for caractere in message:
        entier = table_inverse.get(caractere, 63)
        binaire_str = bin(entier)[2:]
        ligne = tuple(int(bit) for bit in binaire_str)
        qrcode.append(ligne)
        
    return qrcode

# Test de str2qrcode
print("Question 4 : Test de str2qrcode")
message = "M.HARA"
qrcode = str2qrcode(message)
print(f"Message : {message}")
print(f"QR Code : {qrcode}")
# Le problème : `bin(entier)[2:]` ne produit pas de zéros de tête. Par exemple, pour le caractère `.` (code 46), `bin(46)` donne `'0b101110'`, donc `bin(46)[2:]` = `'101110'` → un tuple de 6 bits au lieu de 8.

# La correction : ajouter des zéros inutiles pour garantir que chaque ligne du QR code a 8 bits.

# Version corrigée de str2qrcode
def str2qrcode(message):
    qrcode = []
    table_inverse = {valeur: cle for cle, valeur in ascii.dict_ascii.items()}

    for caractere in message:
        entier = table_inverse.get(caractere, 63)
        binaire_str = bin(entier)[2:]
        # Ajouter des zéros de tête pour garantir 8 bits
        while len(binaire_str) < 8:
            binaire_str = "0" + binaire_str
        ligne = tuple(int(bit) for bit in binaire_str)
        qrcode.append(ligne)
        
    return qrcode

# on vérifie maintenant que le QR code généré pour "M.HARA" correspond à la figure 1
print("Test de str2qrcode après correction")
qrcode = str2qrcode(message)
print(f"Message : {message}")
print(f"QR Code : {qrcode}")
