"""Rendu de monnaie (TD1, exercice 4) - version OR-Tools CP-SAT.
Portage du modele Choco du cours.

COP : minimiser le nombre de pieces sous la contrainte somme(n_v * v) = S.
Bonus : avec les pieces {1, 3, 4}, le glouton n'est pas optimal pour S = 6.
"""
from ortools.sat.python import cp_model


def rendu(valeurs, S):
    model = cp_model.CpModel()
    n = [model.new_int_var(0, S // v, f"n{v}") for v in valeurs]
    model.add(sum(n[i] * valeurs[i] for i in range(len(valeurs))) == S)
    model.minimize(sum(n))
    solver = cp_model.CpSolver()
    statut = solver.solve(model)
    if statut != cp_model.OPTIMAL:
        return None
    return {v: solver.value(n[i]) for i, v in enumerate(valeurs) if solver.value(n[i]) > 0}


def glouton(valeurs, S):
    resultat = {}
    for v in sorted(valeurs, reverse=True):
        if S >= v:
            resultat[v], S = S // v, S % v
    return resultat


if __name__ == "__main__":
    for valeurs, S in (([1, 5, 10, 20, 50, 100, 200], 78), ([1, 3, 4], 6)):
        opt, glo = rendu(valeurs, S), glouton(valeurs, S)
        print(f"pieces {valeurs}, somme {S}")
        print(f"  CP-SAT  : {opt} -> {sum(opt.values())} pieces")
        print(f"  glouton : {glo} -> {sum(glo.values())} pieces")
