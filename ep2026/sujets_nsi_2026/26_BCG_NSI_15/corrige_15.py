# -----------------------------------------------------------------------------
# Numéros de téléphones
# Question 1 : nettoyage des numéros de téléphone

# Écrire la fonction normalisation_tel ici
def normalisation_tel(tel: str) -> str:
    """
    Normalise un numéro de téléphone en supprimant tous les caractères
    non numériques (espaces, tirets, points, parenthèses, etc.).
    
    :param tel: numéro de téléphone avec formatages variés
    :return: numéro contenant uniquement les chiffres
    """
    resultat = ""  # Initialise une chaîne vide pour accumuler les chiffres
    
    # Parcourt chaque caractère du numéro de téléphone
    for c in tel:
        # Vérifie si le caractère est un chiffre (0-9)
        if c.isdigit():
            # Ajoute le chiffre à la chaîne de résultat
            resultat += c
    
    # Retourne le numéro nettoyé contenant uniquement les chiffres
    return resultat

import sqlite3


def test_normalisation_tel():
    """
    Tous les tests doivent passer...
    """
    assert normalisation_tel("06 12 99 90 12") == "0612999012"
    assert normalisation_tel("02 12 99 90 12") == "0212999012"
    assert normalisation_tel("02.12.99.90.12") == "0212999012"
    assert normalisation_tel("0.6.12.99.90.12") == "0612999012"
    assert normalisation_tel("06-12-99-90-12") == "0612999012"
    assert normalisation_tel("(0)6.12.99-90-12 gilbert") == "0612999012"
    assert normalisation_tel("061299901") == "061299901"
    assert normalisation_tel("06129990123") == "06129990123"
    print('Les tests de la fonction normalisation_tel sont passés')

print("Question 1 : tests de la fonction normalisation_tel")
test_normalisation_tel()
# -----------------------------------------------------------------------------
# Question 2 : validation des numéros de téléphone


def validation_tel(tel):
    """
    Validation des numéros de téléphone portable français
    selon les conditions spécifiées.
    :param tel: numéro de téléphone
    :return: True si le numéro est valide, False sinon
    """
    if len(tel) != 10:
        return False
    if tel[0] != "0":
        return False
    if tel[1] != "6" and tel[1] != "7":
        return False
    return True


# Ecrire votre jeu de tests permettant
# de vérifier le bon fonctionnement de la fonction.

print("Question 2 : tests de la fonction validation_tel")

# Cas valides
assert validation_tel("0612999012") == True   # numéro 06 valide
assert validation_tel("0712345678") == True   # numéro 07 valide

# Cas invalides : longueur
assert validation_tel("061299901") == False    # trop court (9 chiffres)
assert validation_tel("06129990123") == False  # trop long (11 chiffres)

# Cas invalides : préfixe
assert validation_tel("1612999012") == False   # ne commence pas par 0
assert validation_tel("0212999012") == False   # 02 n'est pas un portable
assert validation_tel("0512999012") == False   # 05 n'est pas un portable

print("Tous les tests passent !")

# On teste les cas limites : numéros valides (06, 07), numéros trop courts, trop longs, qui ne commencent pas par 0, et dont le deuxième chiffre n'est ni 6 ni 7.


# -----------------------------------------------------------------------------
# Détermination de la liste des chats à vacciner
# Question 3 : interrogation de la base de données

DB_PATH = "cabinet.sqlite"


def proprietaires_animaux_nes_apres(date):
    """
    Renvoie les noms et prénoms des propriétaires d'animaux nés après la date `date`,
    triés par ordre alphabétique de noms puis prénoms

    :param: date: date de naissance minimale
    :return: liste [(nom_proprietaire, prenom_ proprietaire)]
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    resultat = cursor.execute(
        """
    SELECT proprietaire.nom, proprietaire.prenom
    FROM proprietaire
        JOIN  animal ON proprietaire.id = animal.id_proprietaire 
    WHERE animal.date_naissance > ?
    ORDER BY proprietaire.nom, proprietaire.prenom;
    """,
        (date,),
    )
    return list(resultat)


def consultation_vaccination_chat(date: str) -> list:
    """
    Renvoie les consultations de vaccination de chats dont la date
    est supérieure à la date `date`.

    :param: date: date minimale
    :return: liste [(id_animal, nom_animal, tel_proprietaire, date_consultation)]
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    resultat = cursor.execute(
        """
    SELECT animal.id, animal.nom, proprietaire.telephone, consultation.date
    FROM consultation
        JOIN animal ON consultation.id_animal = animal.id
        JOIN proprietaire ON animal.id_proprietaire = proprietaire.id
    WHERE consultation.motif = 'vaccination'
        AND animal.espece = 'chat'
        AND consultation.date > ?
    ORDER BY animal.id, consultation.date;
    """,
        (date,),
    )
    return list(resultat)


