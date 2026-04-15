#############################################################################
# Question 1 : Mise en évidence du problème des flottants                   #
#############################################################################
# Écrire ci-dessous la fonction calcul_recettes() et son appel
def calcul_recettes():
    '''Calcule les recettes journalières de RESTO NSI.'''
    prix_menu = 2.27 + 5.19 + 1.81  # 9.27 €
    total = 0
    nb_restaurants = 1000
    nb_menus = 500
    for k in range(nb_restaurants * nb_menus):
        total += prix_menu
    return total

print("Question 1")
resultat = calcul_recettes()
print(f"Résultat calculé : {resultat} €")
print(f"Valeur théorique : 4635000 €")
print(f"Différence : {resultat - 4635000} €")

# Explications : La valeur théorique est 9.27 × 500 000 = 4 635 000 €. Mais en virgule flottante, 9.27 n'est pas représenté exactement en binaire. L'addition répétée 500 000 fois accumule les erreurs d'arrondi, produisant un résultat différent de la valeur exacte.

#############################################################################
# Question 2 : Conversion BCD vers Décimal                                  #
#############################################################################
# Écrire ci-dessous la fonction convertir_BCD_vers_decimal(liste_quartets)
# et l'assertion de test demandée

def convertir_BCD_vers_decimal(liste_quartets):
    '''Convertit une liste de quartets BCD en valeur décimale (float).
    Convention : virgule implicite 2 rangs avant la fin.'''
    
    # PARTIE ENTIÈRE : traiter tous les quartets sauf les 2 derniers
    partie_entiere = ""
    for i in range(len(liste_quartets) - 2):
        quartet = liste_quartets[i]
        # Convertir le quartet binaire en chiffre décimal
        # Formule : bit3*8 + bit2*4 + bit1*2 + bit0*1
        chiffre = int(quartet[3]) + int(quartet[2])*2 + int(quartet[1])*2**2 + int(quartet[0])*2**3
        partie_entiere += str(chiffre)
    
    # PARTIE DÉCIMALE : traiter uniquement les 2 derniers quartets
    partie_decimale = ""
    for i in range(len(liste_quartets) - 2, len(liste_quartets)):
        quartet = liste_quartets[i]
        # Convertir le quartet binaire en chiffre décimal (même formule)
        chiffre = int(quartet[3]) + int(quartet[2])*2 + int(quartet[1])*2**2 + int(quartet[0])*2**3
        partie_decimale += str(chiffre)
    
    # Assembler et convertir en float
    # Exemple : "13" + "." + "56" = "13.56" → 13.56
    return float(partie_entiere + "." + partie_decimale)

print("Question 2")
assert convertir_BCD_vers_decimal(['0001', '0011', '0101', '0110']) == 13.56
print("Test OK !")
print(convertir_BCD_vers_decimal(['0101', '1001', '0000', '0000']))  # 59.0
print(convertir_BCD_vers_decimal(['0000', '0010', '0011']))  # 0.23

#############################################################################
# Code fourni pour les questions 3 et 4                                     #
#############################################################################

def convertir_dec_vers_BCD(decimal):
    """
    Convertit une chaîne représentant un décimal vers une liste de quartets BCD.
    Convention : virgule implicite avant les deux derniers quartets.
    """
    ajouter_zero = False
    liste_quartets = []

    if '.' not in decimal:
        decimal = decimal + '.00'

    for i in range(len(decimal)):
        if decimal[i] != '.':
            quartet = bin(int(decimal[i]))[2:].zfill(4)
            liste_quartets.append(quartet)

        # Si le nombre n'a qu'un seul chiffre après la virgule
        if decimal[i] == '.' and i == len(decimal) - 2:
            ajouter_zero = True

    if ajouter_zero:
        liste_quartets.append('0000')

    return liste_quartets


