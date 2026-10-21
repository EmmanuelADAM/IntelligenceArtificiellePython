"""Model and helpers for the "Negotiation for mobility" Jupyter Book (keep this file next to the notebooks).

The book follows module 5 of the course (negotiation / bargaining):

* chapters 1-3, cooperative approach: a bargaining problem (S, d), the Nash solution,
  the Kalai-Smorodinsky (KS) solution, isolated agreements and social welfare;
* chapter 4, non-cooperative approach: ultimatum game and Rubinstein model;
* chapter 5, negotiating agents: concession strategies (Boulware, Conceder, Tit-for-Tat, Distance)
  and the Zeuthen strategy.

Conventions
-----------
* A bargaining problem is given by an array ``points`` of shape (n, 2): each row is a pair of
  utilities (u1, u2) reachable by an agreement, and by the disagreement point ``d = (d1, d2)``.
* A continuous set S is approximated by many points (see ``frontier``).
"""
import itertools

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.set_printoptions(legacy="1.25")      # print numpy numbers as 3.0, not np.float64(3.0)

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# === BOOK 1. bargaining problems

def frontier(f, u1_max, u1_min=0.0, n=2001):
    """Points (u1, f(u1)) of a continuous frontier, for u1 in [u1_min, u1_max]."""
    u1 = np.linspace(u1_min, u1_max, n)
    return np.column_stack([u1, f(u1)])


def acceptable(points, d=(0, 0)):
    """Keep only the agreements both agents prefer (weakly) to the disagreement point."""
    points = np.asarray(points, dtype=float)
    return points[(points[:, 0] >= d[0]) & (points[:, 1] >= d[1])]


def pareto(points):
    """Keep only the Pareto-optimal agreements (no other point is better for both)."""
    points = np.asarray(points, dtype=float)
    keep = [i for i, p in enumerate(points)
            if not any((q >= p).all() and (q > p).any() for q in points)]
    return points[keep]


def nash_solution(points, d=(0, 0)):
    """Agreement maximising the Nash product (u1 - d1)(u2 - d2) among acceptable points."""
    ok = acceptable(points, d)
    product = (ok[:, 0] - d[0]) * (ok[:, 1] - d[1])
    return ok[np.argmax(product)]


def ideal_point(points, d=(0, 0)):
    """a = (a1, a2): best utility of each agent while the other still gets at least d."""
    ok = acceptable(points, d)
    return ok.max(axis=0)


def ks_solution(points, d=(0, 0)):
    """Kalai-Smorodinsky: maximise the smallest relative gain (u_i - d_i) / (a_i - d_i).

    On a fine continuous frontier this is the point of the segment [d, a];
    on isolated agreements it is the 'discrete version' of the slides.
    """
    ok = acceptable(points, d)
    a = ideal_point(points, d)
    shares = (ok - np.asarray(d)) / (a - np.asarray(d))
    return ok[np.argmax(shares.min(axis=1))]


def utilitarian(points):
    """Agreement maximising the sum u1 + u2 (first one in case of a tie)."""
    points = np.asarray(points, dtype=float)
    return points[np.argmax(points.sum(axis=1))]


def egalitarian(points, d=(0, 0)):
    """Agreement maximising the smallest gain min(u1 - d1, u2 - d2)."""
    ok = acceptable(points, d)
    return ok[np.argmax((ok - np.asarray(d)).min(axis=1))]


def with_lotteries(points, n=51):
    """Add all the lotteries between two agreements: lam * P + (1 - lam) * Q.

    In expectation, a lottery gives a point of the segment [P, Q]: S becomes convex.
    """
    points = np.asarray(points, dtype=float)
    lam = np.linspace(0, 1, n)[:, None]
    mixes = [lam * p + (1 - lam) * q for p, q in itertools.combinations(points, 2)]
    return np.vstack([points] + mixes) if mixes else points


