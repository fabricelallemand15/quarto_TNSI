import csv

def lire_mouvements_depuis_csv(nom_fichier_csv):
    """
    Lit les données d'un fichier CSV et les retourne en liste de dictionnaires.
    Les colonnes 'montant' et 'mois' sont converties respectivement en flottant et en entier.
    """
    mouvements_csv = []
    try:
        with open(nom_fichier_csv, mode='r', newline='', encoding='utf-8') as fichier_csv:
            lecteur_csv = csv.DictReader(fichier_csv)
            for ligne in lecteur_csv:
                ligne['montant'] = float(ligne['montant'])
                ligne['mois'] = int(ligne['mois'])
                mouvements_csv.append(ligne)
        return mouvements_csv
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier_csv}' est introuvable.")
        return []

mouvements_test = [
    {'type': 'recette', 'catégorie': 'cotisations', 'montant': 1200.0, 'mois': 1},
    {'type': 'recette', 'catégorie': 'billetterie', 'montant': 300.0, 'mois': 6},
    {'type': 'dépense', 'catégorie': 'fonctionnement', 'montant': 450.0, 'mois': 6},
    {'type': 'dépense', 'catégorie': 'déplacements', 'montant': 200.0, 'mois': 12},
    {'type': 'dépense', 'catégorie': 'salaires', 'montant': 1500.0, 'mois': 12},
    {'type': 'recette', 'catégorie': 'subventions', 'montant': 800.0, 'mois': 12}
]

#############################################################################
# Écrire ci-dessous la fonction total_par_type et ses tests (Question 1)    #
#############################################################################
def total_par_type(mouvements, type_mouvement):
    """
    Calcule le total des montants pour un type de mouvement spécifique.
    
    Cette fonction parcourt une liste de mouvements (transactions) et additionne tous les montants correspondant au type de mouvement demandé.
    
    Args:
        mouvements (list): Liste de dictionnaires représentant des mouvements.
                          Chaque dictionnaire doit contenir au minimum les clés:
                          - 'type' (str): le type du mouvement
                          - 'montant' (int ou float): le montant du mouvement
        type_mouvement (str): Le type de mouvement à filtrer et totaliser
    
    Returns:
        int ou float: La somme totale des montants pour le type de mouvement spécifié.
        Retourne 0 si aucun mouvement du type donné n'est trouvé.
    """
    # Initialiser l'accumulateur à 0 pour stocker la somme des montants
    total = 0
    
    # Parcourir chaque mouvement de la liste
    for m in mouvements:
        # Vérifier si le type du mouvement correspond au type recherché
        if m['type'] == type_mouvement:
            # Ajouter le montant au total
            total += m['montant']
    
    # Retourner le total accumulé
    return total

def test_total():
    assert total_par_type(mouvements_test, "recette") == 2300.0
    assert total_par_type(mouvements_test, "dépense") == 2150.0

print("Question 1 : Total par type")
test_total()
print("Tests passés !")

# Recettes = 1200 + 300 + 800 = 2300. Dépenses = 450 + 200 + 1500 = 2150.

#############################################################################
# Fonctions de calcul du solde (Questions 2 et 3)                           #
#############################################################################

def solde_mensuel(mouvements, mois):
    """
    Calcule le solde pour un mois donné (recettes - dépenses).
    """
    total_recettes = 0
    total_depenses = 0

    for m in mouvements:
        if m['mois'] == mois:
            if m['type'] == 'recette':
                total_recettes += m['montant']
            else:
                total_depenses += m['montant']

    return total_recettes - total_depenses


def solde_annuel(mouvements):
    """
    Calcule le solde annuel en additionnant les soldes de chaque mois.
    """
    total = 0
    # Parcourt les mois de l'année pour cumuler le bilan
    # for m in range(1, 12): # ERREUR : la boucle doit parcourir les mois de 1 à 12 (inclus) et non pas de 1 à 11.
    for m in range(1, 13): # CORRECTION
        total = total + solde_mensuel(mouvements, m)

    return total


#############################################################################
# Écrire ci-dessous la fonction test_solde_annuel (Question 2)              #
#############################################################################
# Calcul manuel :
# Mois 1 : recettes 1200, dépenses 0 → solde = 1200
# Mois 6 : recettes 300, dépenses 450 → solde = -150
# Mois 12 : recettes 800, dépenses 1700 → solde = -900
# Total : 1200 - 150 - 900 = 150.0

def test_solde_annuel():
    print(solde_annuel(mouvements_test))
    assert solde_annuel(mouvements_test) == 150.0

print("Questions 2 et 3 : Solde annuel")
test_solde_annuel()
print("Tests passés !")
# ERREUR : la fonction retourne 1050 au lieu de 150.

# CORRECTION : la boucle for de solde_annuel doit parcourir les mois de 1 à 12 (inclus) et non pas de 1 à 11. Il faut donc remplacer la ligne "for m in range(1, 12):" par "for m in range(1, 13):".

# Application sur le fichier complet
mouvements_complets = lire_mouvements_depuis_csv("budget_complet.csv")
print("Le solde annuel sur le fichier complet est de :", solde_annuel(mouvements_complets))
# Résultat : -3423.17 €, le club est en déficit.

#############################################################################
# Programme principal pour analyser le fichier complet                      #
#############################################################################

# mouvements_complets = lire_mouvements_depuis_csv("budget_complet.csv")
# print("Le solde annuel sur le fichier complet est de :", solde_annuel(mouvements_complets))