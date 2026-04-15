import random


class Coccinelle:
    def __init__(self, sexe, age, niv_nutrition):
        self.age = age
        self.esperance_de_vie = random.randint(200, 350)
        self.sexe = sexe
        self.niv_nutrition = niv_nutrition

    def chasser(self, nb_proies, nb_coccinelles):
        # Cas particulier : s'il n'y a aucune coccinelle, les proies ne diminuent pas
        if nb_coccinelles == 0:
            return nb_proies

        # Calcul du ratio proies disponibles par coccinelle
        # (pour adapter la quantité de nourriture selon l'abondance)
        proies_par_cocci = nb_proies / nb_coccinelles

        # Détermination de la quantité à chasser selon l'abondance de proies
        if proies_par_cocci > 20:
            # Cas 1 : Abondance de proies → chasse abondante (12 à 20 proies)
            consomme = random.randint(12, 20)
        elif proies_par_cocci > 10:
            # Cas 2 : Ressources moyennes → chasse modérée (8 à 15 proies)
            consomme = random.randint(8, 15)
        else:
            # Cas 3 : Famine → chasse faible (3 à 8 proies)
            consomme = random.randint(3, 8)

        # Vérification : on ne peut pas manger plus de proies qu'il n'en existe
        consomme = min(consomme, nb_proies)

        # Mise à jour du niveau de nutrition en fonction du repas
        if consomme >= 10:
            # Bonne chasse : augmentation du niveau de nutrition
            self.niv_nutrition += 1
        else:
            # Mauvaise chasse : diminution du niveau (minimum 0)
            self.niv_nutrition = max(0, self.niv_nutrition - 1)

        # Retour du nombre de proies restantes après cette chasse
        return nb_proies - consomme

    # Version initiale des méthodes reproduction() et a_survecu() :
    def reproduction(self):
        """
        Une femelle avec un niveau de nutrition >= 2 engendre exactement
        deux descendants : un mâle et une femelle.
        """
        descendants = []
        if self.sexe == "femelle" and self.niv_nutrition >= 2:
            descendants.append(Coccinelle("male", 0, 0))
            descendants.append(Coccinelle("femelle", 0, 0))
            self.niv_nutrition = 0

        return descendants

    def a_survecu(self):
        """
        Met à jour l'âge de la coccinelle et indique si elle est encore en vie.
        """
        self.age = self.age + 1
        return self.age < self.esperance_de_vie
    
    # Version modifiée pour la question 4 (maturité sexuelle et mortalité par faim) :
    def reproduction(self):
        '''Version corrigée avec maturité sexuelle (>= 20 jours)'''
        descendants = []
        # La femelle ne peut se reproduire que si 3 conditions sont réunies :
        # 1. Elle est femelle (sexe == "femelle")
        # 2. Elle est bien nourrie (niveau de nutrition >= 2)
        # 3. Elle a atteint la maturité sexuelle (âge >= 20 jours)
        if self.sexe == "femelle" and self.niv_nutrition >= 2 and self.age >= 20:
            # Création de deux descendants : un mâle et une femelle
            descendants.append(Coccinelle("male", 0, 0))
            descendants.append(Coccinelle("femelle", 0, 0))
            # Après la reproduction, la mère épuisée perd toute son énergie
            self.niv_nutrition = 0
        return descendants

    def a_survecu(self):
        '''Version corrigée avec mortalité par manque de nourriture'''
        # Vieillissement inévitable : chaque jour l'âge augmente de 1
        self.age = self.age + 1
        
        # Condition 1 : mort naturelle si l'espérance de vie est atteinte
        if self.age >= self.esperance_de_vie:
            return False
        
        # Condition 2 : mort par famine
        # Si la coccinelle est affamée (nutrition = 0), elle a 1 chance sur 3
        # de mourir ce jour-là (représentant la faiblesse due à la faim)
        if self.niv_nutrition == 0 and random.random() < 1/3:
            return False
        
        # Si aucune condition de mort n'est remplie, la coccinelle survit
        return True

    def __repr__(self):
        return f"Coccinelle {self.sexe}, âge: {self.age}/{self.esperance_de_vie}, niv_nutrition: {self.niv_nutrition}"


def evolution(population, nb_proies):
    """
    Simule une journée dans l'écosystème :
    - chasse des coccinelles
    - reproduction
    - vieillissement et mortalité
    - croissance des pucerons

    population est une liste d'instances de la classe Coccinelle
    nb_proies est un entier indiquant le nombre de proies

    Cette fonction renvoie un couple (population_suivante, nouveau_nb_proies) indiquant
    la nouvelle population à la fin de la journée et le nombre de proies.
    """
    population_suivante = []
    nouveau_nes = []
    nb_coccinelles = len(population)

    for coccinelle in population:
        nb_proies = coccinelle.chasser(nb_proies, nb_coccinelles)

        if coccinelle.a_survecu():
            population_suivante.append(coccinelle)

        nouveau_nes += coccinelle.reproduction()

    # Croissance naturelle des pucerons (augmentation de 20% par jour)
    nb_proies = int(nb_proies * 1.2)

    # Ajout des nouveau-nés en fin de journée
    population_suivante += nouveau_nes

    return population_suivante, nb_proies


