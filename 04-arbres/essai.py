graphe = {
    "Lyon": [{"Grenoble":106}, {"Aix":292}],
    "Grenoble": [{"Lyon":106}, {"Aix":239}, {"Nice":293}],
    "Aix": [{"Lyon":292}, {"Grenoble":239}, {"Nice":174}, {"Marseille":30}],
    "Nice": [{"Grenoble":293}, {"Aix":174}],
    "Marseille":[{"Aix":30}]
}


def paths(graphe, depart, arrivee, chemin=[]):
    """ 
    Renvoie tous les chemins possibles pour aller de Nice à Lyon
    sans jamais passer deux fois par la même ville.
    """
    chemin = chemin + [depart]
    if depart == arrivee:
        return [chemin]
    if not depart in graphe.keys():
        return []
    chemins = []
    for noeud in graphe[depart]:
        # noeud est ici un dictionnaire à un seul élément
        nouveau_depart = list(noeud.keys())[0]
        if nouveau_depart not in chemin:
            nouveau_chemin = paths(graphe, nouveau_depart, arrivee, chemin)
            for c in nouveau_chemin:
                chemins.append(c)
    return chemins

print(paths(graphe, "Nice", "Lyon"))