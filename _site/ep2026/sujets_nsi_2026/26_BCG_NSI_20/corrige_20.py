# Données d'émissions en gCO2e par unité
EMISSIONS = {
    'emails_simples': 4,       # par email
    'emails_pj': 19,           # par email avec pièce jointe
    'streaming_sd': 36,        # par heure
    'streaming_hd': 100,       # par heure
    'recherches': 7,           # par recherche
    'stockage_cloud': 10       # par Go par mois
}

# Exemples d'utilisateurs pour les tests
utilisateur1 = {
    'emails_simples': 150,
    'emails_pj': 20,
    'streaming_sd': 10,
    'streaming_hd': 25,
    'recherches': 500,
    'stockage_cloud': 15
}

utilisateur2 = {
    'streaming_hd': 15,
    'emails_simples': 100,
    'recherches': 10
}

utilisateur3 = {
    'emails_simples': 50,
    'emails_pj': 5,
    'streaming_sd': 30,
    'streaming_hd': 5,
    'recherches': 200,
    'stockage_cloud': 5
}

utilisateur4 = {
    'emails_simples': 100,
    'recherches': 50
}

utilisateur5 = {
    'emails_simples': 50,
    'recherches': 100
}

utilisateur6 = {}

#############################################################################
# Écrire le code de la fonction calculer_empreinte de la question 1         #
#############################################################################
def calculer_empreinte(utilisateur):
    """
    Calcule l'empreinte carbone totale d'un utilisateur en fonction de ses activités.
    
    Args:
        utilisateur (dict): Un dictionnaire où les clés sont des noms d'activités et les valeurs sont les quantités/fréquences de ces activités.
    
    Returns:
        int: L'empreinte carbone totale de l'utilisateur, arrondie à l'entier inférieur.
    """
    total = 0  # Initialise l'accumulation des émissions à 0
    for activite in utilisateur:  # Parcourt chaque activité de l'utilisateur
        # Accumule : quantité de l'activité × émission par unité
        total += utilisateur[activite] * EMISSIONS[activite]
    return int(total)  # Retourne le total arrondi à l'entier inférieur

print("Question 1 :")
print(calculer_empreinte(utilisateur1))  # 7490
print(calculer_empreinte(utilisateur2))  # 1970

# 150×4 + 20×19 + 10×36 + 25×100 + 500×7 + 15×10 = 600 + 380 + 360 + 2500 + 3500 + 150 = **7490**.


#############################################################################
# Écrire le code de la fonction classer_par_impact de la question 2         #
#############################################################################
def classer_par_impact(utilisateur):
    """
    Classe les activités d'un utilisateur par catégorie d'impact carbone.
    
    Args:
        utilisateur (dict): Dictionnaire avec activités et leurs quantités/fréquences.
    
    Returns:
        dict: Dictionnaire avec trois clés ('fort', 'moyen', 'faible') 
              contenant les listes d'activités par catégorie d'impact.
    """
    classement = {'fort': [], 'moyen': [], 'faible': []}  # Initialise les trois catégories
    
    for activite in utilisateur:  # Parcourt chaque activité de l'utilisateur
        # Calcule l'émission totale pour cette activité
        emission = utilisateur[activite] * EMISSIONS[activite]
        
        # Classe dans la catégorie appropriée selon le seuil d'émission
        if emission >= 1000:
            classement['fort'].append(activite)
        elif emission >= 200:
            classement['moyen'].append(activite)
        else:
            classement['faible'].append(activite)
    
    return classement  # Retourne le dictionnaire des activités classées

print("Question 2 :")
print(classer_par_impact(utilisateur2))
print(classer_par_impact(utilisateur1))

#############################################################################
# Fonction fournie pour la question 3                                       #
#############################################################################

def comparer(u1, u2):
    """Compare les émissions de deux utilisateurs pour toutes les activités.
    Renvoie un dictionnaire avec, pour chaque activité, la différence des
    émissions (émissions de l’utilisateur 2 moins celles de l’utilisateur 1).
    Si une activité est absente chez un utilisateur, on considère que
    son émission vaut 0."""
    differences = {}
    for activite in EMISSIONS:
        quantite1 = 0
        quantite2 = 0
        if activite in u1:
            quantite1 = u1[activite]
        if activite in u2:
            quantite2 = u2[activite]
        emission1 = quantite1 * EMISSIONS[activite]
        emission2 = quantite2 * EMISSIONS[activite]
        differences[activite] = emission2 - emission1
    return differences

def test_comparer():
    diff = comparer(utilisateur4, utilisateur5)
    assert diff['emails_simples'] == -200  # (50-100) * 4
    assert diff['recherches'] == 350     # (100-50) * 7

    # Test 1 : activité absente chez u2 → émission considérée comme 0
    # Important pour vérifier le cas où un utilisateur n'a pas une activité
    diff2 = comparer(utilisateur1, utilisateur2)
    assert diff2['emails_pj'] == -380  # 0 - 20*19 = -380

    # Test 2 : utilisateur vide → toutes les différences sont négatives ou nulles
    # Important pour vérifier le cas limite d'un utilisateur sans aucun usage
    diff3 = comparer(utilisateur1, utilisateur6)
    assert diff3['streaming_hd'] == -2500  # 0 - 25*100

    # Test 3 : deux utilisateurs identiques → différences toutes nulles
    diff4 = comparer(utilisateur1, utilisateur1)
    for activite in diff4:
        assert diff4[activite] == 0

print("Question 3 :")
test_comparer()
print("Tests passés !")


#############################################################################
# Fonction fournie pour la question 4                                       #
#############################################################################
# Fonction initiale à corriger pour la question 4
def comparer_v2(u1, u2):
    """Compare les émissions de deux utilisateurs pour toutes les activités.
    Renvoie un dictionnaire avec, pour chaque activité, l'écart des émissions
    sous forme de pourcentage, en proportion de la première émission."""
    ecarts = {}
    for activite in EMISSIONS:
        quantite1 = 0
        quantite2 = 0
        if activite in u1:
            quantite1 = u1[activite]
        if activite in u2:
            quantite2 = u2[activite]
        emission1 = quantite1 * EMISSIONS[activite]
        emission2 = quantite2 * EMISSIONS[activite]
        ecarts[activite] = (emission2 - emission1)/emission1 * 100
    return ecarts

# L'erreur se produit quand emission1 = 0 (activité absente chez u1)
# → division par zéro dans (emission2 - emission1) / emission1
# Correction : vérifier que `emission1 != 0` avant la division. Si les deux sont à 0, l'écart est 0. Si seule `emission1` est à 0, l'écart n'est pas calculable (on peut renvoyer `None`).

# Version corrigée de comparer_v2
def comparer_v2(u1, u2):
    """Compare les émissions de deux utilisateurs pour toutes les activités.
    Renvoie un dictionnaire avec, pour chaque activité, l'écart des émissions
    sous forme de pourcentage, en proportion de la première émission."""
    ecarts = {}
    for activite in EMISSIONS:
        quantite1 = 0
        quantite2 = 0
        if activite in u1:
            quantite1 = u1[activite]
        if activite in u2:
            quantite2 = u2[activite]
        emission1 = quantite1 * EMISSIONS[activite]
        emission2 = quantite2 * EMISSIONS[activite]
        
        if emission1 == 0:
            if emission2 == 0:
                ecarts[activite] = 0  # Pas d'émission chez les deux → écart de 0%
            else:
                ecarts[activite] = None  # Écart non calculable (division par zéro)
        else:
            ecarts[activite] = (emission2 - emission1) / emission1 * 100
    
    return ecarts