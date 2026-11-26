"""Helpers for the "Sharing a charging station" Jupyter Book
(library, so keep this file next to the notebooks).

The situation
-------------
Alice owns a house with a 22 kW wallbox in her yard; she works during the day and mostly uses her electric car at the weekend.
Bob, her neighbour, is a home nurse: he chains short visits in the district and often comes home during the day.
He has just bought an electric car and cannot install a charger. He asks Alice to share her charger.
They must agree on the terms.

* Chapter 1: one issue, the price of the kWh.
* Chapters 2 to 4: several issues (margin over Alice's tariff, charges per month, time slot, then notice and duration).
  Bob pays Alice's tariff of the slot (ALICE_TARIFF) plus the negotiated margin.

Conventions
-----------
* A package (a possible agreement) is a dict, e.g. {"margin": 0.10, "charges": 10, "slot": "7h-18h"}.
* A scoring sheet gives, for each issue, the points of each option (private to each agent).
* A strategy is a plain function  strategy(r, T, mine, theirs) -> next offer
    r: the current round (0, 1, ..., T-1), T: the number of rounds,
    mine / theirs: the lists of the offers already sent by the agent / by the other agent.
"""
import itertools

import matplotlib.pyplot as plt
import numpy as np

# ------------ GLOBAL VARIABLES: chapter 1 (one issue, the price) ------------------------------------
ALICE_COST = 0.20          # EUR/kWh: Alice's electricity price (regulated tariff, base option)
ALICE_NIGHT_COST = 0.16    # EUR/kWh: Alice's price during off-peak hours (night)
PUBLIC_PRICE = 0.35        # EUR/kWh: Bob's alternative, the public charger of the district
ALICE_START, BOB_START = 0.40, 0.16   # EUR/kWh: first offers
KWH_PER_MONTH = 200        # kWh: Bob's needs (about 1200 km per month)
T_PRICE = 10               # rounds for the price negotiation


def price_gains(price, cost=ALICE_COST, public=PUBLIC_PRICE):
    """Return (Alice's gain, Bob's gain) in EUR per kWh; (0, 0) if there is no deal (price None)."""
    if price is None:
        return 0.0, 0.0
    return price - cost, public - price


def time_dependent(r, T, start, limit, beta):
    """p(t) = start + (limit - start) * t^(1/beta), with t = r / (T-1) from 0 to 1."""
    t = r / (T - 1)
    return start + (limit - start) * t ** (1 / beta)


def negotiate_price(alice, bob, T=T_PRICE, tol=0.005, cost=ALICE_COST, public=PUBLIC_PRICE):
    """Run a negotiation on the price only (simultaneous offers, as in the carpool book).

    parameters:
    alice, bob: the two strategies (functions)
    T: number of rounds
    tol: the tolerance for a deal (the offers can cross by up to tol EUR)
    cost, public: Alice's limit (her cost) and Bob's limit (the public charger)
    Returns a dict: price (None if no deal), round of the deal, offers of Alice and of Bob, gains per kWh.
    """
    a_offers, b_offers = [], []
    for r in range(T):
        a = max(alice(r, T, a_offers, b_offers), cost)     # Alice never asks less than her cost
        b = min(bob(r, T, b_offers, a_offers), public)      # Bob never offers more than the public charger
        a_offers.append(a)
        b_offers.append(b)
        if b >= a - tol:
            price = (a + b) / 2
            return {"price": price, "round": r, "alice": a_offers, "bob": b_offers,
                    "gains": price_gains(price, cost, public)}
    return {"price": None, "round": len(a_offers) - 1, "alice": a_offers, "bob": b_offers, "gains": (0.0, 0.0)}


def show_price(result, ax=None, title=""):
    """Plot the price offers of both agents, round after round, and the deal if any."""
    ax = ax or plt.subplots(figsize=(6.5, 3.5))[1]
    ax.plot(result["alice"], "o-", color="tab:blue", label="Alice asks")
    ax.plot(result["bob"], "s-", color="tab:red", label="Bob offers")
    if result["price"] is not None:
        ax.axhline(result["price"], ls=":", color="gray")
        ax.set_title(title or f"deal at {result['price']:.3f} EUR/kWh (round {result['round']})")
    else:
        ax.set_title(title or "no deal")
    ax.set_xlabel("round")
    ax.set_ylabel("price (EUR/kWh)")
    ax.legend()
    return ax


# ------------ GLOBAL VARIABLES: chapters 2 to 4 (several issues) ------------------------------------
# Bob pays Alice's tariff of the slot plus the negotiated margin (EUR/kWh)
ALICE_TARIFF = {"7h-18h": 0.20, "18h-22h": 0.20, "22h-7h": 0.16}

