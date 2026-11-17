"""Coloration de zones reseau (niveaux de securite) - version OR-Tools CP-SAT.
Portage de ColorZone.java (Choco-solver).  Installation : pip install ortools

Points cles OR-Tools illustres :
  - un modele (CpModel) et un solveur (CpSolver) separes ;
  - pas de .post() : model.add(...) ajoute directement la contrainte ;
  - enumeration de toutes les solutions : boucle "resoudre, interdire, recommencer".
"""
from ortools.sat.python import cp_model

COULEURS = ["ROUGE", "JAUNE", "VERT", "BLEU"]
ROUGE, JAUNE, VERT, BLEU = range(4)


def color_zones():
    model = cp_model.CpModel()
    zones = {
        "Admin": model.new_int_var(ROUGE, JAUNE, "Admin"),   # rouge ou jaune
        "Data": model.new_int_var(ROUGE, BLEU, "Data"),
        "Web": model.new_int_var(VERT, BLEU, "Web"),         # vert ou bleu
        "Dev": model.new_int_var(ROUGE, BLEU, "Dev"),
        "Test": model.new_int_var(JAUNE, BLEU, "Test"),      # pas de rouge
    }

    # Contraintes : deux zones connectees ont des niveaux differents
    connexions = [("Admin", "Data"), ("Admin", "Dev"), ("Data", "Web"),
                  ("Data", "Dev"), ("Web", "Test"), ("Dev", "Test")]
    for a, b in connexions:
        model.add(zones[a] != zones[b])

    # Toutes les solutions : on resout, on interdit la solution trouvee, on recommence
    solver = cp_model.CpSolver()
    variables = list(zones.values())
    nb = 0
    while solver.solve(model) == cp_model.OPTIMAL:
        solution = [solver.value(v) for v in variables]
        nb += 1
        print(f"Solution {nb} :", {nom: COULEURS[c] for nom, c in zip(zones, solution)})
        model.add_forbidden_assignments(variables, [solution])
    print(nb, "solutions")


def color_zones_petit():
    """4 zones A,B,C,D et 3 niveaux : une seule solution demandee."""
    model = cp_model.CpModel()
    A, B, C, D = [model.new_int_var(1, 3, n) for n in "ABCD"]
    model.add(A != B)
    model.add(A != C)
    model.add(B != C)
    model.add(C != D)
    solver = cp_model.CpSolver()
    if solver.solve(model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print({v.name: solver.value(v) for v in (A, B, C, D)})


if __name__ == "__main__":
    color_zones()
    color_zones_petit()
