"""Helpers for the "Negotiating agents: a carpool price" Jupyter Book (keep this file next to the notebooks).

The situation
-------------
Alice drives tomorrow to Valenciennes. Picking up Bob costs her a 4 EUR detour; Bob's alternative is the
train (18 EUR). On a carpool app, an agent negotiates for each of them:

* Alice's agent first asks 18 EUR and never asks less than 4 EUR (her limit);
* Bob's agent first offers 4 EUR and never offers more than 18 EUR (the train);
* at each round, both agents send an offer at the same time;
* deal as soon as the offers cross (up to 0.5 EUR): the price is the middle of the two offers;
* deadline: T rounds (the departure); no deal -> Alice drives alone, Bob takes the train: gains (0, 0).

A strategy is a plain function  strategy(r, T, mine, theirs) -> next offer
    r: the current round (0, 1, ..., T-1), T: the number of rounds,
    mine / theirs: the lists of the offers already sent by the agent / by the other agent.
"""
import matplotlib.pyplot as plt
import numpy as np

DETOUR, TRAIN = 4, 18          # EUR: Alice's limit and Bob's limit
ALICE_START, BOB_START = 18, 4  # EUR: first offers
T = 10                          # number of rounds before the departure


def gains(price):
    """(Alice's gain, Bob's gain) for a price; (0, 0) if there is no deal (price None)."""
    if price is None:
        return 0.0, 0.0
    return price - DETOUR, TRAIN - price


def negotiate(alice, bob, T=T, risk=0.0, seed=None, tol=0.5):
    """Run a negotiation between two strategies.

    risk: probability that the negotiation stops before each new round (Bob takes the train...).
    Returns a dict: price (None if no deal), round of the deal, offers of Alice and of Bob, gains.
    """
    rng = np.random.default_rng(seed)
    a_offers, b_offers = [], []
    for r in range(T):
        if r > 0 and rng.random() < risk:
            break
        a = max(alice(r, T, a_offers, b_offers), DETOUR)   # Alice never asks less than 4 EUR
        b = min(bob(r, T, b_offers, a_offers), TRAIN)       # Bob never offers more than 18 EUR
        a_offers.append(a)
        b_offers.append(b)
        if b >= a - tol:
            price = (a + b) / 2
            return {"price": price, "round": r, "alice": a_offers, "bob": b_offers, "gains": gains(price)}
    return {"price": None, "round": len(a_offers) - 1, "alice": a_offers, "bob": b_offers, "gains": (0.0, 0.0)}


def show(result, ax=None, title=""):
    """Plot the offers of both agents, round after round, and the deal if any."""
    ax = ax or plt.subplots(figsize=(6.5, 3.5))[1]
    ax.plot(result["alice"], "o-", color="tab:blue", label="Alice asks")
    ax.plot(result["bob"], "s-", color="tab:red", label="Bob offers")
    if result["price"] is not None:
        ax.axhline(result["price"], ls=":", color="gray")
        ax.set_title(title or f"deal at {result['price']:.2f} EUR (round {result['round']})")
    else:
        ax.set_title(title or "no deal")
    ax.set_xlabel("round")
    ax.set_ylabel("price (EUR)")
    ax.set_ylim(DETOUR - 1, TRAIN + 1)
    ax.legend()
    return ax


# ---------------------------------------------------------------- the strategies of the course
def time_dependent(r, T, start, limit, beta):
    """p(t) = start + (limit - start) * t^(1/beta), with t = r / (T-1) from 0 to 1."""
    t = r / (T - 1)
    return start + (limit - start) * t ** (1 / beta)


def tit_for_tat(mine, theirs, start, direction, coef=1.0, first_step=1.0):
    """Concede coef x the other's last concession (first_step at the 2nd round). direction: -1 Alice, +1 Bob."""
    if not mine:
        return start
    if len(theirs) < 2:
        return mine[-1] + direction * first_step
    return mine[-1] + direction * coef * abs(theirs[-1] - theirs[-2])


def distance(mine, theirs, start, k):
    """p' = p + k (p_received - p): cover a fraction k of the gap with the other's last offer."""
    if not mine:
        return start
    return mine[-1] + k * (theirs[-1] - mine[-1])
