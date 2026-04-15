import os
import os.path
import json

########### Fonctions données ###########

def chargement_json(nom_fichier):
    """Charge le contenu d'un fichier JSON dans un dictionnaire Python renvoyé"""
    with open(nom_fichier, "r", encoding="utf8") as curseur:
        return json.load(curseur)


def sauvegarde_json(dictionnaire, nom_fichier):
    """Sauvegarde le contenu d'un dictionnaire dans un fichier JSON"""
    with open(nom_fichier, "w", encoding="utf8") as curseur:
        json.dump(dictionnaire, curseur)


def est_dictionnaire(objet):
    """Teste si un objet est de type dictionnaire"""
    return isinstance(objet, dict)


##########################################


### Première fonction à implémenter après avoir découvert le fichier JSON agrégé
### Cf fichier `empreinte_ada_agr.json`
def total_simple(empreinte):
    """Fonction qui renvoie l'empreinte carbone totale d'un dictionnaire associant
    une empreinte carbone à des noms de catégories"""
    # Initialiser un accumulateur à zéro pour stocker la somme
    total = 0
    
    # Parcourir toutes les valeurs du dictionnaire (pas besoin des clés ici)
    for valeur in empreinte.values():
        # Ajouter chaque valeur au total (accumulation)
        total += valeur
    
    # Retourner la somme totale
    return total

def test_total_simple():
    # on charge l'empreinte agrégée d'Ada
    empreinte_agr = chargement_json("empreinte_ada_agr.json")
    print("Empreinte totale d'Ada :", total_simple(empreinte_agr), "kgCO2") # Résultat : 7252 kg

test_total_simple()


### Deuxième fonction : il faut la récursivité pour le cas des sous-catégories
### Cf fichier `empreinte_ada.json`
def total_rec(empreinte):
    """Fonction récursive qui renvoie l'empreinte carbone totale représentée
    par un dictionnaire dont les valeurs peuvent aussi être des dictionnaires"""
    # Initialiser un accumulateur à zéro pour stocker la somme
    total = 0
    
    # Parcourir toutes les valeurs du dictionnaire
    for valeur in empreinte.values():
        # Si la valeur est un dictionnaire, faire un appel récursif pour calculer sa somme
        if est_dictionnaire(valeur):
            total += total_rec(valeur)  # Ajouter le résultat de l'appel récursif au total
        else:
            total += valeur  # Ajouter la valeur directement au total si ce n'est pas un dictionnaire
    
    # Retourner la somme totale
    return total


def test_total_rec():
    test_dico1 = {"a": 1, "d": 2}
    assert total_rec(test_dico1) == 3
    test_dico2 = {"a": {"b": 1, "c": 2}, "d": {"e": 3}}
    assert total_rec(test_dico2) == 6
    # on charge l'empreinte d'Ada avec les sous-catégories
    empreinte = chargement_json("empreinte_ada.json")
    print("Empreinte totale d'Ada :", total_rec(empreinte), "kg") # Résultat : 7252 kg
    print("test_total_rec() : tous les tests sont passés")

test_total_rec()

# ==========================================
# Fonction à analyser et corriger (Question 3)
# ==========================================

def alerte_valeur_aberrante(empreinte, limite):
    """
    Fonction censée déterminer si au moins une valeur du dictionnaire
    dépasse strictement la limite donnée.
    """
    for categorie, valeur in empreinte.items():
        if est_dictionnaire(valeur):
            return alerte_valeur_aberrante(valeur, limite)
        else:
            if valeur > limite:
                return True
    return False

# Mise en évidence du problème
# Il y a une erreur dans l'énoncé, la fonction renvoie bien True.

# Ceci dit la fonction n'est pas correcte, car sa structure récursive empêche de parcourir la totalité du dictionnaire. Si un valeur supérieure à 1000 est à la fin du dictionnaire, elle n'est pas détectée.
# Exemple de test qui met en évidence le problème :
empreinte_test = {
    "chauffage": 800,
    "électricité": 500,
    #il faut un premier dictionnaire qui passe
    "alimentation": {
        "viande": 200,
        "légumes": 100
    },
    "transport": {
        "voiture": 300,
        "avion": 1200  # Valeur aberrante, mais elle ne sera pas détectée
    }
}
print("avion > 1000 ?", alerte_valeur_aberrante(empreinte_test, 1000))  # Devrait être True, mais renvoie False
# **Explications :** Le bug est le `return alerte_valeur_aberrante(valeur, limite)` qui renvoie immédiatement le résultat du premier appel récursif, sans explorer les autres catégories. Si la première sous-catégorie ne contient pas de valeur aberrante, la fonction renvoie `False` sans vérifier les suivantes. La correction : on ne fait `return True` que si l'appel récursif renvoie `True`, sinon on continue la boucle.

def alerte_valeur_aberrante_V2(empreinte, limite):
    '''Version corrigée'''
    for categorie, valeur in empreinte.items():
        if est_dictionnaire(valeur):
            if alerte_valeur_aberrante_V2(valeur, limite):
                return True
        else:
            if valeur > limite:
                return True
    return False

# Vérification de la correction
empreinte_detaillee = chargement_json("empreinte_ada.json")
print("Chauffage > 1000 ?", alerte_valeur_aberrante_V2(empreinte_detaillee, 1000))  # True
print("Valeur > 2000 ?", alerte_valeur_aberrante_V2(empreinte_detaillee, 2000))     # False
print("avion > 1000 ?", alerte_valeur_aberrante_V2(empreinte_test, 1000))  # True

##############
# QUESTION 4 #
##############

# Test 1 : dictionnaire plat sans dépassement
# Vérifie le cas de base (pas de récursion nécessaire)
assert alerte_valeur_aberrante_V2({"a": 10, "b": 20}, 50) == False

# Test 2 : dictionnaire plat avec dépassement
# Vérifie la détection dans le cas simple
assert alerte_valeur_aberrante_V2({"a": 10, "b": 100}, 50) == True

# Test 3 : dictionnaire imbriqué, dépassement dans une sous-catégorie profonde
# Vérifie que la récursion explore bien toutes les branches
assert alerte_valeur_aberrante_V2({"A": {"x": 10}, "B": {"y": {"z": 100}}}, 50) == True

# Test 4 : dictionnaire vide
# Vérifie le comportement aux limites
assert alerte_valeur_aberrante_V2({}, 100) == False

# Test 5 : valeur exactement égale à la limite (strictement supérieur)
# Vérifie la condition stricte
assert alerte_valeur_aberrante_V2({"a": 50}, 50) == False

# Test 6 : dépassement dans la dernière branche uniquement
# Vérifie que toutes les branches sont explorées, pas seulement la première
assert alerte_valeur_aberrante_V2({"A": {"x": 1}, "B": {"y": 2}, "C": {"z": 100}}, 50) == True

print("Tous les tests passent !")

# Test 1 : cas de base sans récursion, aucune valeur ne dépasse → False.
# Test 2 : cas de base avec dépassement → True.
# Test 3 : récursion profonde (3 niveaux), le dépassement n'est pas dans la première branche.
# Test 4 : dictionnaire vide, cas aux limites.
# Test 5 : valeur exactement égale à la limite, vérifie le « strictement supérieur ».
# Test 6 : le dépassement est dans la dernière branche → vérifie que le bug d'origine (arrêt prématuré) est bien corrigé.
