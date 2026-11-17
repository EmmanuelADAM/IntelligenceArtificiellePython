from ortools.sat.python import cp_model

def carre_magique(n=3):
    model = cp_model.CpModel()
    # variables : une par case, un entier dans le domaine [1, n*n]
    cases = [model.new_int_var(1, n * n, f"case_{i}_{j}") for i in range(n) for j in range(n)]
    # contraintes : toutes les cases sont differentes
    model.add_all_different(cases)
    # contraintes : somme des lignes, colonnes et diagonales
    somme = n * (n * n + 1) // 2
    for i in range(n):
        model.add(sum(cases[i * n + j] for j in range(n)) == somme)  # lignes
        model.add(sum(cases[j * n + i] for j in range(n)) == somme)  # colonnes
    model.add(sum(cases[i * n + i] for i in range(n)) == somme)      # diagonale principale
    model.add(sum(cases[i * n + (n - 1 - i)] for i in range(n)) == somme)  # diagonale secondaire

    solver = cp_model.CpSolver()
    statut = solver.solve(model)
    if statut in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Solution:")
        for i in range(n):
            print([solver.value(cases[i * n + j]) for j in range(n)])
        #temps de calcul
        print(solver.response_stats())

carre_magique(10)
