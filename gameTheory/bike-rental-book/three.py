"""Model and helpers for chapter 5 "Three renters" (keep this file next to the notebooks).

The model
---------
Same assumptions as bikes.py, with any number of shops in the street (3 by default):

* each shop has 20 bikes; the usual price is 15 EUR per day;
* C = keep the usual price; D = play the day: undercut to 10 EUR on a quiet day, surge to 25 EUR on a busy day;
* customers go to the cheapest shops first (split equally between shops at the same price),
  then the customers not served go to the next price level;
* at 25 EUR, only 60 % of the customers still want a bike;
* reputation cost of a shop above the usual price, per bike rented:
  - review_rule="any":   12.5 EUR (bad_review) if at least one other shop keeps the usual price, else 5 EUR (grumble);
  - review_rule="share": from 5 EUR (no other shop at the usual price) to 12.5 EUR (all the others at the usual price),
                         in proportion to the share of the other shops that keep the usual price.

With three shops, the street has 30 customers on a quiet day and 90 on a busy day.

A policy is a function  policy(me, others, today, days) -> C or D
* me:     my past moves (list of C / D)
* others: the past moves of each other shop (list of lists, one per other shop)
* today:  "quiet" or "busy"
* days:   the types of the past days, in the same order as the moves
We only keep axelrod's actions C and D: axelrod's matches are for two players only.
"""
import axelrod as axl
import matplotlib.pyplot as plt
import numpy as np

C, D = axl.Action.C, axl.Action.D

# ---------------------------------------------------------------- global values
FLEET = 20                                  # bikes per shop
USUAL, LOW, HIGH = 15, 10, 25               # prices in EUR per day
MOVE_PRICE = {"quiet": LOW, "busy": HIGH}   # the price of D on each type of day
CUSTOMERS = {"quiet": 30, "busy": 90}       # customers in the street, for 3 shops
STILL_WILLING = {HIGH: 0.6}                 # share of customers who still rent at this price (else 100 %)
BAD_REVIEW, GRUMBLE = 12.5, 5               # reputation costs per bike rented above the usual price

CITY_WEEK = ["busy"] * 5 + ["quiet"] * 2      # active city: commuters on weekdays, quiet weekends
TOURIST_WEEK = ["quiet"] * 5 + ["busy"] * 2   # tourist town: quiet weekdays, busy weekends


def season(week, n_weeks=26):
    """A calendar: the list of day types for n_weeks repetitions of a week pattern."""
    return list(week) * n_weeks


# ---------------------------------------------------------------- one day
def rentals(prices, customers, fleet=FLEET):
    """Number of bikes rented by each shop, given the prices of all shops.

    The cheapest shops are served first; the customers who are not served go to the next price level.
    """
    rented = [0.0] * len(prices)
    left = customers                                        # customers still looking for a bike
    for price in sorted(set(prices)):                       # from the cheapest price level to the dearest
        shops = [k for k, p in enumerate(prices) if p == price]
        willing = left * STILL_WILLING.get(price, 1)        # customers who accept this price
        for k in shops:
            rented[k] = float(min(fleet, willing / len(shops)))   # equal split between shops at this price
        left = left - sum(rented[k] for k in shops)
    return rented


def reputation_cost(k, prices, review_rule="any", bad_review=BAD_REVIEW, grumble=GRUMBLE):
    """Reputation cost per bike rented for shop k (0 if its price is not above the usual price)."""
    if prices[k] <= USUAL:
        return 0
    others = [p for j, p in enumerate(prices) if j != k]
    n_usual = sum(1 for p in others if p <= USUAL)          # other shops that keep the usual price
    if review_rule == "any":
        return bad_review if n_usual > 0 else grumble
    if review_rule == "share":
        return grumble + (bad_review - grumble) * n_usual / len(others)
    raise ValueError(f"unknown review_rule {review_rule!r}: use 'any' or 'share'")


def revenues(prices, customers, review_rule="any", bad_review=BAD_REVIEW, grumble=GRUMBLE):
    """Revenue of each shop (EUR) for one day, including the reputation costs."""
    rented = rentals(prices, customers)
    result = []
    for k, price in enumerate(prices):
        cost = reputation_cost(k, prices, review_rule, bad_review, grumble)
        result.append(rented[k] * (price - cost))
    return result


