# ///////////////////////////////////////////////////////////////////////////
# FONCTIONS DONNEES
# ///////////////////////////////////////////////////////////////////////////

def recupere_donnees_fichier_csv(nom_fichier):
    """ Fonction qui récupère les données relevées du ballon sonde sans les en-têtes de la 1ère ligne """
    altitudes = []                                  # Initialisation des listes de valeurs relevées
    temperatures = []
    longitudes = []
    latitudes = []
    # Ouverture du fichier csv au format npm.csv en mode "read"
    contenu_fichier = open(nom_fichier, 'r')
    # Supprime la 1ère ligne avec les en-têtes
    contenu_fichier.readline()
    # Parcours des lignes du fichier csv contenant les donnees relevées
    for ligne in contenu_fichier.readlines():
        # rstrip() supprime les \n et espaces en fin de ligne
        ligne = ligne.rstrip()
        # création d'une listeValeurs. split(";") sépare les valeurs grâce au ;
        listeValeurs = ligne.split(";")
        # conversion string en int de l'altitude et insertion dans la liste correspondante
        altitudes.append(int(listeValeurs[0]))
        # conversion string en float de l'altitude et insertion dans la liste correspondante
        temperatures.append(float(listeValeurs[1]))
        # conversion string en float de l'altitude et insertion dans la liste correspondante
        longitudes.append(float(listeValeurs[2]))
        # conversion string en float de l'altitude et insertion dans la liste correspondante
        latitudes.append(float(listeValeurs[3]))
    return altitudes, temperatures, longitudes, latitudes


def genere_kml(liste_longitudes, liste_latitudes):
    """ Fonction qui génère un fichier de données géographiques au format standard international KML
        Ce fichier est visionnable ensuite dans différents logiciels
    """
    #Ligne ajoutée à la question 4 pour vérifier que les deux listes ont le même nombre d'éléments
    assert len(liste_longitudes) == len(liste_latitudes), \
        "Les listes de longitudes et latitudes doivent avoir la même longueur"
    fichier_kml = open(
        'ballon sonde.kml', 'w')    # Création et ouverture du fichier kml en mode "write"
    entete_fichier = '<?xml version="1.0" encoding="UTF-8"?>\n'
    entete_fichier += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    entete_fichier += '<Document>\n'
    entete_fichier += '<name>Trajectoire ballon sonde</name>\n'
    # Ecriture du contenu de la variable entete_fichier dans le fichier kml
    fichier_kml.write(entete_fichier)
    for i in range(len(liste_longitudes)):
        corps_fichier = '<Placemark>\n'
        corps_fichier += f'<name>Point {i}</name>\n'
        corps_fichier += '<Point>\n'
        corps_fichier += f'<coordinates>{liste_longitudes[i]},{liste_latitudes[i]}</coordinates>\n'
        corps_fichier += '</Point>\n'
        corps_fichier += '</Placemark>\n'
        fichier_kml.write(corps_fichier)
    bas_fichier = '</Document>\n'
    fichier_kml.write(bas_fichier)
    # Ligne ajoutée à la question 6 pour ajouter la balise fermante </kml> à la fin du fichier kml
    fichier_kml.write('</kml>\n')
    fichier_kml.close()                         # Fermeture du fichier kml


# ///////////////////////////////////////////////////////////////////////////
# TRAVAIL DEMANDE
# ///////////////////////////////////////////////////////////////////////////

# QUESTION 1
altitudes, temperatures, longitudes, latitudes = recupere_donnees_fichier_csv("releves_ballon_sonde.csv")

print("Question 1 :")
print(f"Nombre de mesures : {len(altitudes)}")
print(f"Première altitude : {altitudes[0]} m")
print(f"Première température : {temperatures[0]} K")

# QUESTION 2
def conversion_K_en_C(liste_temperatures: list[float]) -> list[float]:
    """Convertit une liste de températures de kelvins en degrés Celsius."""
    liste_celsius = []
    for temp in liste_temperatures:
        liste_celsius.append(round(temp - 273.15, 1))
    return liste_celsius

print("Question 2 :")
temperatures_celsius = conversion_K_en_C(temperatures)
print(temperatures_celsius)

# QUESTION 3
def altitude_la_plus_froide(liste_altitudes: list[int], liste_temperatures: list[float]) -> tuple[float, list[int]]:
    """Renvoie un tuple (temp_min, [altitudes correspondantes])."""
    # Trouve la température minimale dans la liste des températures
    temp_min = min(liste_temperatures)
    # Initialise une liste vide pour stocker les altitudes correspondant à temp_min
    altitudes_min = []
    # Parcourt chaque indice i de la liste des températures
    for i in range(len(liste_temperatures)):
        # Vérifie si la température à l'indice i est égale à la température minimale
        if liste_temperatures[i] == temp_min:
            # Si oui, ajoute l'altitude correspondante à la liste altitudes_min
            altitudes_min.append(liste_altitudes[i])
    # Retourne un tuple contenant la température minimale et la liste des altitudes associées
    return (temp_min, altitudes_min)

print("Question 3 :")
print(altitude_la_plus_froide([7000, 10125, 13896, 14211], [-35.2, -52.1, -57.4, -57.4]))
print(altitude_la_plus_froide([6000, 7250, 11542, 15214, 17300], [-33.7, -45, -53, -58.5, -60.1]))

# QUESTION 4
# On ajoute la ligne : 
# assert len(liste_longitudes) == len(liste_latitudes), \
#         "Les listes de longitudes et latitudes doivent avoir la même longueur"
# au début de la fonction genere_kml pour vérifier que les deux listes ont le même nombre d'éléments.

# QUESTION 5
print("Question 5 :")
genere_kml(longitudes, latitudes)
print("Le fichier 'ballon sonde.kml' a été généré avec les coordonnées du ballon sonde.")

# QUESTION 6
# On modifie la fonction genere_kml pour ajouter la balise fermante </kml> à la fin du fichier kml, après la balise </Document>. Voir le fichier ci-dessus.