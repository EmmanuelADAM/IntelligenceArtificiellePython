# Aide-mémoire OR-Tools CP-SAT

```python
from ortools.sat.python import cp_model
model = cp_model.CpModel()
solver = cp_model.CpSolver()
```

## Variables

| Besoin | Code |
|---|---|
| Entier dans un intervalle | `model.new_int_var(1, 9, "x")` |
| Entier dans une liste de valeurs | `model.new_int_var_from_domain(cp_model.Domain.from_values([1, 6, 11]), "c")` |
| Booléen (0/1) | `model.new_bool_var("b")` |
| Liste de variables | `[model.new_int_var(0, 10, f"t_{i}") for i in range(n)]` |
| Matrice de booléens | `[[model.new_bool_var(f"x_{i}_{j}") for j in range(k)] for i in range(n)]` |
| Intervalle de durée fixe | `model.new_fixed_size_interval_var(debut, duree, "tache")` |

## Contraintes

| Besoin | Code |
|---|---|
| Comparer | `model.add(x != y)` (`==`, `!=`, `<`, `<=`, `>`, `>=`) |
| Expression linéaire | `model.add(y >= x + 3)`, `model.add(x + y <= 1)`, `model.add(sum(t) == 10)` |
| Toutes différentes | `model.add_all_different(liste)` |
| Maximum | `model.add_max_equality(m, liste)` |
| Exactement / au plus un booléen vrai | `model.add_exactly_one(booleens)`, `model.add_at_most_one(booleens)` |
| Contrainte conditionnelle | `model.add(x == c).only_enforce_if(b)` |
| Interdire une affectation | `model.add_forbidden_assignments(variables, [valeurs])` |
| Ressource partagée | `model.add_cumulative(intervalles, hauteurs, capacite)` |

## Résolution

| Besoin | Code |
|---|---|
| Résoudre | `statut = solver.solve(model)` |
| Solution trouvée ? | `statut in (cp_model.OPTIMAL, cp_model.FEASIBLE)` |
| Impossibilité prouvée ? | `statut == cp_model.INFEASIBLE` |
| Nom du statut | `solver.status_name(statut)` |
| Valeur d'une variable | `solver.value(x)` |
| Optimiser | `model.minimize(expr)` ou `model.maximize(expr)`, avant `solve` |
| Limiter le temps | `solver.parameters.max_time_in_seconds = 30` |
| Un seul fil (mesures reproductibles) | `solver.parameters.num_workers = 1` |
| Sans présolution | `solver.parameters.cp_model_presolve = False` |
| Journal de recherche | `solver.parameters.log_search_progress = True` |

## Statistiques

| Mesure | Code |
|---|---|
| Taille du modèle | `len(model.proto.variables)`, `len(model.proto.constraints)` |
| Effort de recherche | `solver.num_branches`, `solver.num_conflicts`, `solver.wall_time` |
| Synthèse | `print(solver.response_stats())`, `print(model.model_stats())` |

## Erreurs fréquentes

:::{list-table}
:header-rows: 1

* - Symptôme
  - Cause probable
* - `solver.value(x)` renvoie une valeur sans signification
  - lecture alors que le statut n'est ni `OPTIMAL` ni `FEASIBLE`
* - Une exception en écrivant une contrainte
  - `and`, `or`, `not` ou `if` Python sur des variables du modèle : utilisez `only_enforce_if`, `add_bool_or`…
* - Les statistiques changent à chaque exécution
  - plusieurs fils d'exécution : `solver.parameters.num_workers = 1`
* - 0 branchement alors que le problème semble difficile
  - la présolution a tout résolu : désactivez-la pour observer la recherche
* - `FileNotFoundError` sur `grilles/...`
  - le répertoire de travail n'est pas le dossier `tp-ortools`
:::

Documentation officielle : [developers.google.com/optimization](https://developers.google.com/optimization/cp/cp_solver).
