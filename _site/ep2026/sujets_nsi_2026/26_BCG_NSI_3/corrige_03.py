import calendar

#############################################################################
# Écrire le code de la fonction est_bissextile de la question 1             #
#############################################################################
def est_bissextile(annee):
    """Renvoie True si l'année est bissextile, False sinon."""
    # Une année est bissextile si elle est divisible par 4
    if annee % 4 == 0:
        # SAUF si elle est divisible par 100 (siècles non bissextiles)
        if annee % 100 == 0:
            # SAUF si elle est aussi divisible par 400 (exception aux siècles)
            # Exemple : 2000 est bissextile, 1900 ne l'est pas
            return annee % 400 == 0
        # Cas normal : divisible par 4 mais pas par 100
        return True
    # L'année n'est pas divisible par 4
    return False

#############################################################################
# Écrire le code de la fonction determiner_phase de la question 2           #
#############################################################################
def determiner_phase(jour):
    """Renvoie un entier correspondant au numéro de la phase associée
       Les phases sont définies comme suit :
       - Jours 1 à 5 : Règles -> 1
       - Jours 6 à 13 : Phase folliculaire -> 2
       - Jour 14 : Ovulation -> 3
       - Jours 15 à 28 : Phase lutéale -> 4
       Si le jour n'est pas compris entre 1 et 28, renvoie "Jour invalide"."""
    assert 1 <= jour <= 28, "Le jour doit être compris entre 1 et 28"
    if 1 <= jour <= 5:
        return 1
    elif 6 <= jour <= 13:
        return 2
    elif jour == 14:
        return 3
    elif 15 <= jour <= 28:
        return 4

#############################################################################
# Fonctions fournies pour la question 3                                     #
#############################################################################
def jours_dans_mois(annee, mois):
    """Renvoie le nombre de jours dans un mois donné d'une année donnée.
       Utilise le module calendar pour gérer les années bissextiles."""
    if mois == 2:  # février
        return 29 if calendar.isleap(annee) else 28
    elif mois in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    else:
        return 30

def ajouter_jours(date, nb_jours):
    """Ajoute nb_jours à une date donnée et renvoie la nouvelle date.
       La date est représentée par un tuple (jour, mois, année)."""
    jour, mois, annee = date
    jour = jour + nb_jours

    # Ajustement du jour et du mois si dépassement
    while jour > jours_dans_mois(annee, mois):
        jour = jour - jours_dans_mois(annee, mois)
        mois = mois + 1
        if mois > 12:  # passage à l'année suivante
            mois = 1
            annee = annee + 1

    return (jour, mois, annee)

def test_ajouter_jours():
    # Test fourni : ajout simple dans le même mois
    assert ajouter_jours((7, 9, 2025), 3) == (10, 9, 2025)

    # Test 1 : changement de mois (30 sept + 5 = 5 oct)
    assert ajouter_jours((28, 9, 2025), 5) == (3, 10, 2025)

    # Test 2 : passage d'année (31 déc + 1 = 1er janv)
    assert ajouter_jours((31, 12, 2025), 1) == (1, 1, 2026)

    # Test 3 : année bissextile (28 fév 2024 + 1 = 29 fév)
    assert ajouter_jours((28, 2, 2024), 1) == (29, 2, 2024)

    # Test 4 : année non bissextile (28 fév 2025 + 1 = 1 mars)
    assert ajouter_jours((28, 2, 2025), 1) == (1, 3, 2025)

    print("Tous les tests passent !")

test_ajouter_jours()

# Test 1 : verifie le changement de mois (passage de septembre a octobre)
# Test 2 : verifie le passage d'annee (31 decembre -> 1er janvier)
# Test 3 : verifie le comportement en annee bissextile (29 fevrier existe)
# Test 4 : verifie qu'en annee non bissextile, le 29 fevrier n'existe pas et on passe au 1er mars

    
#############################################################################
# Fonction fournie pour la question 4                                       #
#############################################################################
def calendrier_cycles(date_regles):
    """Renvoie une chaîne de caractère contenant au format iCalendar, l'ensemble
    des dates de début de règles qui se présentent dans les 100 jours suivants 
    `date_regles`, date incluse.

    Hypothèse : cycle régulier de 28 jours. """

    cal_lignes = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:']

    date_courante = date_regles
    jours_ecoules = 0

    # On ajoute les dates tant que l'on ne dépasse pas 100 jours écoulés
    while jours_ecoules + 28 <= 100:
        jour, mois, annee = date_courante  
        cal_lignes.append('BEGIN:VEVENT')
        cal_lignes.append('SUMMARY: Règles')
        #### ZONE CORRIGEE ####
        mois_str = str(mois)
        if mois < 10:
            mois_str = '0' + mois_str
        jour_str = str(jour)
        if jour < 10:
            jour_str = '0' + jour_str
        date = str(annee)+mois_str+jour_str
        ### FIN ZONE CORRIGEE ###
        cal_lignes.append('DTSTART:'+date)
        cal_lignes.append('END:VEVENT')
        date_courante = ajouter_jours(date_courante, 28)
        jours_ecoules += 28 

    cal_lignes.append('END:VCALENDAR')

    # La méthode join va renvoyer ici une unique chaîne contenant toutes les
    # chaînes de la liste séparées par des sauts de lignes.
    return '\n'.join(cal_lignes)

def test_calendrier_cycles():
    '''Crée un calendrier et le charge avec le module ics pour vérifier sa
    validité.

    Nécessite que le module ics soit présent sur la machine (pip install ics).
    '''
    from ics import Calendar
    c = calendrier_cycles( (12,3,2026) )
    print(c)
    cal = Calendar(c)
    print(cal.events)
    return None

test_calendrier_cycles()

##############
# QUESTION 4 #
##############

# Explications : Le problème est dans la construction de la date au format iCalendar. La ligne :
# date = str(annee)+str(mois)+str(jour)
# de la fonction initiale produit par exemple "2026312" pour le 12 mars 2026, au lieu de "20260312". Le format DTSTART exige exactement 8 caractères au format AAAAMMJJ, avec des zéros de remplissage pour les mois et jours inférieurs à 10.
# La correction ci-dessus garantit 4 chiffres pour l'année, 2 pour le mois et 2 pour le jour.