def additionner_binaire_quartets(quartet1, quartet2, retenue):
    """
    Additionne bit à bit deux quartets binaire purs.
    Renvoie un tuple (somme_binaire_str, nouvelle_retenue_int).
    """
    somme = ""
    for i in range(4):
        # Lecture de la droite vers la gauche
        bit1 = int(quartet1[3 - i])
        bit2 = int(quartet2[3 - i])
        total = bit1 + bit2 + retenue

        if total == 0:
            somme = '0' + somme
            retenue = 0
        elif total == 1:
            somme = '1' + somme
            retenue = 0
        elif total == 2:
            somme = '0' + somme
            retenue = 1
        elif total == 3:
            somme = '1' + somme
            retenue = 1

    return somme, retenue


def corriger_BCD(somme, retenue):
    """
    Applique la correction BCD si le quartet dépasse 9 ou génère une retenue.
    Ajoute '0110' (6) au quartet invalide.
    """
    # Si somme >= 10 ('1010' ou '1011' ou '1100' etc.)
    if somme[0] == '1' and (somme[1] == '1' or somme[2] == '1'):
        somme, retenue = additionner_binaire_quartets(somme, '0110', 0)
        return somme, retenue

    # S'il y a eu dépassement naturel lors de l'addition binaire
    if retenue == 1:
        somme, _ = additionner_binaire_quartets(somme, '0110', 0)
        return somme, retenue
        
    return somme, retenue


def aligner_quartets(q1, q2):
    '''Version corrigée : aligne les deux listes en ajoutant des
    '0000' à gauche de la liste la plus courte.'''
    while len(q1) < len(q2):
        q1 = ['0000'] + q1
    while len(q2) < len(q1):
        q2 = ['0000'] + q2
    return q1, q2

##############
# QUESTION 3 #
##############

print("Question 3")

def additionner_nombres_format_BCD(a, b):
    """
    Additionne deux nombres au format BCD, quartet par quartet.
    """
    liste_quartets1 = convertir_dec_vers_BCD(a)
    liste_quartets2 = convertir_dec_vers_BCD(b)

    # Ajustement de la longueur
    liste_quartets1, liste_quartets2 = aligner_quartets(liste_quartets1, liste_quartets2)

    retenue = 0
    resultat = []
    longueur_max = max(len(liste_quartets1), len(liste_quartets2)) 

    for i in range(longueur_max):
        index = longueur_max - i - 1
        
        # Addition binaire simple des quartets
        somme, retenue = additionner_binaire_quartets(liste_quartets1[index], liste_quartets2[index], retenue)

        # LIGNE AJOUTEE : Correction BCD si nécessaire
        somme, retenue = corriger_BCD(somme, retenue)
        
        resultat.insert(0, somme) 

    # Gestion de la dernière retenue éventuelle
    if retenue == 1:
        resultat.insert(0, '0001')
        
    return resultat

print("27 + 35 =", additionner_nombres_format_BCD('27', '35'))

# Explications : Avant la correction, on obtient 27+35=512. L'oubli est l'appel à `corriger_BCD(somme, retenue)` après chaque addition de quartets. Sans cette correction, quand la somme binaire dépasse 9 (par exemple 7+5=12, soit `'1100'` en binaire), le quartet n'est pas un chiffre BCD valide. L'ajout de 6 (`'0110'`) ramène le résultat dans la plage 0-9 et propage la retenue.

##############
# QUESTION 4 #
##############

print("Question 4")

print("23 + 4 =", additionner_nombres_format_BCD('23', '4'))
print("99.99 + 0.01 =", additionner_nombres_format_BCD('99.99', '0.01'))

# Avec la version initiale de la fonction, les résultats sont incorrects, car les listes additionnées n'ont pas la même longueur.
# Sans alignement, les listes `['0010', '0011', '0000', '0000']` (23.00 → 4 quartets) et `['0100', '0000', '0000']` (4.00 → 3 quartets) n'ont pas la même longueur, ce qui provoque une erreur d'indice. La correction ajoute des `'0000'` à gauche du nombre le plus court pour que les deux listes aient la même taille.
# Voir la fonction `aligner_quartets(q1, q2)` corrigée ci-dessus.
