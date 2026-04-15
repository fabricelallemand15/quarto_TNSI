# ------------------------------------
# gestion_eau.py
# Programme de contrôle des réservoirs
# ------------------------------------
from donnees import reservoirs

# Question 1 : écrire la fonction est_en_penurie
def est_en_penurie(reservoirs, nom):
    """
    Vérifie si un réservoir est en pénurie.    
    Cherche un réservoir par son nom dans la liste des réservoirs et détermine
    s'il est en pénurie en comparant son taux de remplissage à 20%.
    
    Args:
        reservoirs (list): Liste de dictionnaires contenant les informations des réservoirs.
                          Chaque réservoir doit avoir les clés "nom", "volume" et "capacite".
        nom (str): Le nom du réservoir à vérifier.
    
    Returns:
        bool: True si le réservoir est trouvé et son taux de remplissage est inférieur à 20%,
              False sinon (réservoir non trouvé ou taux >= 20%).
    """
    # Parcourir chaque réservoir dans la liste des réservoirs
    for r in reservoirs:
        # Vérifier si on a trouvé le réservoir avec le nom recherché
        if r["nom"] == nom:
            # Calculer le taux de remplissage : (volume actuel / capacité totale) * 100
            # Retourner True si le taux est inférieur à 20%, False sinon
            return (r["volume"] / r["capacite"]) * 100 < 20
    # Si aucun réservoir n'a ce nom, retourner False
    return False

print("Question 1 : tests de la fonction est_en_penurie")
print(est_en_penurie(reservoirs, "Motuavai"))  # True (11.1%)
print(est_en_penurie(reservoirs, "Nuiavai"))   # False (55%)
print(est_en_penurie(reservoirs, "Vaihere"))   # False (21%)

# Question 2 : écrire la fonction volume_par_district
def volume_par_district(reservoirs):
    """
    Calcule le volume total d'eau par district à partir d'une liste de réservoirs.
    
    Cette fonction parcourt chaque réservoir et accumule les volumes d'eau
    en les regroupant par district. Elle utilise un dictionnaire pour stocker
    les totaux par district.
    
    Args:
        reservoirs (list): Liste de dictionnaires représentant les réservoirs.
                          Chaque dictionnaire doit contenir au minimum les clés :
                          - "district" (str): Le nom ou l'identifiant du district
                          - "volume" (int ou float): Le volume d'eau du réservoir
    
    Returns:
        dict: Dictionnaire où :
              - Les clés sont les noms des districts
              - Les valeurs sont les volumes totaux cumulés par district
    """
    # Initialiser un dictionnaire vide pour stocker les volumes par district
    volumes = {}
    
    # Parcourir chaque réservoir de la liste
    for r in reservoirs:
        # Extraire le district du réservoir actuel
        district = r["district"]
        
        # Vérifier si c'est la première fois qu'on rencontre ce district
        if district not in volumes:
            # Si oui, initialiser son volume à 0
            volumes[district] = 0
        
        # Ajouter le volume du réservoir actuel au total du district
        volumes[district] += r["volume"]
    
    # Retourner le dictionnaire contenant les volumes cumulés par district
    return volumes

print("Question 2 : tests de la fonction volume_par_district")
print(volume_par_district(reservoirs))

# Question 3

# Version initiale (buguée)
def volume_moyen(reservoirs):
    """
    Renvoie le volume moyen d'eau disponible dans les réservoirs.
    """
    somme_totale = 0
    for r in reservoirs:
        somme_totale += r["volume"]
    moyenne = somme_totale / (len(reservoirs)-1)
    return moyenne

print("Question 3 : tests de la fonction volume_moyen")
# # Tests mettant en évidence le bug
# # Test 1 : un seul réservoir → division par 0 !
# volume_moyen([{"nom": "A", "capacite": 1000, "volume": 500, "district": "X"}])
# print("Test 1 : pas d'erreur")
# # Test 2 : la moyenne ne doit pas dépasser la plus grande capacité
# r = volume_moyen(reservoirs)
# max_cap = max(r["capacite"] for r in reservoirs)
# assert r <= max_cap, f"Moyenne {r} > capacité max {max_cap}"

# # Test 3 : deux réservoirs avec même volume → moyenne = ce volume
# deux = [
#     {"nom": "A", "capacite": 1000, "volume": 500, "district": "X"},
#     {"nom": "B", "capacite": 2000, "volume": 500, "district": "Y"},
# ]
# assert volume_moyen(deux) == 500, f"Attendu 500, obtenu {volume_moyen(deux)}"

# Version corrigée
def volume_moyen(reservoirs):
    somme_totale = 0
    for r in reservoirs:
        somme_totale += r["volume"]
    moyenne = somme_totale / len(reservoirs)  # len() sans -1
    return moyenne

