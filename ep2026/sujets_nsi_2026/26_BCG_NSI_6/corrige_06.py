class Boutique_smoothie:
    def __init__(self, liste_fruits_disponibles):
        self.liste_fruits_disponibles = liste_fruits_disponibles
        self.db_smoothies = {
            "Tropical": ["Mangue", "Ananas", "Banane"],
            "Rouge": ["Fraise", "Framboise", "Cerise"],
            "Vert": ["Kiwi", "Pomme verte", "Menthe"],
            "Agrume": ["Orange", "Citron", "Pamplemousse"],
            "Exotique": ["Papaye", "Fruit de la passion", "Noix de coco"],
            "Tropical citron": ["Mangue", "Ananas", "Citron"],
            "Rouge kiwi": ["Fraise", "Framboise", "Kiwi"],
            "Exotique rouge": ["Papaye", "Fraise", "Fruit de la passion"],
            "Vert citron": ["Kiwi", "Pomme verte", "Citron"],
            "Soleil couchant": ["Mangue", "Fraise", "Pamplemousse"]
        }

    ##### QUESTION 1 #####
    def smoothie_possible(self, nom_smoothie):
        """Retourne True si le smoothie peut être préparé avec les fruits disponibles, False sinon."""
        for fruit in self.db_smoothies[nom_smoothie]:
            if fruit not in self.liste_fruits_disponibles:
                return False
        return True

    ##### QUESTION 2 #####
    def liste_smoothies_possibles(self):
        """Retourne la liste des smoothies pouvant être préparés avec les fruits disponibles."""
        possibles = []
        for nom in self.db_smoothies:
            if self.smoothie_possible(nom):
                possibles.append(nom)
        return possibles

    ##### QUESTION 3 #####
    def score_proximite(self, nom1, nom2):
        """Retourne le nombre de fruits communs entre deux smoothies."""
        nb = 0
        fruits1 = self.db_smoothies[nom1]
        fruits2 = self.db_smoothies[nom2]
        for fruit in fruits1:
            if fruit in fruits2:
                nb += 1
        return nb

    # VERSION INTIALE A CORRIGER
    def plus_proche_possible(self, nom_smoothie_ref):
        """Retourne le nom du smoothie le plus proche de nom_smoothie_ref en termes de fruits communs parmi les smoothies possibles.
        En cas d'égalité, retourne le premier trouvé.
        """
        max_communs = 0
        smoothie_proche = None
        for nom_smoothie in self.db_smoothies:
            nb_communs = self.score_proximite(nom_smoothie_ref, nom_smoothie)
            if nb_communs > max_communs:
                max_communs = nb_communs
                smoothie_proche = nom_smoothie
        return smoothie_proche
    
    # VERSION CORRIGEE (QUESTION 4)
    def plus_proche_possible(self, nom_smoothie_ref):
        '''Version corrigée'''
        # Initialiser le score maximal et le smoothie le plus proche
        max_communs = 0
        smoothie_proche = None
        
        # Récupérer uniquement les smoothies réalisables avec les fruits disponibles
        # (au lieu d'itérer sur TOUS les smoothies de la base de données)
        possibles = self.liste_smoothies_possibles()
        
        # Parcourir chaque smoothie réalisable
        for nom_smoothie in possibles:
            # Exclure le smoothie de référence lui-même
            # (sinon il sera toujours le "plus proche" avec un score de 3)
            if nom_smoothie != nom_smoothie_ref:
                # Calculer le nombre de fruits communs
                nb_communs = self.score_proximite(nom_smoothie_ref, nom_smoothie)
                
                # Mettre à jour si on trouve un smoothie avec plus de fruits communs
                if nb_communs > max_communs:
                    max_communs = nb_communs
                    smoothie_proche = nom_smoothie
        
        # Retourner le smoothie le plus proche (ou None si aucun n'existe)
        return smoothie_proche

    def affichage_possibles(self):
        """Affiche les smoothies possibles."""
        smoothies = self.liste_smoothies_possibles()
        print("Smoothies possibles avec les fruits disponibles :")
        for smoothie in smoothies:
            print(smoothie)
        print("Alternative aux autres smoothies :")
        for smoothie in self.db_smoothies:
            if smoothie not in smoothies:
                proche = self.plus_proche_possible(smoothie)
                if proche != None:
                    print(f"Pour le smoothie {smoothie}, essayez {proche}.")
                else:
                    print(f"Pour le smoothie {smoothie}, aucun smoothie proche disponible.")

# ========= Fonctions de test ==================


def test_smoothie_possible():
    boutique = Boutique_smoothie(
        ["Mangue", "Ananas", "Banane", "Fraise", "Citron"])
    assert boutique.smoothie_possible("Tropical") == True
    assert boutique.smoothie_possible("Rouge") == False
    print("Tous les tests passent pour la méthode smoothie_possible!")


