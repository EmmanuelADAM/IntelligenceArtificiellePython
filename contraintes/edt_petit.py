from ortools.sat.python import cp_model

PROFS = ["Durand", "Dupont", "Dupond", "Lagaffe"]
SALLES = ["A", "B", "C"]
CRENEAUX = ["8h-10h", "10h-12h", "14h-16h", "16h-18h"]
MATIERES = ["Math", "Physique", "Chimie", "Biologie", "Histoire"]
# matières possibles par professeur (indices consécutifs dans MATIERES)
PEUT = {"Durand": (0, 1), "Dupont": (1, 2), "Dupond": (2, 3), "Lagaffe": (3, 4)}

model = cp_model.CpModel()
salle = {p: model.new_int_var(0, 2, f"salle_{p}") for p in PROFS}
creneau = {p: model.new_int_var(0, 3, f"creneau_{p}") for p in PROFS}
matiere = {p: model.new_int_var(PEUT[p][0], PEUT[p][1], f"matiere_{p}") for p in PROFS}

# c1 : un seul cours par salle et par créneau -> numéro de case 4 * salle + créneau
model.add_all_different(4 * salle[p] + creneau[p] for p in PROFS)
# c2 : matières toutes différentes
model.add_all_different(matiere.values())

solver = cp_model.CpSolver()
statut = solver.solve(model)
print(solver.response_stats())
for p in PROFS:
    print(f"{p:8s}: {MATIERES[solver.value(matiere[p])]:9s} salle {SALLES[solver.value(salle[p])]}, "
          f"{CRENEAUX[solver.value(creneau[p])]}")
