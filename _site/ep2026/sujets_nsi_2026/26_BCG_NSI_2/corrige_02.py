import donnees
import donnees_completes
from math import sqrt

##############
# QUESTION 1 #
##############

def salaire_moyen_condition(employes, champ, valeur):
    '''Renvoie le salaire moyen des employes ayant val comme valeur associée
    au champ donné en argument.
    Si le nombre d'employés considéré est nul, cette fonction renvoie None'''
    
    # Initialiser les accumulateurs
    nombre = 0      # Compteur d'employés correspondant à la condition
    total = 0       # Somme des salaires correspondant à la condition
    
    # Parcourir tous les employés
    for employe in employes:
        # Vérifier si l'employé satisfait la condition
        if employe[champ] == valeur:
            nombre += 1                          # Incrémenter le compteur
            total += employe["salaire"]          # Ajouter le salaire à la somme
    
    # Calculer et retourner la moyenne
    if nombre > 0:
        # Il y a au moins un employé correspondant
        return total / nombre
    else:
        # Aucun employé ne correspond à la condition
        return None

empl_cplt = donnees_completes.employes
print(f"Salaire moyen des hommes sur les données complètes {salaire_moyen_condition(empl_cplt, 'sexe', 'M')}")
print(f"Salaire moyen des femmes sur les données complètes {salaire_moyen_condition(empl_cplt, 'sexe', 'F')}")

# Pour le jeu complet de données, on obtient 2438,04 € pour le salaire moyen des hommes et 2229,20 € pour le salaire moyen des femmes.

def test_salaire_moyen_condition():
    e = donnees.employes
    assert salaire_moyen_condition([], 'sexe', 'F') == None
    assert salaire_moyen_condition(e, 'sexe', 'F') == 2400.0
    assert salaire_moyen_condition(e, 'etudes', 3) == 2550.0
    assert salaire_moyen_condition(e, 'etudes', 12) == None

##############
# QUESTION 2 #
##############

def effectif_par_sexe(employes):
    '''Renvoie un dictionnaire ayant deux clés 'F' et 'M'
    associée respectivement au nombre d'employées femmes et au
    nombre d'employés hommes dans les données en arguments.'''
    
    # Initialiser les compteurs pour chaque sexe
    total_femmes = 0    # Nombre d'employées femmes
    total_hommes = 0    # Nombre d'employés hommes
    
    # Parcourir chaque employé de la liste
    for employe in employes:
        # Vérifier le sexe et incrémenter le compteur correspondant
        if employe['sexe'] == 'F':
            total_femmes += 1           # Ajouter 1 au compteur des femmes
        elif employe['sexe'] == 'M':
            total_hommes += 1           # Ajouter 1 au compteur des hommes
    
    # Retourner un dictionnaire avec les deux effectifs
    return {'F': total_femmes, 'M': total_hommes}
    

def test_effectif_par_sexe():
    e = donnees.employes
    assert effectif_par_sexe(e) == { 'F' : 3, 'M' : 3 }

##############
# QUESTION 3 #
##############

# Version de départ de la fonction, à corriger
# def calcul_ecart_sexe(employes):
#     '''Renvoie l'écart de salaire en pourcentage pour les femmes 
#     par rapport aux hommes'''
#     moy_h = salaire_moyen_condition(employes, 'sexe', 'M')
#     moy_f = salaire_moyen_condition('employes', 'sexe', 'F')
#     return moy_h - moy_f

# Le code original contient trois erreurs :

# 1. `'employes'` au lieu de `employes` : la chaîne de caractères `'employes'` est passée à la place de la variable `employes`, ce qui provoque une erreur car on itère sur les caractères de la chaîne.
# 2. Pas de gestion de `None` : si un seul sexe est présent, `salaire_moyen_condition` renvoie `None` et la soustraction échoue.
# 3. Formule incorrecte : `moy_h - moy_f` donne une différence en euros, pas un pourcentage. Il faut diviser par `moy_h` et multiplier par 100. 