# Test 1 : un seul réservoir → division par 0 !
volume_moyen([{"nom": "A", "capacite": 1000, "volume": 500, "district": "X"}])
print("Test 1 : pas d'erreur")
# Test 2 : la moyenne ne doit pas dépasser la plus grande capacité
r = volume_moyen(reservoirs)
max_cap = max(r["capacite"] for r in reservoirs)
assert r <= max_cap, f"Moyenne {r} > capacité max {max_cap}"

# Test 3 : deux réservoirs avec même volume → moyenne = ce volume
deux = [
    {"nom": "A", "capacite": 1000, "volume": 500, "district": "X"},
    {"nom": "B", "capacite": 2000, "volume": 500, "district": "Y"},
]
assert volume_moyen(deux) == 500, f"Attendu 500, obtenu {volume_moyen(deux)}"

print(f"Volume moyen (corrigé) : {volume_moyen(reservoirs)}")

# Le bug : la division par `len(reservoirs) - 1` au lieu de `len(reservoirs)`. Avec un seul réservoir, cela provoque une division par zéro. Avec plusieurs réservoirs, la moyenne est faussée (trop élevée).


# Question 4

def taux_remplissage(reservoir, changement=0):
    """
    Renvoie le taux de remplissage du réservoir (en pourcentage),
    en tenant compte d'un changement éventuel du volume.
    Attention : le changement n'est pas effectif, il est hypothétique.
    - changement > 0 : ajout d'eau
    - changement < 0 : retrait d'eau
    - changement = 0 (par défaut) : taux de remplissage réel
    """
    volume_modifie = reservoir["volume"] + changement
    capacite = reservoir["capacite"]

    # On évite de dépasser les limites physiques
    if volume_modifie < 0:
        volume_modifie = 0
    if volume_modifie > capacite:
        volume_modifie = capacite

    return volume_modifie * 100 / capacite


def liste_districts(reservoirs):
    """
    Renvoie la liste des districts présents dans les données.
    """
    liste = []
    for r in reservoirs:
        if (r["district"] not in liste):
            liste.append(r["district"])
    return liste


def reservoirs_par_district(reservoirs):
    """
    Renvoie un dictionnaire associant chaque district à la liste
    des réservoirs qui s’y trouvent.
    """
    liste_rpd = {}
    for r in reservoirs:
        district = r["district"]
        if district not in liste_rpd:
            liste_rpd[district] = []
        liste_rpd[district].append(r)
    return liste_rpd

# Question 4
def districts_vulnerables(reservoirs, seuil=0.8):
    """
    Identifie les districts dont le volume moyen d'eau est insuffisant.
    Détermine quels districts sont vulnérables en comparant leur volume moyen
    à un pourcentage du volume moyen global de tous les réservoirs.
    Args:
        reservoirs (list): Liste de dictionnaires représentant les réservoirs,
                           chacun contenant au minimum les clés "district" et "volume".
        seuil (float, optional): Coefficient multiplicateur du volume moyen global
                                 définissant la limite de vulnérabilité. 
                                 Par défaut 0.8 (80%).
    Returns:
        list: Liste des identifiants (noms) des districts vulnérables,
              c'est-à-dire dont le volume moyen est inférieur à 
              seuil * volume_moyen_global.
    """    
    # Étape 1 : Calculer la moyenne globale d'eau sur tous les réservoirs
    moyenne_globale = volume_moyen(reservoirs)
    
    # Étape 2 : Définir le seuil critique
    # Un district est vulnérable si sa moyenne < 80% de la moyenne globale
    limite = seuil * moyenne_globale

    # Étape 3 : Regrouper les réservoirs par district
    # rpd = dictionnaire {district: [réservoirs du district]}
    rpd = reservoirs_par_district(reservoirs)
    
    # Étape 4 : Initialiser la liste des districts vulnérables
    vulnerables = []
    
    # Étape 5 : Parcourir chaque district et sa liste de réservoirs
    for district, liste_res in rpd.items():
        # Calculer le volume moyen pour ce district
        vol_moy = 0
        for r in liste_res:
            vol_moy += r["volume"]
        vol_moy = vol_moy / len(liste_res)
        
        # Vérifier si ce district est en situation de vulnérabilité
        if vol_moy < limite:
            vulnerables.append(district)
    
    # Retourner la liste des districts vulnérables
    return vulnerables

print("Question 4 : tests de la fonction districts_vulnerables")
v = districts_vulnerables(reservoirs)
print(f"Moyenne globale : {volume_moyen(reservoirs)} L")
print(f"Seuil (80%) : {0.8 * volume_moyen(reservoirs)} L")
print(f"Districts vulnérables : {v}")

# Seul Tepua est vulnérable (volume moyen = 30 000 L < 37 600 L).

# Stratégie de gestion possible : redistribuer l'eau depuis les districts excédentaires (Avera, Fare) vers Tepua par camions citernes ou canalisations, en priorité vers les réservoirs les plus vides (Motuavai avec seulement 10 000 L).