# Scoring sheets: points of each option, for each issue (private information of each agent).
# The options of each issue are written in the same order for both agents.
ALICE_SHEET = {
    "margin":   {0.00: 0, 0.02: 4, 0.04: 8, 0.06: 12, 0.08: 17, 0.10: 22, 0.12: 26, 0.14: 30},
    "charges":  {4: 20, 6: 17, 8: 12, 10: 6, 12: 0},
    "slot":     {"7h-18h": 25, "18h-22h": 0, "22h-7h": 10},
    "notice":   {"0 h": 0, "2 h": 6, "12 h": 11, "24 h": 15, "48 h": 15},
    "duration": {"1 month": 7, "3 months": 10, "6 months": 6, "12 months": 0},
}
BOB_SHEET = {
    "margin":   {0.00: 30, 0.02: 26, 0.04: 22, 0.06: 18, 0.08: 14, 0.10: 9, 0.12: 5, 0.14: 0},
    "charges":  {4: 0, 6: 7, 8: 15, 10: 21, 12: 25},
    "slot":     {"7h-18h": 15, "18h-22h": 6, "22h-7h": 12},
    "notice":   {"0 h": 6, "2 h": 10, "12 h": 5, "24 h": 2, "48 h": 0},
    "duration": {"1 month": 0, "3 months": 6, "6 months": 13, "12 months": 20},
}
ISSUES_3 = ["margin", "charges", "slot"]                          # chapters 2 and 3
ISSUES_5 = ["margin", "charges", "slot", "notice", "duration"]    # chapter 4

# Reservation scores: below this score, the agent prefers no deal
ALICE_RESERVATION_3, BOB_RESERVATION_3 = 30, 25    # with 3 issues (Alice max 75, Bob max 70)
ALICE_RESERVATION_5, BOB_RESERVATION_5 = 40, 35    # with 5 issues (max 100 for both)
T_PACKAGES = 20                                    # rounds for the negotiation on packages


def price_paid(package):
    """Return the price (EUR/kWh) Bob pays with this package: Alice's tariff of the slot plus the margin."""
    return round(ALICE_TARIFF[package["slot"]] + package["margin"], 2)


def all_packages(issues):
    """Return the list of all the possible packages (dicts) on these issues."""
    options = [list(ALICE_SHEET[issue]) for issue in issues]
    return [dict(zip(issues, combination)) for combination in itertools.product(*options)]


def score(package, sheet):
    """Return the score of a package for the agent who owns this sheet (sum of the points of each issue)."""
    return sum(sheet[issue][package[issue]] for issue in package)


def pareto(packages, sheet_a=ALICE_SHEET, sheet_b=BOB_SHEET):
    """Return the Pareto-optimal packages: no other package is better for one agent and not worse for the other."""
    scores = [(score(p, sheet_a), score(p, sheet_b)) for p in packages]
    optimal = []
    for p, (a, b) in zip(packages, scores):
        dominated = any(a2 >= a and b2 >= b and (a2 > a or b2 > b) for a2, b2 in scores)
        if not dominated:
            optimal.append(p)
    return optimal


def show_packages(packages, res_a, res_b, marked=None, ax=None, title=""):
    """Plot all the packages in the plane (Alice's score, Bob's score), the reservation lines,
    the Pareto frontier, and some marked packages given as {name: package}."""
    ax = ax or plt.subplots(figsize=(6, 5))[1]
    xs = [score(p, ALICE_SHEET) for p in packages]
    ys = [score(p, BOB_SHEET) for p in packages]
    ax.scatter(xs, ys, s=12, color="lightgray", label="packages")
    front = sorted(pareto(packages), key=lambda p: score(p, ALICE_SHEET))
    ax.plot([score(p, ALICE_SHEET) for p in front], [score(p, BOB_SHEET) for p in front],
            "-", color="tab:green", lw=1.5, label="Pareto frontier")
    ax.axvline(res_a, ls="--", color="tab:blue", lw=1, label="Alice's reservation")
    ax.axhline(res_b, ls="--", color="tab:red", lw=1, label="Bob's reservation")
    markers = ["*", "D", "P", "X", "^", "v"]
    for k, (name, p) in enumerate((marked or {}).items()):
        a, b = score(p, ALICE_SHEET), score(p, BOB_SHEET)
        ax.scatter(a, b, s=150, marker=markers[k % len(markers)], zorder=3, label=f"{name} ({a}, {b})")
    ax.set_xlabel("Alice's score")
    ax.set_ylabel("Bob's score")
    ax.set_title(title)
    ax.legend(fontsize=8)
    return ax


