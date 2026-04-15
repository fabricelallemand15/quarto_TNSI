# =================================================================================#
# Données de test
donnees_test = [
    # Société - Données sur 2010 et 2020
    {'date': '2010-01-15', 'zone': 'Societe', 'temperature': 27.0},
    {'date': '2010-06-20', 'zone': 'Societe', 'temperature': 26.5},
    {'date': '2011-03-10', 'zone': 'Societe', 'temperature': 27.5},
    {'date': '2020-02-14', 'zone': 'Societe', 'temperature': 28.0},
    {'date': '2020-08-22', 'zone': 'Societe', 'temperature': 28.5},
    {'date': '2021-05-30', 'zone': 'Societe', 'temperature': 29.0},

    # Tuamotu - Données sur 2010 et 2020
    {'date': '2015-04-10', 'zone': 'Tuamotu', 'temperature': 26.8},
    {'date': '2020-07-15', 'zone': 'Tuamotu', 'temperature': 27.5},
    {'date': '2021-09-20', 'zone': 'Tuamotu', 'temperature': 28.0},

    # Marquises - Données uniquement sur 2020
    {'date': '2020-03-15', 'zone': 'Marquises', 'temperature': 25.5},
    {'date': '2021-07-10', 'zone': 'Marquises', 'temperature': 26.0},
    {'date': '2022-11-25', 'zone': 'Marquises', 'temperature': 26.5},
]

# =================================================================================#
#  Question 1 : Ecrire le code de votre fonction température_moyenne
def temperature_moyenne(zone, donnees):
    """
    Calcule la température moyenne pour une zone donnée.
    Cette fonction parcourt une liste de relevés de température et calcule
    la moyenne des températures enregistrées dans la zone spécifiée.
    
    Args:
        zone (str): L'identifiant de la zone pour laquelle calculer la moyenne.
        donnees (list): Une liste de dictionnaires contenant les relevés.
                       Chaque dictionnaire doit avoir les clés 'zone' et 'temperature'.
    
    Returns:
        float: La température moyenne de la zone (somme / nombre de relevés).
        None: Si aucun relevé n'existe pour la zone donnée.
    """
    # Initialiser les variables pour accumuler les valeurs
    somme = 0          # Accumule la somme des températures
    compteur = 0       # Compte le nombre de relevés pour la zone

    # Parcourir tous les relevés de température
    for releve in donnees:
        # Vérifier si le relevé appartient à la zone recherchée
        if releve['zone'] == zone:
            # Ajouter la température à la somme
            somme += releve['temperature']
            # Incrémenter le compteur
            compteur += 1
    
    # Gérer le cas où aucun relevé n'existe pour la zone
    if compteur == 0:
        return None
    
    # Calculer et retourner la moyenne (somme / nombre de relevés)
    return somme / compteur

print("Question 1 : Tests de la fonction temperature_moyenne")
# on utilise les données de test pour vérifier le fonctionnement de la fonction
print(temperature_moyenne('Societe', donnees_test))    # 27.75
print(temperature_moyenne('Australes', donnees_test))   # None

# =================================================================================#
#  Question 2 : Ecrire le code de votre fonction detection_anomalies
def detecter_anomalies(zone, seuil, donnees):
    """
    Détecte les relevés de température anormaux pour une zone donnée.
    Un relevé est considéré comme anormal si son écart à la moyenne dépasse le seuil.
    
    Args:
        zone (str): L'identifiant de la zone à analyser.
        seuil (float): L'écart maximum acceptable par rapport à la moyenne.
        donnees (list): Liste des relevés de température.
    
    Returns:
        list: Liste des dates des relevés anormaux, ou liste vide si aucune anomalie.
    """
    # Étape 1 : Calculer la température moyenne de la zone
    moyenne = temperature_moyenne(zone, donnees)
    
    # Étape 2 : Vérifier si la zone existe (si moyenne est None, zone inexistante)
    if moyenne is None:
        return []
    
    # Étape 3 : Initialiser la liste pour stocker les dates des anomalies
    anomalies = []
    
    # Étape 4 : Parcourir tous les relevés
    for releve in donnees:
        # Filtrer uniquement les relevés de la zone recherchée
        if releve['zone'] == zone:
            # Calculer l'écart absolu entre la température et la moyenne
            # abs() donne la valeur absolue pour comparer sans tenir compte du signe
            ecart = abs(releve['temperature'] - moyenne)
            
            # Si l'écart dépasse le seuil, ajouter la date à la liste des anomalies
            if ecart > seuil:
                anomalies.append(releve['date'])
    
    # Étape 5 : Retourner la liste des dates anormales
    return anomalies

