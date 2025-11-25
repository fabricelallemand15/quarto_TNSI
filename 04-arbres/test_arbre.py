class Noeud:
    def __init__(self, etiquette, gauche=None, droit=None):
        """
        Crée un nouveau noeud.
        :param etiquette: La valeur stockée dans le noeud.
        :param gauche: Le sous-arbre gauche (instance de Noeud ou None).
        :param droit: Le sous-arbre droit (instance de Noeud ou None).
        """
        self.etiquette = etiquette
        self.gauche = gauche
        self.droit = droit

    def est_feuille(self) -> bool:
        """Renvoie True si le noeud est une feuille."""
        return self.gauche is None and self.droit is None

    def __repr__(self):
        """Représentation textuelle pour le débogage."""
        return f"Noeud({self.etiquette})"


def taille(arbre) -> int:
    """
    Calcule la taille de l'arbre (nombre total de noeuds).
    """
    if arbre is None:
        return 0
    else:
        return 1 + taille(arbre.gauche) + taille(arbre.droit)

def hauteur(arbre) -> int:
    """
    Calcule la hauteur de l'arbre.
    Convention : Hauteur(vide) = 0, Hauteur(feuille) = 1.
    """
    if arbre is None:
        return 0
    else:
        return 1 + max(hauteur(arbre.gauche), hauteur(arbre.droit))


def affiche(arbre, niveau=0, prefixe="Racine: "):
    """Affiche l'arbre dans la console de manière textuelle."""
    if arbre is None:
        return
    
    # On affiche d'abord le sous-arbre droit (pour qu'il soit en haut)
    affiche(arbre.droit, niveau + 1, " /-- ")
    
    # On affiche le noeud courant
    print("    " * niveau + prefixe + str(self.etiquette))
    
    # On affiche le sous-arbre gauche
    affiche(arbre.gauche, niveau + 1, " \\-- ")

def insere_abr(arbre, valeur):
    """
    Insère une valeur dans un ABR et renvoie la nouvelle racine.
    Si l'arbre est vide, crée un nouveau noeud.
    """
    if arbre is None:
        return Noeud(valeur)
    
    if valeur < arbre.etiquette:
        arbre.gauche = insere_abr(arbre.gauche, valeur)
    elif valeur > arbre.etiquette:
        arbre.droit = insere_abr(arbre.droit, valeur)
    # Si valeur == arbre.etiquette, on ne fait rien (pas de doublons)
    
    return arbre


abr = None
abr = insere_abr(abr, 10)
abr = insere_abr(abr, 5)
abr = insere_abr(abr, 15)
abr = insere_abr(abr, 2)