# ------------ negotiation on packages (chapters 3 and 4) --------------------------------------------
def option_distance(p, q):
    """Distance between two packages: for each issue, the gap between the positions of the two options
    (0 = same option, 1 = the two extreme options), summed over the issues."""
    d = 0.0
    for issue in p:
        options = list(ALICE_SHEET[issue])
        d += abs(options.index(p[issue]) - options.index(q[issue])) / (len(options) - 1)
    return d


def negotiate(alice, bob, issues=ISSUES_3, T=T_PACKAGES, res_a=ALICE_RESERVATION_3, res_b=BOB_RESERVATION_3):
    """Run a negotiation on packages, with alternating offers.

    Round 0: Alice proposes, round 1: Bob proposes, and so on.
    The other agent accepts the offer if it is at least as good for it as the package it would propose now
    (it only uses its own sheet). After T rounds without agreement: no deal, each agent keeps its reservation.
    parameters:
    alice, bob: the two strategies (functions)
    issues: ISSUES_3 or ISSUES_5 (only used for the result)
    T: number of rounds
    res_a, res_b: reservation scores, given when there is no deal
    Returns a dict: package (None if no deal), round, offers of Alice and of Bob, scores (Alice, Bob).
    """
    a_offers, b_offers = [], []
    for r in range(T):
        if r % 2 == 0:
            offer = alice(r, T, a_offers, b_offers)
            a_offers.append(offer)
            counter = bob(r, T, b_offers, a_offers)          # what Bob would propose now
            accepted = score(offer, BOB_SHEET) >= score(counter, BOB_SHEET)
        else:
            offer = bob(r, T, b_offers, a_offers)
            b_offers.append(offer)
            counter = alice(r, T, a_offers, b_offers)        # what Alice would propose now
            accepted = score(offer, ALICE_SHEET) >= score(counter, ALICE_SHEET)
        if accepted:
            return {"package": offer, "round": r, "alice": a_offers, "bob": b_offers, "issues": issues,
                    "scores": (score(offer, ALICE_SHEET), score(offer, BOB_SHEET))}
    return {"package": None, "round": T - 1, "alice": a_offers, "bob": b_offers, "issues": issues,
            "scores": (res_a, res_b)}


def show_negotiation(result, res_a, res_b, ax=None, title=""):
    """Plot the offers of both agents in the plane (Alice's score, Bob's score), with the Pareto frontier."""
    ax = show_packages(all_packages(result["issues"]), res_a, res_b, ax=ax)
    for offers, color, name in ((result["alice"], "tab:blue", "Alice's offers"), (result["bob"], "tab:red", "Bob's offers")):
        ax.plot([score(p, ALICE_SHEET) for p in offers], [score(p, BOB_SHEET) for p in offers],
                "o-", color=color, ms=4, lw=1, label=name)
    if result["package"] is not None:
        ax.scatter(*result["scores"], s=200, marker="*", color="gold", edgecolor="black", zorder=4,
                   label=f"deal {result['scores']} (round {result['round']})")
    ax.set_title(title or ("no deal" if result["package"] is None else ""))
    ax.legend(fontsize=7)
    return ax


# ------------ the strategies on packages (written step by step in chapter 3) -----------------------
def target_score(r, T, sheet, issues, reservation, beta):
    """The score the agent asks for at round r: from its best score down to its reservation (time-dependent)."""
    best = max(score(p, sheet) for p in all_packages(issues))
    return time_dependent(r, T, best, reservation, beta)


def candidates(r, T, sheet, issues, reservation, beta):
    """The packages that give the agent at least its target score at round r."""
    target = target_score(r, T, sheet, issues, reservation, beta)
    return [p for p in all_packages(issues) if score(p, sheet) >= target]


def blind(r, T, mine, theirs, sheet, issues, reservation, beta):
    """Blind agent: among its candidates, proposes the one with the lowest score for itself (closest to its target),
    without looking at the other's offers."""
    return min(candidates(r, T, sheet, issues, reservation, beta), key=lambda p: score(p, sheet))


def trade_off(r, T, mine, theirs, sheet, issues, reservation, beta):
    """Trade-off agent: among its candidates, proposes the one closest to the other's last offer
    (the best one for itself at the first round, or when two candidates are as close)."""
    pool = candidates(r, T, sheet, issues, reservation, beta)
    if not theirs:
        return max(pool, key=lambda p: score(p, sheet))
    return min(pool, key=lambda p: (option_distance(p, theirs[-1]), -score(p, sheet)))
