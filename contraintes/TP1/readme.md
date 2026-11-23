# TP OR-Tools : modéliser, comparer, résoudre

Ce livret accompagne le TP de programmation par contraintes avec **OR-Tools** (solveur **CP-SAT** de Google), en Python.
Il ne remplace pas l'énoncé : il vous guide pas à pas, donne des **morceaux de code** pour démarrer,
propose des questions pour vérifier votre compréhension et des **indices progressifs** à ouvrir seulement si vous êtes bloqué·e.

## Ce que vous allez faire

| Partie | Problème | Ce que vous apprenez | Points |
|---|---|---|---|
| [Question 1](q1_planification.md) | Planifier 10 tâches liées par des précédences | Modéliser du temps ; optimiser une date de fin | 3 |
| [Question 2](q2_sudoku.md) | Compléter des grilles de Sudoku lues dans un fichier | Contraintes globales ; détecter l'absence de solution ; soigner un programme utilisable | 5 |
| [Question 3](q3_tectonic.md) | Résoudre le casse-tête Tectonic | Modéliser seul un problème nouveau ; tester l'unicité d'une solution | 6 |
| [Question 4](q4_canaux_wifi.md) | Attribuer des canaux Wi-Fi à 14 bornes sans interférence | Lire et comparer plusieurs modèles d'un même problème ; écrire un modèle booléen | 6 |

## Fichiers fournis

```text
tp-ortools/
├── requirements.txt              ortools
├── canaux_wifi.py                code fourni pour la question 4 (3 modèles)
├── exemple_planification.py      exemple de planification (question 1)
├── MagicSquare-ort.py            exemple du carré magique (question 2)
└── grilles/
    ├── sudoku_cours.txt          grilles de test pour la question 2
    ├── sudoku_facile.txt
    ├── sudoku_difficile.txt
    ├── sudoku_multiple.txt
    ├── sudoku_insoluble.txt
    ├── sudoku_4x4.txt
    ├── tectonic_cours.txt        grilles de test pour la question 3verifier si
    ├── tectonic_petit.txt
    ├── tectonic_moyen.txt
    ├── tectonic_grand.txt
    └── tectonic_insoluble.txt
```

## Comment utiliser ce livret

:::{tip} Les indices
Les blocs repliés **Indice 1**, **Indice 2**… donnent des pistes de plus en plus précises.
Essayez d'abord sans : chercher fait partie de l'apprentissage, et c'est ce qui est évalué.
:::

:::{note} Les questions marquées (R)
Elles appellent une **réponse rédigée** (quelques lignes, un tableau de mesures).
Écrivez-les au fur et à mesure dans votre compte rendu ([voir la page Rendu](rendu.md)).
:::

:::{note} Les morceaux de code
Les blocs de code marqués `# A COMPLETER` sont des squelettes à recopier et compléter.
Les cellules suivies d'un résultat ont été exécutées lors de la construction du livret : vous devez obtenir la même chose chez vous.
:::

Commencez par la page [Prise en main](prise_en_main.md) pour installer OR-Tools et revoir
la structure d'un programme CP-SAT.
