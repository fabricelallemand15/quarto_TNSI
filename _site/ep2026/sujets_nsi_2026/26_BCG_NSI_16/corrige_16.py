import csv
import matplotlib.pyplot as plt

############ Question 1  ############


def charger(nom_fichier):
    """
    Lit un fichier CSV (contenant les colonnes 'Year' et 'Anomaly') 
    et renvoie une liste de dictionnaires correctement typés.
    """
    donnees = []
    with open(nom_fichier, mode='r', encoding='utf-8') as f:
        lecteur = csv.DictReader(f)
        for ligne in lecteur:
            annee = int(ligne["Year"])
            ecart = float(ligne["Anomaly"])
            donnees.append({"année": annee, "écart": ecart})
    return donnees


# Chargement global des données
datas_temperature = charger("datas.csv")

#############################################################################
# Question 1 : Recherche de l'écart                                         #
#############################################################################
def ecart_temperature(datas: list[dict[str, float]], annee: int) -> float | None:
    """
    Recherche et retourne l'écart de température pour une année donnée.
    
    Paramètres:
        datas : liste de dictionnaires contenant les données météorologiques
        annee : l'année recherchée
    
    Retour:
        L'écart de température (float) si l'année est trouvée,
        None sinon
    """
    # Parcourir chaque dictionnaire de la liste de données
    for d in datas:
        # Si l'année du dictionnaire correspond à celle recherchée
        if d["année"] == annee:
            # Retourner immédiatement l'écart trouvé
            return d["écart"]
    
    # Si la boucle se termine sans trouver l'année, retourner None
    return None

# Jeu de tests
print("Tests question 1 :")
assert ecart_temperature(datas_temperature, 2020) == 1.01
assert ecart_temperature(datas_temperature, 1851) == -0.15
assert ecart_temperature(datas_temperature, 2050) is None
assert ecart_temperature(datas_temperature, 2025) == 1.29
print("Tous les tests passent !")
# Écrire la fonction ecart_temperature et ses tests ici


def derniere_annee_ecart_negatif(datas):
    annee = max([element["année"] for element in datas])
    ecart = ecart_temperature(datas, annee)
    while ecart >= 0:
        annee = annee - 1
        ecart = ecart_temperature(datas, annee)
    return annee

print("Question 2 : Dernière année avec écart négatif")
resultat = derniere_annee_ecart_negatif(datas_temperature)
print(f"Dernière année à écart négatif : {resultat}")
print(f"Écart cette année-là : {ecart_temperature(datas_temperature, resultat)} °C")

# La dernière année où la température mondiale était inférieure à la moyenne de référence est 1977 avec un écart de −0,03 °C.


#############################################################################
# Question 3 : Analyse et correction de bug                                 #
#############################################################################

def moyenne_ecarts(annee_debut, annee_fin, datas):
    """
    Renvoie la moyenne des écarts de température pour la période comprise 
    entre annee_debut et annee_fin (incluses).
    """
    somme = 0
    compteur = 0
    for dico in datas:
        if annee_debut <= dico["année"] and dico["année"] <= annee_fin:
            # somme = somme - dico["écart"] # Erreur : il faut additionner les écarts, pas les soustraire
            somme += dico["écart"] # Correction : utilisation de += pour additionner les écarts
            compteur += 1
    return somme / compteur


def prevision(datas, annee, n):
    """
    Renvoie l'écart de température attendu calculé par régression linéaire 
    sur les n dernières années.
    """
    longueur = len(datas)
    annee_debut = datas[longueur-n]["année"]
    annee_fin = datas[longueur-1]["année"]

    moy_annees = (annee_debut + annee_fin) / 2
    moy_temperatures = moyenne_ecarts(annee_debut, annee_fin, datas)

    numerateur = 0
    denominateur = 0
    for i in range(1, n+1):
        ecart_annee = datas[longueur-i]["année"] - moy_annees
        ecart_temp = datas[longueur-i]["écart"] - moy_temperatures
        numerateur += ecart_annee * ecart_temp
        denominateur += ecart_annee ** 2

    a = numerateur / denominateur
    b = moy_temperatures - a * moy_annees

    return a * annee + b

print("Question 3 : Prévision pour 2040")
print("Prévision pour 2040 :", prevision(datas_temperature, 2040, 20))
# Le résultat avant correction est absurde : -0.105 °C, ce qui est incohérent avec la tendance générale d'augmentation des températures.
# L'erreur** : dans `moyenne_ecarts`, la ligne `somme = somme - dico["écart"]` soustrait l'écart au lieu de l'additionner, inversant le signe de la moyenne. Avec le `+`, la prévision pour 2040 donne une valeur positive cohérente avec le réchauffement actuel.
# Le résultat après correction est d'environ 1.6 °C, ce qui est plus réaliste compte tenu de la tendance à l'augmentation des températures mondiales observée dans les données historiques.



#############################################################################
# Question 3 : Dataviz (Warming Stripes)                                    #
#############################################################################

def graphique(datas):
    """
    Représente visuellement les warming stripes.
    """
    fig, ax = plt.subplots(figsize=(10, 2))

    # Création d'une palette de couleurs basée sur l'amplitude thermique
    cmap = plt.get_cmap("seismic")
    temperatures = [dico["écart"] for dico in datas]
    max_val = max(max(temperatures), -min(temperatures))
    norm = plt.Normalize(-max_val, max_val)

    # Création des listes pour les abscisses et ordonnées
    annees = []
    ordonnees = []

    # Remplir les listes annees et ordonnees ici :
    for dico in datas:
        annees.append(dico["année"])
        ordonnees.append(1)  # La hauteur de chaque barre est fixe (1) car seule la couleur varie

    # Génération du graphique
    ax.bar(annees, ordonnees, width=1.0, color=cmap(norm(temperatures)))
    ax.set_title("Warming Stripes mondiales - Base 1901-2000")
    plt.yticks([], [])  # Masque l'axe Y car seule la couleur compte
    ax.set_xlabel("Année")

    plt.tight_layout()
    plt.show()

graphique(datas_temperature)