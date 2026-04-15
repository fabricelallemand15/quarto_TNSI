from Objet3D_corr import Objet3D

#############################################################################
# Variables et fonctions fournies pour la question 3                        #
#############################################################################
parametres_imprimante = {'remplissage': 20,
                         'vitesse_extrusion': 8}  # 8mm3 / seconde


def volume_cube(cube):
    a, b = cube.sommets_adjacents()
    taille_cote = a.distance(b)  # distance donnee en mm
    return taille_cote ** 3

#############################################################################
# Écrire le code de la fonction estimation_impression de la question 3      #
#############################################################################
def estimation_impression(volume, parametres):
    """Estime le temps d'impression en secondes."""
    # Calcul du volume réel à imprimer en tenant compte du taux de remplissage
    # Exemple: 1000 mm³ avec 20% de remplissage = 200 mm³ à extruder
    volume_impression = volume * parametres['remplissage'] / 100
    
    # Calcul du temps d'impression en divisant le volume par la vitesse d'extrusion
    # Exemple: 200 mm³ à 8 mm³/sec = 25 secondes
    temps = volume_impression / parametres['vitesse_extrusion']
    
    return temps

print("Question 3 :")
print(estimation_impression(1000, parametres_imprimante))  # 25.0

#############################################################################
# Programme à modifier de la question 4 et 5                                #
#############################################################################
print("Question 4 :")
#Code initial :
# objet = Objet3D()
# objet.ajouter_sommet(0, 0, 0)
# objet.ajouter_sommet(0, 1, 0)
# objet.ajouter_sommet(1, 1, 0)
# objet.ajouter_sommet(1, 0, 0)
# objet.ajouter_face([1, 2, 3, 4])
# objet.afficher()

pyramide = Objet3D()
pyramide.nom = "pyramide"

# Sommets de la base (plan z=0)
pyramide.ajouter_sommet(0, 0, 0)    # Sommet 1
pyramide.ajouter_sommet(2, 0, 0)    # Sommet 2
pyramide.ajouter_sommet(2, 2, 0)    # Sommet 3
pyramide.ajouter_sommet(0, 2, 0)    # Sommet 4
# Sommet du haut
pyramide.ajouter_sommet(1, 1, 2)  # Sommet 5

# Faces
pyramide.ajouter_face([1, 2, 3, 4])  # Base carrée
pyramide.ajouter_face([1, 2, 5])      # Face avant
pyramide.ajouter_face([2, 3, 5])      # Face droite
pyramide.ajouter_face([3, 4, 5])      # Face arrière
pyramide.ajouter_face([4, 1, 5])      # Face gauche

# pyramide.afficher()

print("Question 5 :")

# Code modifié de la méthode implémenté dans Objet3D_corr.py

# def transformer_ameliore(self, rapport):
#     """Renvoie un nouvel Objet3D transformé sans modifier l'original."""
#     nouvel_objet = Objet3D()
#     nouvel_objet.nom = self.nom + f" (x{rapport})"
#     for sommet in self.sommets:
#         nouvel_objet.ajouter_sommet(
#             sommet.x * rapport,
#             sommet.y * rapport,
#             sommet.z * rapport
#         )
#     for face in self.faces:
#         nouvel_objet.ajouter_face(face.sommets)
#     return nouvel_objet

print("Début transformation de la pyramide...")
grande_pyramide = pyramide.transformer(2)
print("Transformation terminée.")
print(grande_pyramide)
print("=== Pyramide originale ===")
pyramide.afficher()
print("\n=== Pyramide agrandie (rapport 2) ===")
grande_pyramide.afficher()

# La version améliorée crée un nouvel `Objet3D`, y copie les sommets transformés (coordonnées multipliées par le rapport) et les faces. L'objet original n'est pas modifié. C'est le principe d'une méthode sans effet de bord.