def plot_problem(points, d=(0, 0), solutions=None, labels=None, nash_curve=False,
                 ax=None, title="", line=False):
    """Draw S (points or a line), d, and some solutions given as {name: point}."""
    points = np.asarray(points, dtype=float)
    ax = ax or plt.subplots(figsize=(5, 4.5))[1]
    if line:
        ax.plot(points[:, 0], points[:, 1], lw=2.5, color="tab:blue", label="S (frontier)")
    else:
        ax.scatter(points[:, 0], points[:, 1], s=40, color="tab:blue", label="agreements", zorder=3)
    if labels is not None:
        for (x, y), name in zip(points, labels):
            ax.annotate(name, (x, y), textcoords="offset points", xytext=(5, 4), fontsize=9)
    ax.scatter(*d, s=60, marker="s", color="gray", zorder=3)
    ax.annotate("d", d, textcoords="offset points", xytext=(-12, -12))
    markers = iter(["*", "D", "P", "X", "^"])
    colors = iter(["tab:red", "tab:green", "tab:purple", "tab:orange", "tab:brown"])
    for name, p in (solutions or {}).items():
        ax.scatter(*p, s=160, marker=next(markers), color=next(colors), zorder=4,
                   label=f"{name} ({p[0]:.3g}, {p[1]:.3g})")
    if nash_curve and solutions and "Nash" in solutions:
        p = solutions["Nash"]
        value = (p[0] - d[0]) * (p[1] - d[1])
        y_top = points[:, 1].max() * 1.1 - d[1]
        x = np.linspace(d[0] + value / y_top, points[:, 0].max() * 1.05, 200)
        ax.plot(x, d[1] + value / (x - d[0]), ":", color="tab:red", label="same Nash product")
    ax.set_xlabel("$u_1$")
    ax.set_ylabel("$u_2$")
    ax.set_xlim(left=min(0, d[0]) - 0.5)
    ax.set_ylim(bottom=min(0, d[1]) - 0.5, top=points[:, 1].max() * 1.15 + 0.5)
    ax.set_title(title)
    ax.legend(fontsize=8)
    return ax


#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# === BOOK 2. an electric bike and an eco-bonus


COST = 60       # EUR: the seller's cost (reservation price)
VALUE = 100     # EUR: what the bike is worth to the buyer
CAP = 100       # EUR: maximum price allowed (price cap)


def bike_deal(price, bonus=0, cost=COST, value=VALUE):
    """Gains (seller, buyer) at this price; the State pays `bonus` EUR to the buyer."""
    price = np.asarray(price, dtype=float)
    return np.column_stack([price - cost, value + bonus - price])


def bike_prices(bonus=0, cap=CAP, cost=COST, value=VALUE, n=4001):
    """All the possible prices: the seller covers its cost, the buyer gains, the cap holds."""
    return np.linspace(cost, min(cap, value + bonus), n)

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# === BOOK 3: a shared loading bay
SLOTS = ("7h", "8h", "9h")
VALUES_1 = {"7h": 5, "8h": 3, "9h": 1}     # GreenVan: early deliveries matter a lot
VALUES_2 = {"7h": 4, "8h": 3, "9h": 2}     # CityCargo: more flexible
BAY_D = (2, 2)                              # no agreement: both deliver from the street


def allocations(values_1=VALUES_1, values_2=VALUES_2, slots=SLOTS):
    """All the ways to give each slot to company 1 or to company 2, with their utilities."""
    rows = []
    for owners in itertools.product((1, 2), repeat=len(slots)):
        u1 = sum(values_1[s] for s, o in zip(slots, owners) if o == 1)
        u2 = sum(values_2[s] for s, o in zip(slots, owners) if o == 2)
        name = "+".join(s for s, o in zip(slots, owners) if o == 1) or "-"
        rows.append({"company 1 gets": name, "u1": u1, "u2": u2})
    return pd.DataFrame(rows)


MODULE1 = pd.DataFrame({"name": list("ABCDEF"),
                        "u1": [1, 1, 7, 2, 2, 4], "u2": [6, 4, 1, 1, 2, 2.5]})


# ================================================================ 3. non-cooperative part
def rubinstein(delta_1, delta_2):
    """Rubinstein shares (x*, y*): x* = what agent 1 keeps when it proposes, y* = same for agent 2."""
    x = (1 - delta_2) / (1 - delta_1 * delta_2)
    y = (1 - delta_1) / (1 - delta_1 * delta_2)
    return x, y


def ultimatum_gain(offer, thresholds):
    """Mean gain of the proposer who offers `offer` (share of 1) to responders with these thresholds.

    A responder accepts when offer >= its threshold; a refusal gives 0 to both.
    """
    thresholds = np.asarray(thresholds)
    return (1 - offer) * np.mean(offer >= thresholds)

