"""Grilles de sudoku et affichage, fournis pour la question 3 (rien a coder ici).

    from outils_sudoku import GRILLES, afficher
    grille = GRILLES["cours"]          # liste de 9 listes de 9 entiers, 0 = case vide
    afficher(grille)
"""

# 0 = case vide
GRILLES = {
    # la grille de l'image sudokuARemplir.png : solution unique
    "cours": [
        [0, 3, 0, 7, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 6, 0, 0],
        [8, 0, 0, 0, 1, 3, 0, 0, 5],
        [0, 6, 0, 0, 7, 4, 5, 0, 0],
        [4, 0, 0, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 9, 0, 0, 0],
        [3, 0, 0, 0, 4, 5, 0, 0, 1],
        [0, 8, 0, 0, 0, 0, 0, 3, 0],
    ],
    # 36 indices : solution unique
    "facile": [
        [0, 3, 0, 9, 1, 5, 0, 0, 0],
        [0, 9, 0, 8, 0, 6, 0, 3, 1],
        [0, 0, 0, 0, 0, 0, 5, 6, 9],
        [0, 0, 7, 6, 8, 0, 3, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 5, 4, 3, 0, 9, 1, 6],
        [0, 0, 0, 5, 6, 0, 0, 0, 3],
        [3, 2, 0, 0, 9, 0, 0, 5, 0],
        [4, 5, 0, 3, 2, 0, 1, 0, 0],
    ],
    # 23 indices : solution unique
    "difficile": [
        [0, 9, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 3, 0, 0, 0],
        [0, 0, 2, 9, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 1, 0, 2, 5],
        [4, 0, 0, 0, 0, 0, 0, 9, 7],
        [0, 0, 8, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 0, 1, 0, 3, 0, 0],
        [9, 0, 0, 0, 2, 0, 0, 6, 0],
        [0, 5, 0, 0, 7, 0, 0, 0, 8],
    ],
    # grille mal posee : plusieurs solutions
    "multiple": [
        [0, 3, 0, 9, 1, 5, 0, 0, 0],
        [0, 9, 0, 0, 0, 6, 0, 3, 1],
        [0, 0, 0, 0, 0, 0, 5, 6, 0],
        [0, 0, 7, 6, 0, 0, 3, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 5, 4, 3, 0, 9, 0, 6],
        [0, 0, 0, 5, 6, 0, 0, 0, 3],
        [3, 2, 0, 0, 9, 0, 0, 5, 0],
        [4, 5, 0, 3, 2, 0, 1, 0, 0],
    ],
    # aucune solution, sans doublon visible
    "insoluble": [
        [1, 9, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 3, 0, 0, 0],
        [0, 0, 2, 9, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 1, 0, 2, 5],
        [4, 0, 0, 0, 0, 0, 0, 9, 7],
        [0, 0, 8, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 0, 1, 0, 3, 0, 0],
        [9, 0, 0, 0, 2, 0, 0, 6, 0],
        [0, 5, 0, 0, 7, 0, 0, 0, 8],
    ],
}


def afficher(grille, depart=None):
    """Affiche une grille 9x9 ; 0 est affiche par un point.
    Si depart (la grille initiale) est donnee, les chiffres trouves par le solveur sont entre crochets."""
    for i in range(9):
        if i % 3 == 0:
            print("+---------+---------+---------+")
        ligne = ""
        for j in range(9):
            if j % 3 == 0:
                ligne += "|"
            v = grille[i][j]
            if v == 0:
                ligne += " . "
            elif depart is not None and depart[i][j] == 0:
                ligne += f"[{v}]"
            else:
                ligne += f" {v} "
        print(ligne + "|")
    print("+---------+---------+---------+")