def test_liste_smoothies_possibles():
    boutique1 = Boutique_smoothie(
        ["Mangue", "Ananas", "Banane", "Fraise", "Citron"])
    boutique2 = Boutique_smoothie(
        ["Fraise", "Framboise", "Cerise", "Kiwi", "Orange", "Citron", "Pamplemousse"])
    boutique3 = Boutique_smoothie(["Orange", "Mangue", "Papaye"])
    assert boutique1.liste_smoothies_possibles() == [
        "Tropical", "Tropical citron"]
    assert boutique2.liste_smoothies_possibles() == [
        "Rouge", "Agrume", 'Rouge kiwi']
    assert boutique3.liste_smoothies_possibles() == []
    print("Tous les tests passent pour la méthode liste_smoothies_possibles!")

##############
# QUESTION 3 #
##############

def test_score_proximite():
    b = Boutique_smoothie(["Mangue", "Ananas", "Banane"])
    # Smoothie identique → score 3 (tous les fruits en commun)
    assert b.score_proximite("Tropical", "Tropical") == 3
    # Tropical et Tropical citron partagent Mangue et Ananas → 2
    assert b.score_proximite("Tropical", "Tropical citron") == 2
    # Tropical et Rouge n'ont aucun fruit en commun → 0
    assert b.score_proximite("Tropical", "Rouge") == 0
    # Soleil couchant et Tropical partagent Mangue → 1
    assert b.score_proximite("Soleil couchant", "Tropical") == 1
    print("Fonction score_proximite : Tous les tests passent !")

# Explications : On teste les cas limites : score maximal (même smoothie), score intermédiaire (2 fruits communs), score nul (aucun fruit commun), et score de 1 fruit commun.


def test_plus_proche_possible():
    boutique = Boutique_smoothie(
        ["Mangue", "Ananas", "Banane", "Fraise", "Citron", "Kiwi", "Pomme verte"])
    smoothie_proche = boutique.plus_proche_possible("Tropical")
    assert smoothie_proche == "Tropical citron"
    print("Tous les tests passent pour la méthode plus_proche_possible!")

    smoothie_proche2 = boutique.plus_proche_possible("Exotique")
    assert smoothie_proche2 == None

##############
# QUESTION 4 #
##############

# Explications : Deux problèmes dans la version originale :

# 1. La méthode itère sur tous les smoothies (`self.db_smoothies`) au lieu de se limiter aux smoothies **réalisables** (`self.liste_smoothies_possibles()`).
# 2. Le smoothie de référence n'est pas exclu de la recherche — il est toujours le plus proche de lui-même (score 3).

# Correction : On itère uniquement sur les smoothies possibles, et on ignore le smoothie de référence.
"""
def plus_proche_possible(self, nom_smoothie_ref):
    '''Version corrigée'''
    # Initialiser le score maximal et le smoothie le plus proche
    max_communs = 0
    smoothie_proche = None
    
    # Récupérer uniquement les smoothies réalisables avec les fruits disponibles
    # (au lieu d'itérer sur TOUS les smoothies de la base de données)
    possibles = self.liste_smoothies_possibles()
    
    # Parcourir chaque smoothie réalisable
    for nom_smoothie in possibles:
        # Exclure le smoothie de référence lui-même
        # (sinon il sera toujours le "plus proche" avec un score de 3)
        if nom_smoothie != nom_smoothie_ref:
            # Calculer le nombre de fruits communs
            nb_communs = self.score_proximite(nom_smoothie_ref, nom_smoothie)
            
            # Mettre à jour si on trouve un smoothie avec plus de fruits communs
            if nb_communs > max_communs:
                max_communs = nb_communs
                smoothie_proche = nom_smoothie
    
    # Retourner le smoothie le plus proche (ou None si aucun n'existe)
    return smoothie_proche
"""

# ======== Lancement des tests ========

test_smoothie_possible()
test_liste_smoothies_possibles()
test_score_proximite()
test_plus_proche_possible() #provoque une erreur dans la version originale, mais pas dans la version corrigée

##############
# QUESTION 5 #
##############
boutique = Boutique_smoothie(
    ["Mangue", "Ananas", "Banane", "Fraise", "Citron", "Kiwi", "Pomme verte"])
boutique.affichage_possibles()

# Explications : Le smoothie Agrume (Orange, Citron, Pamplemousse) n'est pas réalisable, car Orange et Pamplemousse ne sont pas disponibles. L'alternative proposée est le Tropical citron (ou Vert citron), car c'est le smoothie réalisable partageant le plus de fruits communs avec Agrume (le Citron).