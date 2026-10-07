"""Small helpers for the matrix-games Jupyter Book.

They only wrap nashpy / numpy / matplotlib to keep the notebooks short:
print probabilities as fractions and draw best-response diagrams for 2x2 games.
"""
from fractions import Fraction

import matplotlib.pyplot as plt
import numpy as np


def frac(x, max_den=1000):
    """Return x as a readable fraction string (0.0571... -> '2/35')."""
    f = Fraction(float(x)).limit_denominator(max_den)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def pure_nash(game):
    """List the pure-strategy profiles (i, j) where nobody gains by deviating."""
    A, B = game.payoff_matrices
    return [(i, j)
            for i in range(A.shape[0]) for j in range(A.shape[1])
            if A[i, j] == A[:, j].max() and B[i, j] == B[i, :].max()]


def print_equilibria(game, rows, cols, players=("A", "B")):
    """Print every equilibrium found by support enumeration, with fractions."""
    for k, (sr, sc) in enumerate(game.support_enumeration(), start=1):
        ur, uc = game[sr, sc]
        mix_r = ", ".join(f"{r}: {frac(p)}" for r, p in zip(rows, sr) if p > 1e-12)
        mix_c = ", ".join(f"{c}: {frac(q)}" for c, q in zip(cols, sc) if q > 1e-12)
        print(f"Equilibrium {k}:  {players[0]} -> [{mix_r}]   {players[1]} -> [{mix_c}]"
              f"   payoffs = ({frac(ur)}, {frac(uc)})")


def plot_indifference(game, rows, cols, players=("A", "B")):
    """Expected payoff of each action, as a function of the opponent's mix (2x2 games).

    Left: A's payoffs as a function of q = P(B plays cols[0]).
    Right: B's payoffs as a function of p = P(A plays rows[0]).
    Where the two lines of a panel cross, that player is indifferent:
    this is the opponent's probability in the mixed equilibrium.
    """
    A, B = game.payoff_matrices
    t = np.linspace(0, 1, 101)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    panels = [
        (axes[0], players[0], players[1], cols[0], "q", rows,
         [A[0, 0] * t + A[0, 1] * (1 - t), A[1, 0] * t + A[1, 1] * (1 - t)]),
        (axes[1], players[1], players[0], rows[0], "p", cols,
         [B[0, 0] * t + B[1, 0] * (1 - t), B[0, 1] * t + B[1, 1] * (1 - t)]),
    ]
    for ax, me, other, other_act, var, my_acts, (u0, u1) in panels:
        ax.plot(t, u0, lw=2.5, color="#2a6fdb", label=f"{me} plays {my_acts[0]}")
        ax.plot(t, u1, lw=2.5, color="#e8743b", ls="--", label=f"{me} plays {my_acts[1]}")
        d0, d1 = u0[0] - u1[0], u0[-1] - u1[-1]
        if d0 * d1 < 0:                                   # the lines cross
            x = d0 / (d0 - d1)
            y = u0[0] + (u0[-1] - u0[0]) * x
            ax.axvline(x, color="grey", ls=":")
            ax.plot(x, y, "o", ms=10, mfc="white", mec="black", mew=2, zorder=5)
            lo, hi = min(u0.min(), u1.min()), max(u0.max(), u1.max())
            high = y > (lo + hi) / 2
            ax.annotate(f"{me} indifferent\nwhen {var} = {frac(x)}", (x, y),
                        textcoords="offset points", xytext=(12, -12 if high else 12),
                        va="top" if high else "bottom", fontweight="bold")
        ax.set_xlabel(f"{var} = probability that {other} plays {other_act}")
        ax.set_ylabel(f"expected payoff of {me}")
        ax.set_title(f"{me}'s payoff, depending on {other}'s mix {var}")
        ax.set_xlim(0, 1)
        ax.legend(loc="best")
        ax.grid(alpha=0.3)
    plt.tight_layout()
    return axes
