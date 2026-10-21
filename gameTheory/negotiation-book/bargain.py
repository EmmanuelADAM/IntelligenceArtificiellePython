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


# ================================================================ 1. bargaining problems
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



# --- chapter 2: an electric bike and an eco-bonus
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


# --- chapter 3: a shared loading bay
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


# ================================================================ 4. negotiating agents (V2G)
# An electric car owner (seller) sells energy to the grid operator (buyer) during a peak hour.
SELLER_RES, SELLER_START = 10, 40      # c/kWh: minimum price (battery wear), first asking price
BUYER_RES, BUYER_START = 30, 5         # c/kWh: maximum price (peak price), first offer


class Negotiator:
    """Base class. A negotiator proposes a price at each round (it never crosses its reservation).

    role: "seller" (wants a high price) or "buyer" (wants a low price).
    In `propose`, t is the time in [0, 1] (round / last round), mine and theirs the past offers.
    """
    name = "Negotiator"

    def __init__(self, role, start=None, reservation=None):
        self.role = role
        seller = role == "seller"
        self.start = start if start is not None else (SELLER_START if seller else BUYER_START)
        self.reservation = reservation if reservation is not None else (SELLER_RES if seller else BUYER_RES)

    def propose(self, t, mine, theirs):
        raise NotImplementedError

    def clip(self, price):
        """Never go beyond the reservation price."""
        if self.role == "seller":
            return max(price, self.reservation)
        return min(price, self.reservation)

    def gain(self, price):
        """Gain of an agreement at this price (0 if no deal)."""
        if price is None:
            return 0.0
        return price - self.reservation if self.role == "seller" else self.reservation - price

    def __repr__(self):
        return f"{self.name} ({self.role})"


class TimeDependent(Negotiator):
    """p(t) = start + (reservation - start) * t^(1/beta): beta < 1 Boulware, beta > 1 Conceder."""

    def __init__(self, role, beta=1.0, **kw):
        super().__init__(role, **kw)
        self.beta = beta
        self.name = "Boulware" if beta < 1 else ("Conceder" if beta > 1 else "Linear")
        self.name += f" b={beta:g}"

    def propose(self, t, mine, theirs):
        return self.start + (self.reservation - self.start) * t ** (1 / self.beta)


class TitForTat(Negotiator):
    """Concedes coef x the opponent's last concession (a small first step to start)."""

    def __init__(self, role, coef=1.0, first_step=1.0, **kw):
        super().__init__(role, **kw)
        self.coef, self.first_step = coef, first_step
        self.name = f"TitForTat c={coef:g}"

    def propose(self, t, mine, theirs):
        if not mine:
            return self.start
        if len(theirs) < 2:
            step = self.first_step
        else:
            step = self.coef * abs(theirs[-1] - theirs[-2])
        direction = -1 if self.role == "seller" else 1
        return mine[-1] + direction * step


class Distance(Negotiator):
    """p' = p + k (p_received - p): moves a fraction k towards the opponent's last offer."""

    def __init__(self, role, k=0.2, **kw):
        super().__init__(role, **kw)
        self.k = k
        self.name = f"Distance k={k:g}"

    def propose(self, t, mine, theirs):
        if not mine:
            return self.start
        return mine[-1] + self.k * (theirs[-1] - mine[-1])


def negotiate(seller, buyer, rounds=20, breakdown=0.0, seed=None, tol=0.5):
    """Both agents announce an offer at each round (simultaneously).

    Deal as soon as the buyer offers at least what the seller asks (up to `tol` c/kWh):
    price = middle of the two offers.
    breakdown: probability that the negotiation stops before each new round (e.g. the car leaves).
    Returns a dict: price (None if no deal), round, offers of the seller and of the buyer, gains.
    """
    rng = np.random.default_rng(seed)
    s_offers, b_offers = [], []
    price, end = None, rounds - 1
    for r in range(rounds):
        if r > 0 and rng.random() < breakdown:
            end = r - 1
            break
        t = r / (rounds - 1)
        s = seller.clip(seller.propose(t, s_offers, b_offers))
        b = buyer.clip(buyer.propose(t, b_offers, s_offers))
        s_offers.append(s)
        b_offers.append(b)
        if b >= s - tol:
            price, end = (s + b) / 2, r
            break
    return {"price": price, "round": end, "seller": s_offers, "buyer": b_offers,
            "gains": (seller.gain(price), buyer.gain(price))}


