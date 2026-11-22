"""Allocation de canaux Wi-Fi a des bornes - OR-Tools CP-SAT.
Installation : pip install ortools

Deux bornes trop proches (meme piece, pieces voisines, etages superposes) se brouillent
si elles emettent sur le meme canal. On attribue un canal a chaque borne de sorte que
deux bornes en interference n'aient jamais le meme canal : c'est une COLORATION DE GRAPHE
(bornes = sommets, interferences = aretes, canaux = couleurs).

Trois modeles sont proposes :
  - modele_1 : une variable entiere par borne, une contrainte  canal_i != canal_j par interference (relation directe entre deux bornes) ;
  - modele_2 : une variable entiere par borne, recherche de cliques (relations entre groupes de bornes interconnectees) 
  et une contrainte all_different par clique ;
  - modele_3 : une contrainte  canal_i != canal_j par interference (relation directe entre deux bornes) 
  et un modele d'optimisation qui cherche le nombre minimal de canaux.

Usage en tant que librairie
ou pour tester les modeles : python canaux_wifi.py
"""
import random
from ortools.sat.python import cp_model

# les 3 canaux de la bande 2,4 GHz qui ne se recouvrent pas
CANAUX_24GHZ = [1, 6, 11]
# les 8 canaux de 20 MHz des bandes UNII-1 et UNII-2 (5 GHz)
CANAUX_5GHZ = [36, 40, 44, 48, 52, 56, 60, 64]


# ----------------------------------------------------------------------------------
#  Donnees
# ----------------------------------------------------------------------------------
def batiment_b():
    """Le batiment B : 15 bornes sur 3 niveaux.   
    - Return: (nom, bornes, interferences (relations directes entre les bornes))."""
    bornes = ["Hall", "Accueil", "AmphiA", "AmphiB", "Cafet", "Biblio",   # RDC : 0..5
              "TP1", "TP2", "TP3", "TP4", "Bureaux1",                   # 1er : 6..10
              "Direction", "LaboCyber", "OpenSpace", "Reunion"]         # 2e  : 11..14
    interferences = [
        # RDC : la borne du hall central est vue par toutes les bornes du rez-de-chaussee
        (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
        # RDC : les 5 autres bornes forment un anneau autour du hall
        (1, 2), (2, 3), (3, 4), (4, 5), (5, 1),
        # 1er etage : les 4 salles de TP se brouillent toutes entre elles ; TP3 brouille aussi Bureaux1
        (6, 7), (6, 8), (6, 9), (7, 8), (7, 9), (8, 9), (8, 10),
        # 2e etage
        (11, 12), (12, 13), (13, 14), (11, 14),
        # bornes superposees RDC / 1er etage
        (2, 6), (3, 7), (4, 8), (5, 10),
        # bornes superposees 1er / 2e etage
        (6, 12), (7, 13), (10, 11)]
    return "Batiment B", bornes, interferences


def instance_aleatoire(n, densite, graine):
    """Instance aleatoire : chaque borne est reliee a densite % des autres bornes.  
    Meme graine => meme instance à chaque execution.  
    - Return: (nom, bornes, interferences (relations directes entre les bornes))."""
    alea = random.Random(graine)
    bornes = [f"B{i}" for i in range(n)]
    interferences = [(i, j) for i in range(n - 1) for j in range(i + 1, n)
                     if alea.random() < densite]
    return f"Aleatoire n={n} d={densite} graine={graine}", bornes, interferences


# ----------------------------------------------------------------------------------
#  Modele 1 : une contrainte != par interference
# ----------------------------------------------------------------------------------
def modele_1(instance, canaux):
    """modele_1(instance, canaux)
    les bornes de l'instance prennent les valeurs dans un domaine = liste des canaux.  
      *une relation d'interference entre deux bornes est traduite par une contrainte !=.*  
    -param instance = (nom, bornes, relations entre bornes)
    -param canaux = CANAUX_24GHZ(3), CANAUX_5GHZ (8), ou toute liste d'entiers différents.  
    - Return: une affectation des canaux aux bornes de l'instance.
    """
    nom, bornes, interferences = instance
    model = cp_model.CpModel()
    domaine = cp_model.Domain.from_values(canaux)
    canal = [model.new_int_var_from_domain(domaine, f"canal_{b}") for b in bornes]

    for i, j in interferences:
        model.add(canal[i] != canal[j])

    return resoudre(model, canal, instance, "modele 1")


# ----------------------------------------------------------------------------------
#  Modele 2 : contraintes globales all_different sur des cliques
# ----------------------------------------------------------------------------------
def couverture_par_cliques(instance):
    """couverture_par_cliques(instance)  
    Regroupe les aretes, liaisons en cliques maximales (Une **clique** est un sous graphe dont deux sommets quelconques sont toujours adjacents).   
    Approche gloutonne donc le nombre de cliques peut ne pas être le plus petit.
    - param : instance = (nom, bornes, relations entre bornes)
    - Return: liste de cliques (liste de listes des no de bornes inter connectées)
"""
    _, bornes, interferences = instance
    n = len(bornes)
    voisins = [set() for _ in range(n)]
    for i, j in interferences:
        voisins[i].add(j)
        voisins[j].add(i)
    couvertes = set()
    cliques = []
    for i, j in interferences:  
        if (i, j) in couvertes:
            continue
        clique = [i, j]
        for k in range(n):
            if k not in clique and all(k in voisins[c] for c in clique):
                clique.append(k)
        couvertes.update((u, v) for u in clique for v in clique)
        cliques.append(clique)
    return cliques


def modele_2(instance, canaux):
    """modele_2(instance, canaux)
    les bornes de l'instance prennent les valeurs dans un domaine = liste des canaux.  
      *une clique de bornes interconnectées est traduite par une contrainte all_different.*   
    -param instance = (nom, bornes, relations entre bornes)
    -param canaux = CANAUX_24GHZ(3), CANAUX_5GHZ (8), ou toute liste d'entiers différents.  
    - Return: une affectation des canaux aux bornes de l'instance.
    """
    nom, bornes, interferences = instance
    model = cp_model.CpModel()
    domaine = cp_model.Domain.from_values(canaux)
    canal = [model.new_int_var_from_domain(domaine, f"canal_{b}") for b in bornes]

    for clique in couverture_par_cliques(instance):
        model.add_all_different(canal[b] for b in clique)

    return resoudre(model, canal, instance, "modele 2")


# ----------------------------------------------------------------------------------
#  Modele 3 : minimiser le nombre de canaux
# ----------------------------------------------------------------------------------
def modele_3(instance):
    """ modele_3(instance)
        Chaque borne recoit un numero de canal entre 0 et n-1.   
          *une relation d'interference entre deux bornes est traduite par une contrainte !=.*  
          *on cherche a minimiser le plus grand numero de canal utilise.*
        - Return: une affectation des canaux aux bornes de l'instance.
    """
    nom, bornes, interferences = instance
    n = len(bornes)
    model = cp_model.CpModel()
    numero = [model.new_int_var(0, n - 1, f"numero_{b}") for b in bornes]
    for i, j in interferences:
        model.add(numero[i] != numero[j])

    plus_grand = model.new_int_var(0, n - 1, "plus_grand_numero")
    model.add_max_equality(plus_grand, numero)
    model.add(numero[0] == 0)                       # cassage de symetrie
    model.minimize(plus_grand)

    solver = nouveau_solveur()
    statut = solver.solve(model)
    afficher_statistiques(model, solver, statut, "modele 3")
    if statut in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Nombre minimal de canaux :", solver.value(plus_grand) + 1,
              "" if statut == cp_model.OPTIMAL else "(optimalite non prouvee)")
        return [solver.value(v) for v in numero]
    return None


