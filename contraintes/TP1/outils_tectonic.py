"""Lecture et affichage des grilles de Tectonic, fournis pour la question 4 (rien a coder ici).

    from outils_tectonic import FICHIERS, lire_tectonic, cases_par_region, afficher
    regions, indices = lire_tectonic("grilles/tectonic_petit.txt")
    cases = cases_par_region(regions)      # lettre de region -> liste des cases (i, j)
    afficher(regions, indices)

Format des fichiers : la carte des regions (une lettre par region), une ligne '---', puis les indices
('.' pour une case vide). Les lignes commencant par '#' sont des commentaires.
"""
from collections import defaultdict

# les grilles fournies (dossier grilles/)
FICHIERS = {
    "petit": "grilles/tectonic_petit.txt",        # 5 x 4, solution unique
    "cours": "grilles/tectonic_cours.txt",        # 11 x 5, solution unique (image TecToNic.png)
    "moyen": "grilles/tectonic_moyen.txt",        # 6 x 6, 4 indices seulement, solution unique
    "grand": "grilles/tectonic_grand.txt",        # 8 x 6, solution unique
    "insoluble": "grilles/tectonic_insoluble.txt",  # 6 x 6, aucune solution
}

FONDS = ["\033[41m", "\033[42m", "\033[43m", "\033[44m", "\033[45m", "\033[46m", "\033[47m"]
NORMAL = "\033[0m"


def lire_tectonic(nom_fichier):
    """Renvoie (regions, indices) :
    - regions : liste de chaines, une lettre par case (la meme lettre pour toutes les cases d'une region) ;
    - indices : liste de listes d'entiers, 0 pour une case vide."""
    with open(nom_fichier, encoding="utf-8") as f:
        lignes = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
    sep = lignes.index("---")
    regions = lignes[:sep]
    indices = [[0 if c == "." else int(c) for c in ligne] for ligne in lignes[sep + 1:]]
    return regions, indices


def cases_par_region(regions):
    """Renvoie un dictionnaire : lettre de region -> liste des cases (i, j) de cette region."""
    cases = defaultdict(list)
    for i, ligne in enumerate(regions):
        for j, lettre in enumerate(ligne):
            cases[lettre].append((i, j))
    return dict(cases)


def afficher(regions, grille):
    """Affiche la grille, chaque region sur une couleur de fond ; '.' pour une case vide."""
    lettres = sorted({c for ligne in regions for c in ligne})
    for i, ligne in enumerate(regions):
        s = ""
        for j, lettre in enumerate(ligne):
            fond = FONDS[lettres.index(lettre) % len(FONDS)]
            v = str(grille[i][j]) if grille[i][j] else "."
            s += f"{fond}\033[30m {v} {NORMAL}"
        print(s + "   " + ligne)
