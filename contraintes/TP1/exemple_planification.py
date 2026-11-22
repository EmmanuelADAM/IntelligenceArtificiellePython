"""Exemple de planification de taches - OR-Tools CP-SAT.
Portage de ProductionScheduling.java (planifTacheTD2_1 et planifTacheTD).

6 taches (numerotees 0 a 5), de durees 1, 1, 2, 1, 2, 1.
Precedences : 5 apres 0 et 4 ; 3 apres 1 et 2 ; 4 apres 3.
"""
from ortools.sat.python import cp_model


def planif_simple():
    """Version 'a la main' : une variable de debut par tache, une contrainte par precedence,
    et une echeance : la tache 5 doit commencer au plus tard a t=9."""
    model = cp_model.CpModel()
    d = [model.new_int_var(0, 12, f"d{i + 1}") for i in range(6)]

    # contraintes de precedence : debut(apres) >= debut(avant) + duree(avant)
    model.add(d[5] >= d[0] + 1)
    model.add(d[5] >= d[4] + 2)
    model.add(d[4] >= d[3] + 1)
    model.add(d[3] >= d[1] + 1)
    model.add(d[3] >= d[2] + 2)
    model.add(d[5] <= 9)

    solver = cp_model.CpSolver()
    if solver.solve(model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Une solution :", {v.name: solver.value(v) for v in d})
    else:
        print("pas de solution avec ces contraintes !!")


def planif_optimale():
    """Version avec tableaux et minimisation de la date de fin."""
    model = cp_model.CpModel()
    nb_taches = 6
    temps_max = 12
    duree = [1, 1, 2, 1, 2, 1]
    # (avant, apres) : 'apres' ne commence qu'une fois 'avant' terminee
    precedences = [(0, 5), (1, 3), (2, 3), (3, 4), (4, 5)]

    debut = [model.new_int_var(0, temps_max, f"debut_{t}") for t in range(nb_taches)]
    for avant, apres in precedences:
        model.add(debut[apres] >= debut[avant] + duree[avant])

    fin = model.new_int_var(0, temps_max, "fin")
    model.add(fin == debut[5] + duree[5])      # la tache 5 est la derniere
    model.minimize(fin)

    solver = cp_model.CpSolver()
    statut = solver.solve(model)
    if statut == cp_model.OPTIMAL:
        print("Fin au plus tot :", solver.value(fin))
        for t in range(nb_taches):
            print(f"  tache {t} : debut {solver.value(debut[t])}, fin {solver.value(debut[t]) + duree[t]}")
    else:
        print("pas de solution :", solver.status_name(statut))


if __name__ == "__main__":
    planif_simple()
    planif_optimale()
