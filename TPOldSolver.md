# TP (Old) Solvers

(TP basé sur le cours [logique : calcul propositionnel](./logiquesCalculPropositionnel.pdf))

## DP (Davis et Putman)
- reprenez le [code fourni](./DavisPutman.py) et optimisez le selon votre choix pour tenter d'accélérer la résolution. C'est à dire que vous tenterez d'organiser les choix lorsque plusieurs sont possibles à l'activation d'une règle.
- appliquez votre algorithme sur les exemples existants dans le code


## DPLL (Davis et Putman)
- à partir du pseudo-code présenté dans le cours, implémentez l'algorithme de DPLL et optimisez le selon votre choix pour tenter d'accélérer la résolution. C'est à dire que vous tenterez d'organiser les choix lorsque plusieurs sont possibles à l'activation d'une règle.
- appliquez votre algorithme sur les exemples existants dans le code précédent


## Tests
Testez vos algorithmes sur 3 fichiers issus de [uf50](./uf50.zip) (10 énoncés de 50 variables et +- 200 clauses, chaque énoncé est satisfiable), et de [uuf50](./uuf50.zip) (10 énoncés de 50 variables et +- 200 clauses, chaque énoncé est insatisfiable.
Testez avec [uuf150](./uuf150-01.cnf) (énoncé de 150 variables sur 645 clauses).
Ces exemples sont issus de [www.cs.ubc.ca/~hoos/SATLIB/benchm.html](https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html)

## A rendre
- Les codes, commentés en indiquant les idées d'optimisations
- Les tests (avec le nombre d'appels aux algorithmes, et temps de résolution)