def plot_negotiation(result, ax=None, title=""):
    """Offers of both agents round after round, and the deal if any."""
    ax = ax or plt.subplots(figsize=(6.5, 3.5))[1]
    ax.plot(result["seller"], "o-", label="seller (car owner)")
    ax.plot(result["buyer"], "s-", label="buyer (grid operator)")
    if result["price"] is not None:
        ax.axhline(result["price"], ls=":", color="gray")
        ax.annotate(f"deal at {result['price']:.1f} (round {result['round']})",
                    (0, result["price"]), textcoords="offset points", xytext=(4, 4), fontsize=9)
    else:
        ax.annotate("no deal", (len(result["seller"]) - 1, result["seller"][-1]),
                    textcoords="offset points", xytext=(4, 4), color="tab:red")
    ax.set_xlabel("round")
    ax.set_ylabel("price (c/kWh)")
    ax.set_title(title)
    ax.legend(fontsize=8)
    return ax


def tournament(sellers, buyers, rounds=20, breakdown=0.0, runs=300, seed=0):
    """Mean gains of each seller strategy (rows) against each buyer strategy (columns).

    sellers, buyers: functions without argument that create a new negotiator, e.g.
    lambda: TimeDependent("seller", beta=0.3). Returns (seller gains, buyer gains, deal rates).
    """
    rng = np.random.default_rng(seed)
    S, B, R = {}, {}, {}
    for make_b in buyers:
        name_b = make_b().name
        col_s, col_b, col_r = [], [], []
        for make_s in sellers:
            res = [negotiate(make_s(), make_b(), rounds, breakdown, rng.integers(1 << 30))
                   for _ in range(runs if breakdown else 1)]
            col_s.append(np.mean([r["gains"][0] for r in res]))
            col_b.append(np.mean([r["gains"][1] for r in res]))
            col_r.append(np.mean([r["price"] is not None for r in res]))
        S[name_b], B[name_b], R[name_b] = col_s, col_b, col_r
    index = [m().name for m in sellers]
    return (pd.DataFrame(S, index=index).round(2), pd.DataFrame(B, index=index).round(2),
            pd.DataFrame(R, index=index).round(2))


def zeuthen(u_seller, u_buyer, prices, start_seller=None, start_buyer=None):
    """Monotonic Concession Protocol with the Zeuthen strategy, on a grid of prices.

    u_seller(p), u_buyer(p): utilities of an agreement at price p (0 = no deal).
    At each round, each agent computes its risk = (U(own offer) - U(other's offer)) / U(own offer):
    the agent with the smaller risk (more to lose in a conflict) concedes one step on the grid.
    Returns the list of (seller offer, buyer offer) and the final price.
    """
    prices = np.sort(np.asarray(prices, dtype=float))
    i_s = len(prices) - 1 if start_seller is None else int(np.argmin(abs(prices - start_seller)))
    i_b = 0 if start_buyer is None else int(np.argmin(abs(prices - start_buyer)))
    history = [(prices[i_s], prices[i_b])]
    while i_b < i_s:
        ps, pb = prices[i_s], prices[i_b]
        risk_s = (u_seller(ps) - u_seller(pb)) / u_seller(ps) if u_seller(ps) > 0 else 0
        risk_b = (u_buyer(pb) - u_buyer(ps)) / u_buyer(pb) if u_buyer(pb) > 0 else 0
        if risk_s <= risk_b:
            i_s -= 1
        if risk_b <= risk_s:
            i_b += 1
        history.append((prices[i_s], prices[i_b]))
    return history, prices[i_s] if i_b == i_s else (prices[i_s] + prices[i_b]) / 2
