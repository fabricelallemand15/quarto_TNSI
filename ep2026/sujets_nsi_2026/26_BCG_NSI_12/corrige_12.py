import csv

class Renard:
    """
    Classe représentant un renard dans le refuge.
    Attributs : identifiant, nom, poids, date_arrivee.
    """
    def __init__(self, identifiant, nom, poids, date_arrivee):
        ##############
        # Question 1 #
        ##############
        self.identifiant = identifiant
        self.nom = nom
        self.poids = poids
        self.date_arrivee = date_arrivee


    def __str__(self):
        ##############
        # Question 2 #
        ##############
        # Version avec chaînes formattées
        return f"Renard ID {self.identifiant} - {self.nom} (Arrivé le {self.date_arrivee})"
    
        # Version avec concaténation
        # return "Renard ID " + str(self.identifiant) + " - " + self.nom + " (Arrivé le " + self.date_arrivee + ")"

print("Test question 1 :")
r = Renard(101, "Zorro", 6.5, "2023-01-15")
print(r.identifiant, r.nom, r.poids, r.date_arrivee)

print("Test question 2 :")
renard1 = Renard(200, "Oscar", 5.1, "2026-01-01")
print(renard1)
# Affiche : Renard ID 200 - Oscar (Arrivé le 2026-01-01)

class Refuge:
    """
    Classe représentant le refuge contenant la liste des renards.
    """
    def __init__(self, nom, adresse):
        self.nom = nom
        self.adresse = adresse
        self.liste_renards = []
        
    def recueillir(self, un_renard):
        """
        Méthode d'ajout d'un renard au refuge.
        """
        self.liste_renards.append(un_renard)

    def lister_peu_corpulents(self):
        """
        Méthode qui renvoie une liste des Renards dont le poids est < 6.0 kg.
        """
        return [renard for renard in self.liste_renards if renard.poids < 6.0]

    def pourcentage_peu_corpulents(self):
        """
        Méthode qui renvoie le pourcentage des renards peu corpulents.
        """
        if len(self.liste_renards) == 0:
            return 0.0
        return len(self.lister_peu_corpulents()) / len(self.liste_renards) * 100

    def importer_donnees(self, nom_fichier):
        """
        Fonction qui importe les données des renards à partir d'un fichier CSV.
        """
        print(f"Tentative d'importation depuis {nom_fichier}...")
        with open(nom_fichier, 'r', encoding='utf-8') as f:
            lignes = csv.DictReader(f, delimiter=';')
            for ligne in lignes:
                # version corrigée avec conversion des types de données
                renard = Renard(int(ligne['id']), ligne['nom'], float(ligne['poids']), ligne['date_arrivee'])
                self.recueillir(renard)

##############
# Question 3 #
##############

# Explications : Le module `csv.DictReader` lit toutes les valeurs comme des chaînes de caractères. Il faut convertir `ligne['id']` en `int` et `ligne['poids']` en `float` pour que les opérations numériques ultérieures (comparaisons, calculs) fonctionnent correctement.
# La version ci-dessus est corrigée pour convertir les types de données lors de la création des objets Renard.

print("Test question 3 :")
refuge = Refuge("SOS Goupil", "123 Rue des Renards")
refuge.importer_donnees("donnees_renards.csv")
print(f"Refuge : {refuge.nom}")
print(f"Nombre de renards : {len(refuge.liste_renards)}")
print(refuge.liste_renards[0])
print(f"Type id : {type(refuge.liste_renards[0].identifiant)}")
print(f"Type poids : {type(refuge.liste_renards[0].poids)}")

##############
# Question 4 #
##############
print("Test question 4 :")
# Liste des renards peu corpulents
peu_corpulents = refuge.lister_peu_corpulents()
print(f"Renards peu corpulents (poids < 6.0 kg) :")
for r in peu_corpulents:
    print(f"  {r} - {r.poids} kg")

# Pourcentage
pct = refuge.pourcentage_peu_corpulents()
print(f"\nNombre de renards peu corpulents : {len(peu_corpulents)}")
print(f"Nombre total de renards : {len(refuge.liste_renards)}")
print(f"Pourcentage : {len(peu_corpulents)}/{len(refuge.liste_renards)} = {pct:.1f}%")