#############################################################################
# Écrire ci-dessous le code pour les questions de l'énoncé                  #
#############################################################################

##############
# QUESTION 1 #
##############

# Créer la population initiale
population = [
    Coccinelle("femelle", 10, 2),
    Coccinelle("femelle", 10, 2),
    Coccinelle("male", 10, 2)
]
nb_proies = 200

# Simuler 5 jours
for jour in range(1, 6):
    population, nb_proies = evolution(population, nb_proies)
    print(f"Jour {jour} : {len(population)} coccinelles, {nb_proies} pucerons")

##############
# QUESTION 2 #
##############

def simulation_simple(population, nb_proies):
    '''Simule l'écosystème sur 30 jours max.
    S'arrête si population ou proies tombent à 0.
    Renvoie (nb_coccinelles, nb_proies, nb_jours).'''
    
    # Initialiser le compteur de jours
    nb_jours = 0
    
    # Boucle de simulation : maximum 30 jours
    while nb_jours < 30:
        # Appliquer une journée d'évolution à l'écosystème
        population, nb_proies = evolution(population, nb_proies)
        
        # Incrémenter le compteur de jours
        nb_jours += 1
        
        # Conditions d'arrêt : extinction de l'une des deux espèces
        if len(population) == 0 or nb_proies == 0:
            break
    
    # Retourner les résultats finaux sous forme de tuple
    return (len(population), nb_proies, nb_jours)


pop = [Coccinelle("femelle", 10, 2), Coccinelle("femelle", 10, 2), Coccinelle("male", 10, 2)]
resultat = simulation_simple(pop, 1000)
print(f"Résultat : {resultat[0]} coccinelles, {resultat[1]} pucerons, {resultat[2]} jours")

##############
# QUESTION 3 #
##############

# Voir les commentaires dans le code de la méthode chasser() de la classe Coccinelle ci-dessus

"""
Méthode chasser(self, nb_proies, nb_coccinelles)
-------------------------------------------------
Simule la chasse d'une coccinelle parmi les proies disponibles.

Paramètres :
- nb_proies : nombre total de pucerons disponibles (entier)
- nb_coccinelles : nombre total de coccinelles dans la population (entier)

Retour :
- Le nombre de proies restantes après la chasse (entier)

Fonctionnement :
1. Si aucune coccinelle n'est présente, le nombre de proies reste inchangé.
2. On calcule le ratio proies/coccinelle pour adapter l'effort de chasse :
   - Si plus de 20 proies par coccinelle : chasse abondante (12 à 20 proies)
   - Si entre 10 et 20 proies par coccinelle : chasse modérée (8 à 15 proies)
   - Sinon : chasse faible (3 à 8 proies)
3. Le nombre consommé ne peut pas dépasser le nombre de proies restantes.
4. Si la coccinelle consomme 10 proies ou plus, son niveau de nutrition
   augmente de 1 (elle s'est bien nourrie).
   Sinon, son niveau de nutrition diminue de 1 (sans descendre en dessous de 0).
5. On renvoie le nombre de proies restantes.
"""

##############
# QUESTION 4 #
##############

# Voici la nouvelle version des méthodes : 
    # def reproduction(self):
    #     '''Version corrigée avec maturité sexuelle (>= 20 jours)'''
    #     descendants = []
    #     if self.sexe == "femelle" and self.niv_nutrition >= 2 and self.age >= 20:
    #         descendants.append(Coccinelle("male", 0, 0))
    #         descendants.append(Coccinelle("femelle", 0, 0))
    #         self.niv_nutrition = 0
    #     return descendants

    # def a_survecu(self):
    #     '''Version corrigée avec mortalité par manque de nourriture'''
    #     self.age = self.age + 1
    #     if self.age >= self.esperance_de_vie:
    #         return False
    #     if self.niv_nutrition == 0 and random.random() < 1/3:
    #         return False
    #     return True

# Ces versions modifiées sont implémentées dans la classe Coccinelle ci-dessus, remplaçant les versions initiales.
# Test
pop = [Coccinelle("femelle", 10, 2), Coccinelle("femelle", 10, 2), Coccinelle("male", 10, 2)]
nb_proies = 1000
for jour in range(1, 31):
    pop, nb_proies = evolution(pop, nb_proies)
    if len(pop) == 0 or nb_proies == 0:
        break
    print(f"Jour {jour} : {len(pop)} coccinelles, {nb_proies} pucerons")

# Explications :

# - Maturité sexuelle : On ajoute la condition `self.age >= 20` dans `reproduction`. Les coccinelles de moins de 20 jours ne peuvent plus se reproduire.
# - Mortalité par famine : Dans `a_survecu`, si `niv_nutrition == 0`, on tire un nombre aléatoire. Si ce nombre est inférieur à 1/3, la coccinelle meurt.