# ----------------------------------------------------------------------------------
#  Outils communs
# ----------------------------------------------------------------------------------
def nouveau_solveur(limite=30):
    """- param limite = temps maximum de recherche en secondes.
    - return: Un solveur reproductible à l'identique avec 1 seul thread"""
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.max_time_in_seconds = limite
    return solver


def afficher_statistiques(model, solver, statut, titre):
    """ affiche titre, nombre de variables et contraintes, statut de la recherche,   
    temps de recherche, nombre de branchements et de conflits."""
    print(f"[{titre}] {len(model.proto.variables)} variables, "
          f"{len(model.proto.constraints)} contraintes -> {solver.status_name(statut)} "
          f"en {solver.wall_time:.3f} s ({solver.num_branches} branchements, "
          f"{solver.num_conflicts} conflits)")


def resoudre(model, canal, instance, titre):
    """Lance la recherche d'une solution, affiche les statistiques et le plan de canaux si possible.  
    - model = modèle OR-Tools;   
    - canal = liste des canaux (canaux = CANAUX_24GHZ(3), CANAUX_5GHZ (8), or any list of integers)   
    - instance=instance du modèle (nom, bornes, leurs relations)  
    - return si possible l'affection des canaux aux bornes (et affichage si <20 bornes), sinon None
    """
    _, bornes, _ = instance
    solver = nouveau_solveur()
    statut = solver.solve(model)
    afficher_statistiques(model, solver, statut, titre)
    if statut == cp_model.INFEASIBLE:
        print("  Aucune solution : il n'y a pas assez de canaux.")
        return None
    if statut == cp_model.UNKNOWN:
        print("  Limite de temps atteinte : on ne sait pas s'il existe une solution.")
        return None
    plan = [solver.value(c) for c in canal]
    if len(bornes) <= 20:
        for b, c in zip(bornes, plan):
            print(f"  {b:<10} -> canal {c}")
    return plan


def verifier(instance, plan):
    """Verifie a posteriori qu'un plan de canaux respecte toutes les interferences, interdictions."""
    _, _, interferences = instance
    return plan is not None and all(plan[i] != plan[j] for (i, j) in interferences)


# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

##si on lance la bibliothèque directement, on teste les 3 modeles sur le batiment B et sur 2 instances aleatoires
if __name__ == "__main__":
    b = batiment_b()
    print(f"===== {b[0]} : {len(b[1])} bornes, {len(b[2])} interferences =====")

    print("\n--- Bande 2,4 GHz (3 canaux) ---")
    modele_1(b, CANAUX_24GHZ)
    modele_2(b, CANAUX_24GHZ)

    print("\n--- 4 canaux de la bande 5 GHz ---")
    plan = modele_1(b, CANAUX_5GHZ[:4])
    print("Plan valide ?", verifier(b, plan))
    modele_2(b, CANAUX_5GHZ[:4])

    print("\n--- Nombre minimal de canaux ---")
    modele_3(b)

    print("\n===== Instances aleatoires =====")
    for (n, d, g, ks) in [(60, 0.15, 42, (4, 5)), (80, 0.2, 1, (5, 6))]:
        inst = instance_aleatoire(n, d, g)
        print(f"\n{inst[0]} : {len(inst[2])} interferences")
        for k in ks:
            print(f"--- {k} canaux ---")
            modele_1(inst, CANAUX_5GHZ[:k])
            modele_2(inst, CANAUX_5GHZ[:k])