print("Question 2 : Tests de la fonction detecter_anomalies")
print(detecter_anomalies('Societe', 1.0, donnees_test))
print(detecter_anomalies('Marquises', 1.0, donnees_test))

# Remarque : l'exemple fourni dans l'énoncé ne correspond pas aux valeurs trouvées avec les données de test. 

# =================================================================================#
# code de la fonction evolution_par_decennie à corriger dans la question 4:


def evolution_par_decennie(zone, donnees):
    """
    Calcule l'évolution des températures moyennes par décennie pour une zone.

    ATTENTION: Cette fonction contient un bug volontaire à détecter et corriger.

    Arguments:
        zone (str): Nom de l'archipel (ex: 'Societe', 'Tuamotu')
        donnees (list): Liste de dictionnaires de relevés

    Renvoie:
        dict: Dictionnaire {décennie : température_moyenne}
              ex: {2010: 27.5, 2020: 28.3}
              Renvoie un dictionnaire vide si la zone n'existe pas
    """
    # Filtrage des relevés pour la zone
    releves_zone = [r for r in donnees if r['zone'] == zone]

    if not releves_zone:
        return {}

    # Regroupement par décennie
    temperatures_par_decennie = {}

    for releve in releves_zone:
        # Extraction de l'année de la date (format: 'YYYY-MM-DD')
        annee = int(releve['date'].split('-')[0])

        # Calcul de la décennie
        # Version initiale
        # decennie = (annee // 10) # BUG : division entière par 10 sans multiplier par 10 → les clés obtenues sont 202 au lieu de 2020 !
        # Version corrigée
        decennie = (annee // 10) * 10 # Correction : on multiplie par 10 pour obtenir la décennie complète (ex: 2020 au lieu de 202)

        if decennie not in temperatures_par_decennie:
            temperatures_par_decennie[decennie] = []

        temperatures_par_decennie[decennie].append(releve['temperature'])

    # Calcul des moyennes
    moyennes = {}
    for decennie, temperatures in temperatures_par_decennie.items():
        moyennes[decennie] = round(sum(temperatures) / len(temperatures), 2)

    return moyennes


# =================================================================================#
#  Exercice 2.1 :
"""
Tests
À compléter par le candidat dans le cadre de la question 3
"""


def test_zone_inexistante():
    """
    Test 1 : Tester une zone qui n'existe pas

    À compléter:
    1. Appeler evolution_par_decennie avec une zone inexistante
    2. Vérifier que le résultat est un dictionnaire vide
    """
    resultat = evolution_par_decennie('Australes', donnees_test)
    assert resultat == {}, f"Attendu {{}}, obtenu {resultat}"
    print("Test 1 OK : zone inexistante → {}")


def test_une_seule_decennie():
    """
    Test 2: Tester une zone avec données sur une seule décennie

    À compléter:
    1. Appeler evolution_par_decennie avec la zone appropriée
    2. Vérifier que le résultat ne contient qu'une seule décennie (2020)
    3. Vérifier la température moyenne
    """
    resultat = evolution_par_decennie('Marquises', donnees_test)
    # On s'attend à {2020: 26.0} mais on obtient {202: 26.0} !
    assert 2020 in resultat, f"Clé 2020 absente ! Clés obtenues : {list(resultat.keys())}"
    print("Test 2 OK")


def test_plusieurs_decennies():
    """
    Test 3 : Tester une zone avec données sur plusieurs décennies

    À compléter:
    1. Appeler evolution_par_decennie avec la zone appropriée
    2. Vérifier que le résultat contient bien les clés 2010 et 2020
    3. Vérifier que les températures moyennes sont cohérentes
    """
    resultat = evolution_par_decennie('Societe', donnees_test)
    assert 2010 in resultat, f"Clé 2010 absente ! Clés obtenues : {list(resultat.keys())}"
    assert 2020 in resultat, f"Clé 2020 absente ! Clés obtenues : {list(resultat.keys())}"
    print("Test 3 OK")

print("Question 3 : Tests de la fonction evolution_par_decennie")
test_zone_inexistante()
test_une_seule_decennie()
test_plusieurs_decennies()
# Les tests ne passent pas : les clés obtenues sont tronquées (202 au lieu de 2020) → il y a un bug dans la fonction evolution_par_decennie à corriger !

# Question 4 : Corriger le code de la fonction evolution_par_decennie pour que les tests passent
# Après la correction apportée dans la fonction evolution_par_decennie ci-dessus, les tests passent correctement et les clés des décennies sont correctes (2010 et 2020).
