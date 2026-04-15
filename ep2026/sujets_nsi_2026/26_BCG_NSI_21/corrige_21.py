import datetime

def date_future(nb_jours):
    """Renvoie la date située nb_jours après aujourd'hui"""
    return datetime.date.today() + datetime.timedelta(days=nb_jours)

# Variable contenant les délais en jours pour chaque niveau (index 0 à 4)
DELAIS = [1, 3, 7, 15, 30]

class Carte:

    def __init__(self, question, reponse):
        self.question = question
        self.reponse = reponse
        self.niveau = 0
        # À la création, la carte est à réviser le jour même
        self.date_prochaine = datetime.date.today()

    def __repr__(self):
        return f"<Carte: {self.question} (Niveau {self.niveau})>"

    #############################################################################
    # Écrire la méthode traiter_reponse(self, succes) de la question 1          #
    #############################################################################
    def traiter_reponse(self, succes):
        # Si la réponse est correcte
        if succes:
            # Augmente le niveau si on n'a pas atteint le maximum (4)
            if self.niveau < 4:
                self.niveau += 1
        # Si la réponse est incorrecte
        else:
            # Réinitialise le niveau à 0
            self.niveau = 0
        # Met à jour la date de prochaine révision selon le délai du nouveau niveau
        self.date_prochaine = date_future(DELAIS[self.niveau])

# Des cartes et un paquet de cartes pour réaliser des tests
c1 = Carte("Capitale de l'Italie ?", "Rome")
c1.niveau = 2
c1.date_prochaine = date_future(4)
c2 = Carte("7 x 8 ?", "56")
c2.date_prochaine = date_future(1)
c3 = Carte("Symbole du Fer ?", "Fe")
c3.date_prochaine = date_future(7)

paquet = [c1, c2, c3]

# test de la méthode traiter_reponse
print("Question 1 : test de la méthode traiter_reponse")
c = Carte("2+2 ?", "4")
c.traiter_reponse(True)
print(f"Niveau {c.niveau}, prochaine : {c.date_prochaine}")  # 1, +3j
c.traiter_reponse(True)
print(f"Niveau {c.niveau}, prochaine : {c.date_prochaine}")  # 2, +7j
c.traiter_reponse(False)
print(f"Niveau {c.niveau}, prochaine : {c.date_prochaine}")  # 0, +1j
   
#############################################################################
# Écrire la fonction extraire_cartes_du_jour de la question 2               #
#############################################################################
def extraire_cartes_du_jour(paquet, date_jour):
    """Extrait les cartes à réviser pour une date donnée"""
    cartes = []
    # Parcourt toutes les cartes du paquet
    for carte in paquet:
        # Vérifie si la carte doit être révisée avant ou à la date donnée
        if carte.date_prochaine <= date_jour:
            cartes.append(carte)
    # Retourne la liste des cartes à réviser
    return cartes

print("Question 2 : test de la fonction extraire_cartes_du_jour")
print(f"Aujourd'hui : {extraire_cartes_du_jour(paquet, datetime.date.today())}")
print(f"Dans 10 jours : {extraire_cartes_du_jour(paquet, date_future(10))}")

#############################################################################
# Fonction défaillante à analyser et corriger pour la question 3            #
#############################################################################

def extraire_cartes_a_renforcer(paquet):
    """
    Parcourt le paquet et renvoie la liste des cartes ayant le 
    niveau d'avancement le plus faible.
    """
    if len(paquet) == 0:
        return []
        
    niveau_min = paquet[0].niveau
    a_renforcer = []
    
    for carte in paquet:
        if carte.niveau < niveau_min:
            niveau_min = carte.niveau
            # a_renforcer.append(carte) # Problème : on conserve les cartes précédentes même si elles ne sont plus au niveau minimum
            a_renforcer = [carte] # Correction : on réinitialise la liste des cartes à renforcer avec la nouvelle carte au niveau minimum
        elif carte.niveau == niveau_min:
            a_renforcer.append(carte)
            
    return a_renforcer


def test_renforcement():
    # Création d'un paquet de test
    c1 = Carte("Capitale de l'Italie ?", "Rome")
    c1.niveau = 2
    
    c2 = Carte("7 x 8 ?", "56")
    c2.niveau = 1
    
    c3 = Carte("Symbole du Fer ?", "Fe")
    c3.niveau = 2
    
    mon_paquet = [c1, c2, c3]
    
    # Appel de la fonction défaillante
    resultat = extraire_cartes_a_renforcer(mon_paquet)
    
    print("Cartes à renforcer (niveau le plus bas attendu : 1) :")
    print(resultat)

print("Question 3 : test de la fonction extraire_cartes_a_renforcer")
test_renforcement()

# Le bug : quand un nouveau minimum est trouvé (`carte.niveau < niveau_min`), la liste `a_renforcer` n'est pas vidée — les cartes de l'ancien niveau minimum y restent. Il faut remplacer `a_renforcer.append(carte)` par `a_renforcer = [carte]` pour réinitialiser la liste avec uniquement la nouvelle carte de niveau minimum.