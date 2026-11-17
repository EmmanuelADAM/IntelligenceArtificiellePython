"""Carre magique n x n - version OR-Tools CP-SAT.
Portage de MagicSquare.java (Choco-solver).

Usage : python MagicSquare-ort.py [n] [log]
  le 2e argument (optionnel) affiche, si =True, le journal de recherche de CP-SAT.
En Choco on teste des strategies de recherche ; ici il n'y a rien a regler :
on observe seulement le temps et le journal.
"""
import sys
from ortools.sat.python import cp_model


def carre_magique(n, journal=False):
    model = cp_model.CpModel()
    # les variables sont les cases du carre magique, contenues entre 1 et n*n
    c = [[model.new_int_var(1, n * n, f"c{i}.{j}") for j in range(n)] for i in range(n)]
    # la somme des lignes, colonnes et diagonales doit etre egale a but
    # en carre magique, but = n * (n * n + 1) / 2  ( 15 pour n=3, 34 pour n=4, ..., 260 pour n=8, ...)
    but = n * (n * n + 1) // 2
    print("but =", but)

    # contraintes
    # unicite des valeurs
    model.add_all_different(v for ligne in c for v in ligne) 
    # contraintes de sommes
    for i in range(n):
        model.add(sum(c[i]) == but)                                # lignes
        model.add(sum(c[k][i] for k in range(n)) == but)           # colonnes
    model.add(sum(c[i][i] for i in range(n)) == but)               # diagonale 1
    model.add(sum(c[i][n - 1 - i] for i in range(n)) == but)        # diagonale 2

    # resolution
    solver = cp_model.CpSolver()
    # limite de temps (en secondes)
    solver.parameters.max_time_in_seconds = 60
    
    # journal de recherche (journal = True) ou pas (journal = False)
    solver.parameters.log_search_progress = journal
    if journal:
        solver.parameters.log_to_stdout = False   # évite le doublon dans un terminal
        solver.log_callback = print               # le journal passe par print()

    statut = solver.solve(model)
    print(f"{solver.status_name(statut)} en {solver.wall_time:.2f} s "
          f"({solver.num_branches} branchements, {solver.num_conflicts} conflits)")
    
    if statut in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for ligne in c:
            print(" ".join(f"{solver.value(v):3d}" for v in ligne))


carre_magique(10, True)