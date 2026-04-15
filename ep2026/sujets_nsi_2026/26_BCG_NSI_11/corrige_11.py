from math import sqrt
from donnees_habitats import zones_connues

# Variable corrigée : il manquait la clé "presence_renard" dans le dictionnaire "nouveau".
nouveau = {'vegetation': 5, 'proximite_eau': 2, 'densite_urbaine': 4, 'disponibilite_proies': 6, "presence_renard": 0}

##############
# Question 1 #
##############
def distance(habitat_1, habitat_2):
    '''
    Calcule la distance euclidienne entre deux habitats.
    entrée : 
        - habitat_1 : dictionnaire représentant un habitat.
        - habitat_2 : dictionnaire représentant un autre habitat.
    sortie : 
        - float : distance euclidienne entre habitat_1 et habitat_2.
    '''
    cles = ['vegetation', 'proximite_eau', 'densite_urbaine', 'disponibilite_proies', 'presence_renard']
    somme = 0
    for cle in cles:
        somme += (habitat_1[cle] - habitat_2[cle]) ** 2
    return sqrt(somme)

print("Test de la question 1 :")
h1 = {'vegetation': 5, 'proximite_eau': 2, 'densite_urbaine': 4, 'disponibilite_proies': 6, 'presence_renard': 0}
h2 = {'vegetation': 9, 'proximite_eau': 6, 'densite_urbaine': 0, 'disponibilite_proies': 4, 'presence_renard': 1}
print(distance(h1, h2))

####################
# Questions 2 et 3 #
####################
def distance_d_un_habitat(habitat, habitats):
    '''
    Calcule la distance entre un habitat et chaque habitat de la liste.
    entrée : 
        - habitat : dictionnaire représentant un habitat.
        - habitats : liste de dictionnaires représentant des habitats.
    sortie : 
        - list[tuple] : liste de tuples (distance, habitat) où distance est la distance entre habitat et chaque habitat de la liste.
    '''
    resultat = []
    for h in habitats:
        d = distance(habitat, h)
        resultat.append((d, h))
    return resultat

# Avec l'habitat "nouveau" défini dans le fichier fourni, la fonction renvoie une erreur car "nouveau" ne contient pas la clé "presence_renard". C'est sans doute une erreur dans la question, il faudrait ajouter la clé "presence_renard" à "nouveau" pour que la fonction puisse fonctionner correctement. Par exemple, on peut ajouter "presence_renard": 0 à "nouveau". Ce que j'ai fait pour les tests ci-dessous.

print("Test des questions 2 et 3 :")
res = distance_d_un_habitat(nouveau, zones_connues[:3])
for t in res:
    print(t)

##############
# Question 4 #
##############

def k_plus_proches(k, habitat, habitats):
    '''
    Calcule les k habitats les plus proches de l'habitat donné.
    entrée : 
        - k : entier représentant le nombre d'habitats à retourner.
        - habitat : dictionnaire représentant un habitat.
        - habitats : liste de dictionnaires représentant des habitats.
    sortie : 
        - list[tuple] : liste de tuples (distance, habitat) l'élément à l'indice 0 est la distance euclidienne entre habitat 
                        et chaque habitat de la liste et l'élément à l'indice 1 est le dictionnaire correspondant à l'habitat correspondant.
    '''
    # On calcule les distances
    distances = distance_d_un_habitat(habitat, habitats)
    # On cherche à trier les distances en fonction de la distance euclidienne.
    distances.sort(key = lambda x: x[0])
    return distances[:k] # renvoie les distances jusque la borne k non comprise

# Version d'origine à corriger :
def presence_renard(k, habitat, habitats):
    '''
    Vérifie si l'habitat donné a plus de k/2 voisins avec des renards.
    entrée : 
        - k : entier représentant le nombre d'habitats à considérer.
        - habitat : dictionnaire représentant un habitat.
        - habitats : liste de dictionnaires représentant des habitats.
    sortie : 
        - bool : True si l'habitat a plus de k/2 voisins avec des renards, False sinon.
    '''
    habitats = k_plus_proches(k, habitat, habitats)
    n_renards = 0
    for habitat in habitats:
        distance = habitat[0]
        caracteristiques = habitat[1]
        if distance['presence_renard'] == 1:
            n_renards += 1
    return n_renards > k/2

# Version corrigée :
def presence_renard(k, habitat, habitats):
    """Version corrigée : utilise caracteristiques au lieu de distance."""
    habitats_proches = k_plus_proches(k, habitat, habitats)
    n_renards = 0
    for h in habitats_proches:
        dist = h[0]
        caracteristiques = h[1]
        if caracteristiques['presence_renard'] == 1:  # Corrigé
            n_renards += 1
    return n_renards > k / 2

print("Test de la question 4 :")
print(presence_renard(3, nouveau, zones_connues))
print(presence_renard(10, nouveau, zones_connues))

# Explications : Le bug est `distance['presence_renard']` au lieu de `caracteristiques['presence_renard']`. La variable `distance` contient un flottant (la distance calculée), pas un dictionnaire. C'est `caracteristiques` (le dictionnaire de l'habitat) qui contient la clé `'presence_renard'`.

##############
# Question 5 #
##############
print("Question 5 :")
for k in [1, 3, 5, 7, 9, 11]:
    resultat = presence_renard(k, nouveau, zones_connues)
    print(f"k = {k} : {'Présence probable' if resultat else 'Absence probable'}")

# Explications : En testant avec plusieurs valeurs de k, on observe la tendance majoritaire. Si la plupart des valeurs de k donnent `False`, l'habitat `nouveau` n'est probablement pas susceptible de contenir une population de renards. La méthode des k-NN est plus robuste quand on teste plusieurs valeurs de k et qu'on observe la tendance.
