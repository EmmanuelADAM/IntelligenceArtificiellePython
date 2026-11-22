"""Outil de visualisation d'un plan de canaux pour le batiment B (question 1).

    from outils_visu import dessiner_plan
    dessiner_plan([36, 40, 44, ...])     # un canal par borne, dans l'ordre de batiment_b()
    Généré par l'IA Claude (https://claude.ai) à partir du code de jp-book-tp-ortools (EA), le 2024-06-19.
"""
import math
import matplotlib.pyplot as plt
import networkx as nx
from canaux_wifi import batiment_b

# positions des bornes sur le dessin
POS = {0: (0, 0)}
for k, i in enumerate([1, 2, 3, 4, 5]):
    a = math.pi - 2 * math.pi * k / 5
    POS[i] = (1.5 * math.cos(a), 1.5 * math.sin(a))
POS.update({6: (3.8, 2.0), 7: (5.3, 1.3), 8: (3.8, 0.0), 9: (5.3, -0.5), 10: (3.8, -1.6),
            11: (7.6, -1.6), 12: (7.6, 2.0), 13: (8.9, 0.6), 14: (8.9, -1.6)})


def dessiner_plan(plan, titre="Plan de canaux"):
    """Dessine le graphe du batiment B colore selon le plan ; les interferences violees sont en rouge."""
    _, bornes, interferences = batiment_b()
    if plan is None:
        print("Pas de plan a dessiner (le modele n'a pas trouve de solution ?)")
        return
    if len(plan) != len(bornes):
        raise ValueError(f"Le plan doit contenir {len(bornes)} canaux, il en contient {len(plan)}.")
    G = nx.Graph()
    G.add_nodes_from(range(len(bornes)))
    G.add_edges_from(interferences)
    canaux = sorted(set(plan))
    palette = plt.get_cmap("tab10")
    couleurs = [palette(canaux.index(c) % 10) for c in plan]
    conflits = [(i, j) for i, j in interferences if plan[i] == plan[j]]
    ok = [e for e in interferences if e not in conflits]

    fig, ax = plt.subplots(figsize=(10, 4.5))
    nx.draw_networkx_edges(G, POS, edgelist=ok, ax=ax, edge_color="#999", width=1.5)
    nx.draw_networkx_edges(G, POS, edgelist=conflits, ax=ax, edge_color="red", width=4)
    nx.draw_networkx_nodes(G, POS, node_color=couleurs, node_size=1400, edgecolors="#333", ax=ax)
    nx.draw_networkx_labels(G, POS, {i: f"{bornes[i]}\n{plan[i]}" for i in range(len(bornes))},
                            font_size=7.5, ax=ax)
    ax.set_title(f"{titre} : {len(canaux)} canal(aux) utilisé(s), {len(conflits)} conflit(s)")
    ax.axis("off")
    plt.show()
    for i, j in conflits[:5]:
        print(f"Conflit : {bornes[i]} et {bornes[j]} sont toutes les deux sur le canal {plan[i]}")
    if len(conflits) > 5:
        print(f"... et {len(conflits) - 5} autre(s) conflit(s)")
