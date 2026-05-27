## Coloration de graphes
 
La coloration de graphe a plusieurs applications concrètes :
- Ordonnancement et planification : chaque couleur représente un créneau horaire ou une ressource (ex. : machines, salles). Deux tâches en conflit (liées par une arête) ne peuvent pas avoir la même couleur.
- Allocation de fréquences : dans les réseaux mobiles (4G/5G), chaque station de base (antenne) se voit attribuer une fréquence (couleur). Deux stations proches (liées par une arête) ne peuvent pas utiliser la même fréquence pour éviter les interférences.
- Parallélisation de code : Identification de tâches indépendantes (même couleur) pour les exécuter en parallèle sur des cœurs CPU/GPU.
- Planification de mouvements : pour des drones, éviter les collisions en attribuant des trajectoires (couleurs) non conflictuelles.
- ...

Dans un carte plane, 4 couleurs suffisent pour colorier les zones sans que deux zones contigües aient la même valeur.
 

**Définition des variables**

Une zone z possède une couleur c, posons donc $x_{zc}$.

Pour un problème de 10 zones, il y aura donc 40 variables : $x_{13}$ pour le fait que la zone 1 possède la couleur 4, $\neg x_{30}$ pour le fait que la zone 3 n'est pas en couleur 0. 

On suppose les zones numérotées de 0 à 9, et les couleurs de 0 à 3.

On peut poser k=4 puis utiliser cette fonction

```
def x(r, c, k=4):
    return r * k + c + 1
```
ainsi x(1,3) donne 8.


**Définir les fonctions suivantes :**

1. ```def au_moins_une_couleur(model):```
Ajoute dans le modèle le fait que dans chaque région r, on ait $(x_{r0} \vee x_{r1} \vee \dots \vee x_{r3} )$ 
 
2. ```def au_plus_une_couleur(model)```
Ajoute dans le modèle le fait que dans chaque région r, on ne peut avoir deux couleurs, par exemple on ne peut avoir 0 et 1 : $\neg (x_{r0} \wedge x_{r1}) =  (\neg x_{r0} \vee \neg x_{r1})$ 

De même on ne peut avoir 0 et 2, .. 1 et 2,  .... 2 et 3.

Les adjacences sont définies par une liste de tuples. Exemple : ```adjacences = [ (0,1),(0,2),(2,7)]``` pour signifier que les régions 0 et 1 sont adjacentes, ainsi que 0 et 2, et 2 et 7.

3. ```def contraintes_adjacences(model, adjacences)```
Ajoute dans le modèle le fait que deux régions adjacentes ne peuvent avoir la même couleur c: $\neg (x_{r1c} \wedge x_{r2c}) =  (\neg x_{r1k} \vee \neg x_{r2k})$ 

**Tester le modèle**

Voici les régions de France Métropolitaine, leurs relations et les 4 couleurs : 

```
REGIONS = [
    "Hauts-de-France", "Normandie", "Île-de-France", "Grand Est",
    "Bretagne", "Pays de la Loire", "Centre-Val de Loire",
    "Bourgogne-Franche-Comté", "Nouvelle-Aquitaine",
    "Auvergne-Rhône-Alpes", "Occitanie", "PACA"
]

ADJACENCES = [
    (0,1),(0,2),(0,3),(1,2),(1,4),(1,5),(2,3),(2,6),(2,7),
    (3,7),(4,5),(5,6),(5,8),(6,7),(6,8),(6,9),(6,10),(7,9),
    (8,9),(8,10),(9,10),(9,11),(10,11)
]

COULEURS = ["Rouge", "Vert", "Bleu", "Jaune"]
```

- Implémenter les clauses, 
- Donnez le nb de clauses, 
- lancer  la résolution
```m =build_sudoku_solver()
if m.solve():m.get_model()
```
- et afficher la solution proprement.
 
 