# Version corrigée de la fonction :
def calcul_ecart_sexe(employes):
    '''Renvoie l'écart de salaire en pourcentage pour les femmes 
    par rapport aux hommes'''
    
    # Étape 1 : Obtenir les effectifs par sexe pour vérifier la présence des deux sexes
    effectifs = effectif_par_sexe(employes)
    
    # Étape 2 : Vérifier qu'il y a au moins un homme ET une femme
    # Sinon, impossible de calculer un écart de comparaison
    if effectifs['F'] == 0 or effectifs['M'] == 0:
        return None
    
    # Étape 3 : Calculer les salaires moyens pour chaque sexe
    moy_h = salaire_moyen_condition(employes, 'sexe', 'M')  # Salaire moyen des hommes
    moy_f = salaire_moyen_condition(employes, 'sexe', 'F')  # Salaire moyen des femmes
    
    # Étape 4 : Calculer l'écart en pourcentage
    # Formule : ((moy_h - moy_f) / moy_h) * 100
    # Cette formule exprime la différence en pourcentage du salaire des hommes
    return (moy_h - moy_f) * 100 / moy_h

def test_calcul_ecart_sexe():
    assert calcul_ecart_sexe([{'sexe': 'F', 'salaire': 1000, 'experience': 1, 'etudes': 1}]) == None
    e_test = [{'sexe': 'M', 'salaire': 2000, 'experience': 1, 'etudes': 1},{'sexe': 'F', 'salaire': 1800, 'experience': 1, 'etudes': 1}]
    ecart = calcul_ecart_sexe(e_test)
    assert 0 <= ecart <= 100
    assert ecart == 10.0
    print("Tous les tests passent !")

# test_calcul_ecart_sexe()
print(f"Écart moyen sur les données complètes : {calcul_ecart_sexe(donnees_completes.employes)} %")

# L'écart de salaire moyen dans les données complètes est d'environ 8,6 %.
    

# Attribution d'un premier salaire après embauche par les k plus proches voisins

def sexe_vers_entier(e):
    if e['sexe'] == 'F':
        return 1
    else:
        return -1

def distance(e1, e2):
    '''Renvoie la mesure de distance entre deux personnes.'''
    s = 0
    #s = s + (sexe_vers_entier(e1) - sexe_vers_entier(e2))**2
    s = s + (e1['experience'] - e2['experience'])**2
    s = s + (e1['etudes'] - e2['etudes'])**2
    return sqrt(s)

def k_plus_proches(k, employes, e):
    '''Renvoie les k employes les plus proches de e par la 
    distance définie au dessus.'''
    e_d = [(distance(e, employes[i]), i) for i in range(len(employes))]
    e_d.sort() # va trier en premier sur la distance
    voisins = []
    for i in range(k):
        voisins.append(employes[e_d[i][1]])
    return voisins

def salaire_moyen(employes):
    '''Renvoie le salaire moyen pour une liste d'employes'''
    if len(employes) == 0:
        return None
    s = sum(e['salaire'] for e in employes)
    return s/len(employes)

def salaire_par_proximite(employes, e):
    '''Prend en entrée une liste d'employés et un dictionnaire comportant
    les champs experience, etudes et sexe et renvoie le salaire le plus
    proche en moyennant les 3 plus proches voisins'''
    voisins = k_plus_proches(3, employes, e)
    return salaire_moyen(voisins)

test1 = {'experience': 3, 'etudes': 3, 'sexe': 'F'}
test2 = {'experience': 3, 'etudes': 3, 'sexe': 'M'}
print(salaire_par_proximite(donnees_completes.employes, test1))
print(salaire_par_proximite(donnees_completes.employes, test2))

# Telle qu'elle est donnée, la fonction propose un salaire inférieure à la candidate femme par rapport à la candidate homme, alors que les deux ont les mêmes caractéristiques d'expérience et d'études.
# Le problème vient de la fonction distance qui inclut le sexe dans le calcul de distance via sexe_vers_entier. 
# Cela signifie que les candidats femmes sont considérés comme plus « proches » des employées femmes (qui ont des salaires plus bas dans les données) 
# et les candidats hommes des employés hommes (salaires plus élevés). L'algorithme reproduit et amplifie les biais présents dans les données historiques.

# La correction consiste à retirer le sexe du calcul de distance, pour que seuls l'expérience et le niveau d'études déterminent les voisins les plus proches. 
# Ainsi, un homme et une femme avec les mêmes caractéristiques reçoivent la même proposition de salaire.
