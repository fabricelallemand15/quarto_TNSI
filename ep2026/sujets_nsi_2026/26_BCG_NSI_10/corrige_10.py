donnees = [
    {"jour": "2025-02-04", "heure": "00:00", "chaude": 2, "froide": 3},
    {"jour": "2025-02-04", "heure": "01:00", "chaude": 1, "froide": 2},
    {"jour": "2025-02-04", "heure": "02:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-04", "heure": "03:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-04", "heure": "04:00", "chaude": 0, "froide": 1},
    {"jour": "2025-02-04", "heure": "05:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-04", "heure": "06:00", "chaude": 4, "froide": 6},
    {"jour": "2025-02-04", "heure": "07:00", "chaude": 6, "froide": 8},
    {"jour": "2025-02-05", "heure": "00:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-05", "heure": "01:00", "chaude": 1, "froide": 1},
    {"jour": "2025-02-05", "heure": "02:00", "chaude": 1, "froide": 1},
    {"jour": "2025-02-05", "heure": "03:00", "chaude": 1, "froide": 1},
    {"jour": "2025-02-05", "heure": "04:00", "chaude": 0, "froide": 0},
    {"jour": "2025-02-05", "heure": "05:00", "chaude": 0, "froide": 0},
]


# -----------------------------
# Fonctions à compléter
# -----------------------------

##############
# Question 1 #
##############
def total_conso(donnees, jour):
    """
    Calcule la consommation totale d'eau (chaude + froide) pour un jour donné.
    
    Args:
        donnees: liste de dictionnaires contenant les mesures
        jour: chaîne de caractères au format "YYYY-MM-DD"
    
    Returns:
        int: total de la consommation, ou None si aucune mesure pour ce jour
    """
    total = 0  # Accumulateur pour la consommation totale
    trouve = False  # Drapeau pour vérifier si on a trouvé des données pour ce jour
    
    # Parcourir chaque enregistrement de mesure
    for d in donnees:
        # Si la mesure correspond au jour recherché
        if d["jour"] == jour:
            # Ajouter la consommation d'eau chaude et froide
            total += d["chaude"] + d["froide"]
            # Marquer qu'on a trouvé au moins une mesure
            trouve = True
    
    # Retourner le total si on a trouvé des données, sinon None
    if trouve:
        return total
    return None

print('Tests question 1')
print(total_conso(donnees, "2025-02-04"))  # 33
print(total_conso(donnees, "2025-02-05"))  # 6
print(total_conso(donnees, "2025-12-25"))  # None

##############
# Question 2 #
##############
def fuite_possible(donnees, jour):
    """
    Détecte une fuite d'eau possible en cherchant au moins 3 mesures 
    consécutives avec consommation non nulle entre 00:00 et 05:00.
    
    Args:
        donnees: liste de dictionnaires contenant les mesures
        jour: chaîne de caractères au format "YYYY-MM-DD"
    
    Returns:
        bool: True si fuite détectée, False sinon
    """
    # Compteur pour les mesures consécutives non nulles
    compteur = 0
    
    # Parcourir chaque enregistrement de mesure
    for d in donnees:
        # Filtrer : jour recherché ET horaire entre 00:00 et 05:00
        if d["jour"] == jour and d["heure"] <= "05:00":
            # Calculer la consommation totale (chaude + froide)
            consommation = d["chaude"] + d["froide"]
            
            # Si consommation détectée
            if consommation > 0:
                # Incrémenter le compteur de mesures consécutives
                compteur += 1
                # Si 3 mesures consécutives non nulles : fuite détectée !
                if compteur >= 3:
                    return True
            else:
                # Réinitialiser le compteur (perte de consécutivité)
                compteur = 0
    
    # Aucune fuite détectée
    return False

print('Tests question 2')
print(fuite_possible(donnees, "2025-02-04"))  # False
print(fuite_possible(donnees, "2025-02-05"))  # True

##############
# Question 3 #
##############
# -----------------------------
# Fonction fournie (erronée)
# -----------------------------

def lissage_conso(valeurs):
    """
    Calcule une moyenne glissante sur les valeurs.
    Pour chaque valeur, on calcule la moyenne avec ses voisins.
    """
    
    lisse = []
    for i in range(len(valeurs)):
        if i == 0:
            m = (valeurs[i] + valeurs[i+1]) / 2
        elif i == len(valeurs)-1:
            m = (valeurs[i-1] + valeurs[i]) / 2
        else:
            m = (valeurs[i-1] + valeurs[i] + valeurs[i+1]) / 2
        lisse.append(m)
    
    return lisse

print('Tests question 3 (version buguée)')
print(lissage_conso([10, 20, 30, 40, 50]))

# Explications : Le bug est la division par 2 au lieu de 3 pour les éléments intermédiaires. On fait la moyenne de 3 valeurs (précédent + courant + suivant), il faut donc diviser par 3. Par exemple, pour l'indice 1 : (10 + 20 + 30) / 3 = 20.0, alors que la version buguée donnait (10 + 20 + 30) / 2 = 30.0.

# Version corrigée : 

def lissage_conso(valeurs):
    """Version corrigée du lissage par moyenne glissante."""
    lisse = []
    for i in range(len(valeurs)):
        if i == 0:
            m = (valeurs[i] + valeurs[i+1]) / 2
        elif i == len(valeurs) - 1:
            m = (valeurs[i-1] + valeurs[i]) / 2
        else:
            m = (valeurs[i-1] + valeurs[i] + valeurs[i+1]) / 3  # Corrigé : /3
        lisse.append(m)
    return lisse

print('Tests question 3 (version corrigée)')
print(lissage_conso([10, 20, 30, 40, 50]))  # [15.0, 20.0, 30.0, 40.0, 45.0]
print(lissage_conso([5, 15]))  # [10.0, 10.0]

##############
# Question 4 #
##############
# Cas limite non géré : la liste ne contient qu'un seul élément (ou est vide).

# - Si la liste est vide (`len(valeurs) == 0`), la boucle ne s'exécute pas mais le cas `len(valeurs) == 2` n'est pas vérifié, donc la fonction renvoie une liste vide (pas d'erreur mais pas traité explicitement).
# - Si la liste contient un seul élément (`len(valeurs) == 1`), la boucle essaie d'accéder à `valeurs[i+1]` alors que `i == 0` est aussi `len(valeurs) - 1` : le premier `if` est exécuté et provoque une erreur `IndexError`.

# Correction proposée : ajouter un test au début de la fonction :

# def lissage_conso(valeurs):
#     if len(valeurs) <= 1:
#         return list(valeurs)  # copie de la liste
#     if len(valeurs) == 2:
#         m = (valeurs[0] + valeurs[1]) / 2
#         return [m, m]
#     # ... suite inchangée

