"""Small helpers for the axelrod Jupyter Book (keep this file next to the notebooks).

They only wrap axelrod / matplotlib so that the notebooks stay short:
print a game as a bimatrix, draw the scores of a match, summarise a tournament.
"""
import axelrod as axl
import matplotlib.pyplot as plt
import numpy as np

np.set_printoptions(legacy="1.25")   # print numpy numbers as 3, not np.int64(3)


def show_game(game, actions=("C", "D"), title=""):
    """Print an axelrod game as a bimatrix: (row player's payoff, column player's payoff)."""
    A, B = np.asarray(game.A), np.asarray(game.B)
    if title:
        print(title)
    w = max(len(a) for a in actions)
    print(" " * (w + 2) + "".join(f"{a:^10}" for a in actions))
    for i, a in enumerate(actions):
        cells = "".join(f"{f'({A[i, j]:g}, {B[i, j]:g})':^10}" for j in range(len(actions)))
        print(f"{a:>{w}}  {cells}")
    print()


def plot_match(match, ax=None, title=None):
    """Cumulative score of both players, turn after turn (call match.play() first)."""
    ax = ax or plt.subplots(figsize=(6, 3.5))[1]
    scores = np.cumsum(match.scores(), axis=0)
    turns = np.arange(1, len(scores) + 1)
    for k, (player, style) in enumerate(zip(match.players, ("-", "--"))):
        ax.plot(turns, scores[:, k], style, lw=2.5, marker="o", ms=3, label=player.name)
    ax.set_xlabel("turn")
    ax.set_ylabel("cumulative score")
    ax.set_title(title or f"{match.players[0].name} vs {match.players[1].name}")
    ax.legend()
    return ax


def mean_scores(results):
    """Mean score per turn of each strategy in a tournament, best first: {name: score}."""
    means = {name: float(np.mean(s)) for name, s in zip(results.players, results.normalised_scores)}
    return dict(sorted(means.items(), key=lambda kv: -kv[1]))


def print_ranking(results, title=""):
    """Print the ranking of a tournament with the mean score per turn."""
    if title:
        print(title)
    for rank, (name, s) in enumerate(mean_scores(results).items(), start=1):
        print(f"{rank:>3}. {name:<42}{s:6.2f}")
    print()
