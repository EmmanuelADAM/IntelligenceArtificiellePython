# Prise en main

## Installer OR-Tools

```bash
pip install ortools
python canaux_wifi.py                # vérifie que tout fonctionne
```

Vous pouvez travailler dans l'IDE de votre choix (PyCharm, VS Code) ou dans un carnet Jupyter.

:::{warning} Répertoire de travail
Les chemins `grilles/...` sont relatifs au dossier `TP1`.   
Lancez vos programmes depuis ce dossier (dans PyCharm : *Working directory* de la configuration d'exécution).
:::

## Les quatre étapes d'un programme CP-SAT

Tous les programmes du TP suivent le même schéma.   
Voici le petit exemple de coloration de zones réseau vu en cours (`ColorZone-ort.py`) : 
- quatre zones A, B, C, D, trois niveaux de sécurité, deux zones connectées doivent avoir des niveaux différents.

```{code-cell} ipython3
from ortools.sat.python import cp_model

# 1. un modèle
model = cp_model.CpModel()

# 2. des variables et leurs domaines
A, B, C, D = [model.new_int_var(1, 3, nom) for nom in "ABCD"]

# 3. des contraintes (pas de .post() : model.add suffit)
model.add(A != B)
model.add(A != C)
model.add(B != C)
model.add(C != D)

# 4. une résolution
solver = cp_model.CpSolver()
statut = solver.solve(model)
print(solver.status_name(statut))
if statut in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print({v.name: solver.value(v) for v in (A, B, C, D)})
```

Le **statut** renvoyé par `solver.solve` est l'information la plus importante :

| Statut | Signification |
|---|---|
| `OPTIMAL` | une solution a été trouvée (et, s'il y a un objectif, elle est optimale) |
| `FEASIBLE` | une solution a été trouvée, mais son optimalité n'est pas prouvée (limite de temps atteinte) |
| `INFEASIBLE` | il est **prouvé** qu'aucune solution n'existe |
| `UNKNOWN` | la limite de temps est atteinte avant toute conclusion |
| `MODEL_INVALID` | le modèle est mal construit (domaine vide, contrainte incorrecte…) |

## Quelques variables utiles

```{code-cell} ipython3
model = cp_model.CpModel()
# x dans [1, 9]
x = model.new_int_var(1, 9, "x")
# c dans {1, 6, 11}
c = model.new_int_var_from_domain(cp_model.Domain.from_values([1, 6, 11]), "c")
# b dans {0, 1}
b = model.new_bool_var("b")
# une liste de 5 variables
t = [model.new_int_var(0, 10, f"t_{i}") for i in range(5)]
print(model.model_stats())
```

Les contraintes s'écrivent comme des expressions Python :

```python
model.add(x != c)                # différence
model.add(t[1] >= t[0] + 3)      # t[1] commence au moins 3 après t[0]
model.add(sum(t) <= 20)          # somme
model.add_all_different(t)       # toutes différentes (globale)
model.add_max_equality(m, t)     # m = max(t)
model.minimize(m)                # objectif
```

## Mesurer l'effort du solveur

Pour comparer des modèles (question 1), vous aurez besoin de mesures :

| Mesure | Code | Ce qu'elle indique |
|---|---|---|
| Taille du modèle | `len(model.proto.variables)`, `len(model.proto.constraints)` | nombre de variables et de contraintes |
| Branchements | `solver.num_branches` | nombre de choix faits pendant la recherche |
| Conflits | `solver.num_conflicts` | nombre d'impasses rencontrées |
| Temps | `solver.wall_time` | secondes passées à résoudre |
| Tout d'un coup | `print(solver.response_stats())` | une synthèse complète |

```{code-cell} ipython3
model = cp_model.CpModel()
# les 8 reines, version all_different
q = [model.new_int_var(0, 7, f"Q_{i}") for i in range(8)]
model.add_all_different(q)
model.add_all_different(q[i] + i for i in range(8))
model.add_all_different(q[i] - i for i in range(8))

solver = cp_model.CpSolver()
solver.parameters.num_workers = 1   # mesures reproductibles
statut = solver.solve(model)
print(f"{len(model.proto.variables)} variables, {len(model.proto.constraints)} contraintes")
print(f"{solver.status_name(statut)} en {solver.wall_time:.3f} s "
      f"({solver.num_branches} branchements, {solver.num_conflicts} conflits)")
print([solver.value(v) for v in q])
```

:::{admonition} Deux réglages importants pour comparer des modèles
:class: important
- Par défaut, CP-SAT lance **plusieurs stratégies en parallèle** :   
les statistiques changent d'une exécution à l'autre.  
Fixez `solver.parameters.num_workers = 1` pour des mesures reproductibles.
- Avant de chercher, CP-SAT **simplifie** le modèle (la *présolution*) et résout parfois tout à ce stade, avec 0 branchement.   
Pour observer la recherche elle-même, désactivez-la : `solver.parameters.cp_model_presolve = False`.
:::

## Limiter le temps, énumérer des solutions

```python
solver.parameters.max_time_in_seconds = 30     # à régler avant solver.solve(model)
```

Pour savoir si une solution est **unique**, on utilise la technique du cours (`ColorZone-ort.py`) :
on résout, on **interdit** la solution trouvée, on recommence.

```python
variables = [...]          # toutes les variables de décision
solutions = []
while len(solutions) < 2 and solver.solve(model) in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    sol = [solver.value(v) for v in variables]
    solutions.append(sol)
    model.add_forbidden_assignments(variables, [sol])   # interdit cette solution
# 0 solution : insoluble ; 1 : solution unique ; 2 : plusieurs solutions
```

Si tout fonctionne, passez à la [question 1](q1_canaux_wifi.ipynb).
