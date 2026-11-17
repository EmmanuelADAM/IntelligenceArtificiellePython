from ortools.sat.python import cp_model

COULEURS = [ "BLEU","JAUNE", "ROUGE", "VERT"]
BLEU, JAUNE, ROUGE, VERT  = (0, 1, 2, 3)

model = cp_model.CpModel()

# dictionnaire des variables
zones = {
	"Admin": model.new_int_var(JAUNE, ROUGE,  "Admin"),  "Data":  model.new_int_var(BLEU, ROUGE,  "Data"),
	"Web":   model.new_int_var(BLEU, VERT,  "Web"),    "Dev":   model.new_int_var(BLEU, ROUGE,  "Dev"),
	"Test":  model.new_int_var(BLEU, JAUNE, "Test"),   
}

#les contraintes
connexions = [("Admin", "Data"), ("Admin", "Dev"), ("Data", "Web"), 
              ("Data", "Dev"), ("Web", "Test"), ("Dev", "Test")]
#on utilise les noms des variables pour les contraintes
for a, b in connexions: model.add(zones[a] != zones[b])

solver = cp_model.CpSolver()

variables = list(zones.values())

#--------- resolution et affichage des solutions ---------
#v1. à chaque solution trouvée, 
# on interdit cette affectation pour la prochaine itération
nb = 0
#tant que le solveur trouve une solution, 
while solver.solve(model) == cp_model.OPTIMAL:
	nb += 1
	#récupérer les valeurs de la solution et l'afficher
	solution = [solver.value(v) for v in variables]
	print({nom: COULEURS[c] for nom, c in zip(zones, solution)})
	# interdire cette affectation pour la prochaine itération
	model.add_forbidden_assignments(variables, [solution])   

print(nb, "solutions")

#v2. autre manière : 
# on peut demander au solveur d'énumérer toutes les solutions
#
# solver.parameters.enumerate_all_solutions = True
#
# afficheur = cp_model.VarArraySolutionPrinter(variables)
#
# solver.solve(model, afficheur)
#
# print(afficheur.solution_count, "solutions")
