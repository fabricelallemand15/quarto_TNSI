#############################################################################
# Jeux de données fournis                                                   #
#############################################################################
from plantes import plantes, Plante
from mesures import mesures

#############################################################################
# Écrire le code de la fonction croissance_moyenne de la question 1         #
#############################################################################
def croissance_moyenne(plantes: list) -> float:
    '''Renvoie la moyenne des durées de croissance des plantes.
    Si la liste est vide, renvoie None.'''
    # Vérifier si la liste est vide pour éviter une division par zéro
    if len(plantes) == 0:
        return None
    
    # Initialiser l'accumulateur pour la somme des durées de croissance
    total_croissance = 0
    
    # Parcourir chaque plante et ajouter sa durée de croissance au total
    for plante in plantes:
        total_croissance += plante.croissance
    
    # Calculer et retourner la moyenne en divisant par le nombre de plantes
    return total_croissance / len(plantes)

# Tests
assert croissance_moyenne([]) is None
assert croissance_moyenne(plantes) == (60 + 80 + 80 + 85 + 90) / 5
print("Tous les tests passent !")
print("Moyenne :", croissance_moyenne(plantes), "jours")

#############################################################################
# Écrire le code de la fonction dictionnaire_mesure de la question 2      #
#############################################################################
def dictionnaire_mesure(plantes: list, mesures: list) -> dict:
    '''Renvoie un dictionnaire associant chaque nom de plante
    à la liste de ses mesures.'''
    # Initialiser un dictionnaire vide pour stocker les mesures par plante
    dico = {}
    
    # Étape 1 : Créer une clé pour chaque plante avec une liste vide initiale
    # Cela garantit que toutes les plantes auront une entrée, même sans mesure
    for p in plantes:
        dico[p.nom] = []
    
    # Étape 2 : Parcourir toutes les mesures et les associer à leur plante
    for m in mesures:
        # Vérifier que la plante de la mesure existe dans notre dictionnaire
        if m['plante'] in dico:
            # Ajouter la mesure à la liste correspondant à la plante
            dico[m['plante']].append(m)
    
    # Retourner le dictionnaire complété
    return dico


# Tests
d = dictionnaire_mesure(plantes, mesures)
for nom, mes in d.items():
    print(f"{nom}: {len(mes)} mesures")

# Test avec plante sans mesure
p_fictive = Plante("Orchidée", "Orchidaceae", 90, 30, "ombre")
d2 = dictionnaire_mesure(plantes + [p_fictive], mesures)
assert d2["Orchidée"] == []
print("Test plante sans mesure OK")

#############################################################################
# Fonction défaillante à analyser et corriger pour les questions 3 et 4     #
#############################################################################

def purger_mesures_extremes(liste_mesures):
    """
    Supprime de la liste toutes les mesures dont la température 
    n'est pas comprise entre 20 et 25°C inclus.
    """
    for mesure in liste_mesures:
        if mesure['temperature'] < 20 or mesure['temperature'] > 25:
            liste_mesures.remove(mesure)
    return liste_mesures

def test_purger():
    mesures_test = [
         {'jour': 1, 'plante': 'Basilic', 'temperature': 18.0},
         {'jour': 2, 'plante': 'Basilic', 'temperature': 19.0},
         {'jour': 3, 'plante': 'Basilic', 'temperature': 22.0},
         {'jour': 4, 'plante': 'Basilic', 'temperature': 28.0},
         {'jour': 5, 'plante': 'Basilic', 'temperature': 29.0}
    ]

    purger_mesures_extremes(mesures_test)

    print("Résultat après la purge :")
    for m in mesures_test:
        print(f"Jour {m['jour']} : {m['temperature']}°C")

##############
# QUESTION 3 #
##############
test_purger()

# Bug : La fonction purger_mesures_extremes ne supprime pas correctement les mesures extrêmes. On observe un résultat égal à 29°C, alors que seules les mesures entre 20 et 25°C devraient être conservées.
# Explications : Le bug vient de la suppression d'éléments pendant l'itération sur la liste. Quand on supprime un élément avec remove(mesure), les indices des éléments suivants sont décalés. L'itérateur passe alors au suivant en sautant un élément, qui n'est donc jamais vérifié. Par exemple, après la suppression de la mesure à 18°C (indice 0), la mesure à 19°C passe à l'indice 0, mais l'itérateur passe à l'indice 1 (22°C), et la mesure à 19°C n'est jamais testée.

##############
# QUESTION 4 #
##############

# Correction : Pour corriger ce bug, il faut éviter de modifier la liste pendant l'itération. On peut créer une nouvelle liste pour stocker les mesures valides, ou utiliser une compréhension de liste pour filtrer les mesures.

# Version avec une nouvelle liste
def purger_mesures_extremes(liste_mesures):
    '''Version corrigée : ne conserve que les mesures
    dont la température est comprise entre 20 et 25°C inclus.'''
    # Créer une nouvelle liste vide pour stocker les mesures valides
    # (au lieu de modifier la liste pendant l'itération)
    mesures_valides = []
    
    # Parcourir chaque mesure de la liste originale
    for m in liste_mesures:
        # Vérifier si la température est dans l'intervalle [20, 25]
        if 20 <= m['temperature'] <= 25:
            # Si oui, ajouter la mesure à la nouvelle liste
            mesures_valides.append(m)
    
    # Retourner uniquement les mesures valides
    # La liste originale n'est pas modifiée
    return mesures_valides

# Version avec liste en compréhension
def purger_mesures_extremes(liste_mesures):
    '''Version corrigée : ne conserve que les mesures
    dont la température est comprise entre 20 et 25°C inclus.'''
    return [m for m in liste_mesures if 20 <= m['temperature'] <= 25]


# Tests
test = [
    {'jour': 1, 'plante': 'Basilic', 'temperature': 18},
    {'jour': 2, 'plante': 'Basilic', 'temperature': 19},
    {'jour': 3, 'plante': 'Basilic', 'temperature': 22},
    {'jour': 4, 'plante': 'Basilic', 'temperature': 28},
    {'jour': 5, 'plante': 'Basilic', 'temperature': 29}
]
resultat = purger_mesures_extremes(test)
print("Températures restantes :", [m['temperature'] for m in resultat])