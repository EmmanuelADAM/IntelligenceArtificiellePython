"""Zebra puzzle (des slides) - version OR-Tools CP-SAT.

Modele : 
une variable par VALEUR de chaque categorie, 
son domaine est la position de la maison (0 a 4). 
Voisinage : |a - b| = 1 s'ecrit avec add_abs_equality.
"""
from ortools.sat.python import cp_model

#on défini les categories et leurs valeurs en chaine de caracteres
CATEGORIES = {
    "couleur": ["Bleue", "Blanche", "Rouge", "Verte", "Jaune"],
    "nationalite": ["Britannique", "Suedoise", "Francaise", "Espagnole", "Italienne"],
    "animal": ["Chien", "Chat", "Gerbille", "Perruche", "Zebre"],
    "boisson": ["Cafe", "The", "Sirop", "Soda", "Eau"],
    "serie": ["PeakyBlinders", "Fargo", "Crown", "HouseOfCards", "LeParlement"],
}

#creation du modele
model = cp_model.CpModel()
#on crée une variable pour chaque valeur de chaque categorie,
# son domaine est la position de la maison (0 a 4) 
pos = {}                                   # pos["Rouge"] = position de la maison rouge
for categorie, valeurs in CATEGORIES.items():
    for v in valeurs:
        pos[v] = model.new_int_var(0, 4, v)
    # les valeurs d'une meme categorie sont toutes differentes
    # une seule maison par couleur, par nationalite, par animal, ...
    model.add_all_different(pos[v] for v in valeurs)

# on definit une fonction pour les contraintes de voisinage
# dans le puzzle, certaines maisons sont cote a cote
def voisins(a, b):
    """les maisons de a et b sont cote a cote : |pos[a] - pos[b]| = 1"""
    model.add_abs_equality(1, pos[a] - pos[b])

# on ajoute les contraintes du puzzle
model.add(pos["Britannique"] == pos["Rouge"])        # 1
model.add(pos["Suedoise"] == pos["Chien"])           # 2
model.add(pos["Cafe"] == pos["Verte"])               # 3
model.add(pos["Francaise"] == pos["The"])            # 4
model.add(pos["Verte"] == pos["Blanche"] + 1)        # 5 : verte juste a droite de blanche
model.add(pos["PeakyBlinders"] == pos["Chat"])       # 6
model.add(pos["Fargo"] == pos["Jaune"])              # 7
model.add(pos["Sirop"] == 2)                         # 8 : maison du centre
model.add(pos["Espagnole"] == 0)                     # 9 : premiere maison
voisins("Crown", "Gerbille")                         # 10
voisins("Fargo", "Perruche")                         # 11
model.add(pos["HouseOfCards"] == pos["Soda"])        # 12
model.add(pos["Italienne"] == pos["LeParlement"])    # 13
voisins("Espagnole", "Bleue")                        # 14

# on résout le modele
solver = cp_model.CpSolver()

statut = solver.solve(model)

print(solver.status_name(statut))

if statut in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    # on retourne le resultat : solution[categorie][maison] = valeur placee la
    solution = {}
    for categorie, valeurs in CATEGORIES.items():
        solution[categorie] = [""] * 5
        for v in valeurs:
            maison = solver.value(pos[v])
            solution[categorie][maison] = v

    # affichage en tableau, une colonne par maison
    print(f"{'':12s}" + "".join(f"{'Maison ' + str(m + 1):>15s}" for m in range(5)))
    for categorie, par_maison in solution.items():
        print(f"{categorie:12s}" + "".join(f"{v:>15s}" for v in par_maison))

    # les deux questions se lisent alors directement dans le tableau
    print("Le zebre appartient a", solution["nationalite"][solver.value(pos["Zebre"])])
    print("L'eau est bue par", solution["nationalite"][solver.value(pos["Eau"])])