def prices_of(moves, day):
    """The prices posted by the shops, from their moves (C / D) on this type of day."""
    return [USUAL if m == C else MOVE_PRICE[day] for m in moves]


# ---------------------------------------------------------------- Schelling diagram
def plot_schelling(day, ax=None, n_shops=3, review_rule="any", bad_review=BAD_REVIEW, grumble=GRUMBLE):
    """My revenue when I play C or D, against the number of OTHER shops playing D."""
    ax = ax or plt.subplots(figsize=(6, 3.8))[1]
    customers = CUSTOMERS[day]
    n_others = range(n_shops)                               # 0 .. n_shops-1 other shops playing D
    for my_move, label, style in ((C, "I keep the usual price (C)", "o-"),
                                  (D, "I play the day (D)", "s--")):
        mine = []
        for n_d in n_others:
            moves = [my_move] + [D] * n_d + [C] * (n_shops - 1 - n_d)   # I am shop 0
            mine.append(revenues(prices_of(moves, day), customers, review_rule, bad_review, grumble)[0])
        ax.plot(list(n_others), mine, style, lw=2.5, label=label)
    ax.set_xticks(list(n_others))
    ax.set_xlabel("number of OTHER shops playing D")
    ax.set_ylabel("my revenue of the day (EUR)")
    ax.set_title(f"{day} day, {n_shops} shops")
    ax.legend()
    return ax


# ---------------------------------------------------------------- policies
def steady(me, others, today, days):
    """Always the usual price."""
    return C


def opportunist(me, others, today, days):
    """Always plays the day: undercuts on quiet days, surges on busy days."""
    return D


def make_mirror(quiet_threshold=1, busy_threshold=2):
    """A Mirror for several neighbours.

    On a quiet day, it undercuts if at least quiet_threshold other shops undercut on the last quiet day;
    on a busy day, it surges if at least busy_threshold other shops surged on the last busy day.
    The first day of each type, it keeps the usual price.
    """
    def mirror(me, others, today, days):
        same_days = [t for t, d in enumerate(days) if d == today]   # past days of the same type
        if not same_days:
            return C
        last = same_days[-1]
        n_d = sum(1 for moves in others if moves[last] == D)        # other shops that played D that day
        threshold = quiet_threshold if today == "quiet" else busy_threshold
        return D if n_d >= threshold else C

    mirror.__name__ = f"mirror(q={quiet_threshold}, b={busy_threshold})"
    return mirror


def names(policies):
    """The names of the policies (function names)."""
    return [p.__name__ for p in policies]


# ---------------------------------------------------------------- a season
def play_season(policies, calendar, noise=0, seed=0, review_rule="any", bad_review=BAD_REVIEW, grumble=GRUMBLE):
    """Play a whole season with one policy per shop.

    noise: probability that a shop posts the wrong price on a given day.
    Returns:
    - result: array (n_days x n_shops), the revenue of each shop on each day;
    - history: list (one per shop) of the moves actually played.
    """
    rng = np.random.default_rng(seed)
    n = len(policies)
    history = [[] for _ in range(n)]
    days = []
    result = np.zeros((len(calendar), n))
    for t, today in enumerate(calendar):
        moves = []
        for k, policy in enumerate(policies):
            others = [history[j] for j in range(n) if j != k]
            move = policy(history[k], others, today, days)
            if noise and rng.random() < noise:
                move = move.flip()                           # a mistake: the wrong price is posted
            moves.append(move)
        for k in range(n):
            history[k].append(moves[k])
        days.append(today)
        result[t] = revenues(prices_of(moves, today), CUSTOMERS[today], review_rule, bad_review, grumble)
    return result, history


def summary(policies, result):
    """Mean revenue per day of each shop."""
    for name, r in zip(names(policies), result.mean(axis=0)):
        print(f"{name:>24}: {r:6.1f} EUR per day")


def show_moves(policies, history, calendar, n_days=14):
    """Print the type of each day and the moves of each shop."""
    days = "".join("B" if d == "busy" else "q" for d in calendar[:n_days])
    print(f"{'day (B=busy, q=quiet)':>24}  {days}")
    for name, moves in zip(names(policies), history):
        print(f"{name:>24}  {''.join(m.name for m in moves[:n_days])}")