def test_consultation_vaccination_chat():
    vaccinations = consultation_vaccination_chat("20240923")
    assert len(vaccinations) == 118
    assert vaccinations[0] == (16, "Plume", "0.6.36.96.89.83", "20241024")
    assert vaccinations[1] == (16, "Plume", "0.6.36.96.89.83", "20251125")
    assert vaccinations[2] == (17, "Gollum", "0.6.36.96.89.83", "20250113")
    assert vaccinations[3] == (26, "Olympe", "(0)4 73 98 01 23", "20250109")
    assert vaccinations[4] == (32, "Chopin", "06.37.97.66.64", "20241201")
    assert vaccinations[5] == (32, "Chopin", "06.37.97.66.64", "20251119")
    assert vaccinations[6] == (34, "Jazz", "0.6.37.51.65.52", "20250801")
    assert vaccinations[7] == (35, "Tango", "0324182", "20250706")
    assert vaccinations[8] == (38, "Loulou", "05-35-95-87-54", "20250209")
    print('Les tests de la fonction consultation_vaccination_chat sont passés')

print("Question 3 : tests de la fonction consultation_vaccination_chat")
test_consultation_vaccination_chat()

# -----------------------------------------------------------------------------
# Question 4 : détermination de la date de dernière vaccination


def derniere_vaccination(consultations: list) -> dict:
    """
    Renvoie un dictionnaire ayant pour clef l'identifiant de l'animal,
    et dont la valeur associée est la dernière consultation de cet animal.

    Chaque consultation est un tuple :

    (id_animal, nom_animal, tel_proprietaire, date_consultation)
    """
    derniere = {}
    for consult in consultations:
        id_animal = consult[0]
        date = consult[3]
        if id_animal not in derniere:
            derniere[id_animal] = consult
            # Correction apportée à la question 4 : on remplace < par >
        elif date > derniere[id_animal][3]:
            derniere[id_animal] = consult
    return derniere


def test_derniere_vaccination():
    consultations_pour_test = [
        (16, "Plume", "0.6.36.96.89.83", "20241024"),
        (16, "Plume", "0.6.36.96.89.83", "20251125"),
        (17, "Gollum", "0.6.36.96.89.83", "20250113"),
        (26, "Olympe", "(0)4 73 98 01 23", "20250109"),
        (32, "Chopin", "06.37.97.66.64", "20241201"),
        (32, "Chopin", "06.37.97.66.64", "20251119"),
        (34, "Jazz", "0.6.37.51.65.52", "20250801"),
        (35, "Tango", "0324182", "20250706"),
        (38, "Loulou", "05-35-95-87-54", "20250209"),
        (39, "Tango", "07.45.48.02.42", "20250329"),
        (40, "Sésame", "07.45.48.02.42", "20250228"),
        (41, "Pixel", "0130709285", "20241204"),
        (41, "Pixel", "0130709285", "20251222"),
    ]

    resultat = derniere_vaccination(consultations_pour_test)
    # Affichage des résultats, décommenter si besoin
    for a,r in resultat.items():
        print(a, ":", r)

    assert derniere_vaccination(consultations_pour_test) == {
        16: (16, "Plume", "0.6.36.96.89.83", "20251125"),
        17: (17, "Gollum", "0.6.36.96.89.83", "20250113"),
        26: (26, "Olympe", "(0)4 73 98 01 23", "20250109"),
        32: (32, "Chopin", "06.37.97.66.64", "20251119"),
        34: (34, "Jazz", "0.6.37.51.65.52", "20250801"),
        35: (35, "Tango", "0324182", "20250706"),
        38: (38, "Loulou", "05-35-95-87-54", "20250209"),
        39: (39, "Tango", "07.45.48.02.42", "20250329"),
        40: (40, "Sésame", "07.45.48.02.42", "20250228"),
        41: (41, "Pixel", "0130709285", "20251222"),
    }
    print('Les tests de la fonction derniere_vaccination sont passés')

print("Question 4 : tests de la fonction derniere_vaccination")
test_derniere_vaccination()
# Le problème : la condition `date < derniere[id_animal][3]` sélectionne la date la plus ancienne au lieu de la plus récente. Il suffit de remplacer `<` par `>` pour garder la consultation avec la date la plus récente.