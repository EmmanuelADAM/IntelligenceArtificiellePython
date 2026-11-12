"""Model and helpers for the "Two bike renters" Jupyter Book (keep this file next to the notebooks).

The model
---------
Two bike renters share the same street. Each has a fleet of 20 bikes; the usual price is 15 EUR per day.
Every morning, each renter chooses a price for the day:

* C ("cooperate") = keep the usual price (15 EUR);
* D ("defect")    = play the day: undercut to 10 EUR on a quiet day, surge to 25 EUR on a busy day.

Customers go to the cheaper renter first; when its bikes are all out, they go to the other one.
At 25 EUR, only 60 % of the customers still want a bike (the others walk, take the bus or give up).
A customer who paid 25 EUR while the shop next door charged 15 EUR feels cheated: we count a
"bad review" cost of 12.5 EUR per such customer (lost future business). When both shops charge 25 EUR,
the price looks like the market price and the cost is smaller (5 EUR per customer).

Libraries: axelrod for the games and the repeated play, nashpy for the Nash equilibria.
"""
import axelrod as axl
import matplotlib.pyplot as plt
import nashpy as nash
import numpy as np
import pandas as pd

np.set_printoptions(legacy="1.25")          # print numpy numbers as 3, not np.int64(3)
C, D = axl.Action.C, axl.Action.D

FLEET = 20                                  # bikes per renter
USUAL, LOW, HIGH = 15, 10, 25               # prices in EUR per day
QUIET_CUSTOMERS, BUSY_CUSTOMERS = 20, 60    # customers in the street on a quiet / busy day



# ---------------------------------------------------------------- one day
still_willing = lambda price: 1 if price <= USUAL else max(0, 1 - (price - USUAL) * 4 / 100)

def willing(price, customers):
    """Number of customers who still want a bike at this price."""
    return customers * still_willing(price)


def rentals(my_price, other_price, customers, fleet=FLEET):
    """Number of bikes I rent, given both prices and the number of customers in the street."""
    if my_price == other_price:                      # same price: customers split equally
        return min(fleet, willing(my_price, customers) / 2)
    if my_price < other_price:                       # I am cheaper: I am served first
        return min(fleet, willing(my_price, customers))
    left = customers - min(fleet, willing(other_price, customers))   # not served next door
    return min(fleet, willing(my_price, left))       # I am dearer: I only get the overflow


def revenue(my_price, other_price, customers, bad_review=12.5, grumble=5):
    """My revenue of the day (EUR), including the reputation cost of a surge price."""
    cost = 0
    if my_price > USUAL:
        cost = bad_review if other_price == USUAL else grumble
    return rentals(my_price, other_price, customers) * (my_price - cost)


def day_game(customers, move_price, **costs):
    """The 2x2 game of one day: C = usual price, D = move_price. Returns an axelrod Game."""
    R = revenue(USUAL, USUAL, customers, **costs)
    S = revenue(USUAL, move_price, customers, **costs)
    T = revenue(move_price, USUAL, customers, **costs)
    P = revenue(move_price, move_price, customers, **costs)
    return axl.Game(r=R, s=S, t=T, p=P)


QUIET_DAY = day_game(QUIET_CUSTOMERS, LOW)      # quiet day: the move is to undercut
BUSY_DAY = day_game(BUSY_CUSTOMERS, HIGH)       # busy day: the move is to surge
GAMES = {"quiet": QUIET_DAY, "busy": BUSY_DAY}


def show_game(game, moved_price, title=""):
    """Print a symmetric 2x2 game as a matrix: (my revenue, neighbour's revenue)."""
    A, B = np.asarray(game.A), np.asarray(game.B)
    prices = (f"{USUAL} EUR", f"{moved_price} EUR")
    w = max(len(p) for p in prices) + 2
    if title:
        print(title)
    print(" " * (w + 2) + "".join(f"{p:^14}" for p in prices) + "   <- neighbour")
    for i, p in enumerate(prices):
        print(f"{p:>{w}}  " + "".join(f"{f'({A[i, j]:g}, {B[i, j]:g})':^14}" for j in range(2)))
    print()

def nash_game(game):
    """The same game as a nashpy Game, to compute its Nash equilibria (pure and mixed)."""
    return nash.Game(np.asarray(game.A), np.asarray(game.B))


def describe(game, actions=("C", "D")):
    """Print my best answers and the Nash equilibria (pure and mixed) of a 2x2 game."""
    A = np.asarray(game.A)
    for j, other in enumerate(actions):
        best = [actions[i] for i in range(2) if A[i, j] == A[:, j].max()]
        print(f"  if the neighbour plays {other}, my best answer is {' or '.join(best)}")

    def play(sigma):                                  # (0, 1) -> "D",  (0.6, 0.4) -> "C 60 % / D 40 %"
        used = [(a, p) for a, p in zip(actions, sigma) if p > 1e-9]
        return used[0][0] if len(used) == 1 else " / ".join(f"{a} {p:.0%}" for a, p in used)

    g = nash_game(game)
    print("  Nash equilibria (me, neighbour) -> revenues:")
    for me, other in g.support_enumeration():
        r_me, r_other = g[me, other]
        print(f"    ({play(me)}, {play(other)}) -> ({r_me:g}, {r_other:g})")


# ---------------------------------------------------------------- calendars
CITY_WEEK = ["busy"] * 5 + ["quiet"] * 2      # active city: commuters on weekdays, quiet weekends
TOURIST_WEEK = ["quiet"] * 5 + ["busy"] * 2   # tourist town: quiet weekdays, busy weekends


def season(week, n_weeks=26):
    """A calendar: the list of day types for n_weeks repetitions of a week pattern."""
    return list(week) * n_weeks


# ---------------------------------------------------------------- a season
def play_season(me, neighbour, calendar, games=GAMES, noise=0, seed=0):
    """Play a whole season, day after day, with the game of each day.

    Before each day, both players get two attributes they can use in strategy():
    self.today (the type of today: "quiet" or "busy") and self.days (the types of past days).
    Returns an array (n_days x 2): the revenue of each day for me and for the neighbour.
    """
    rng = np.random.default_rng(seed)
    for p in (me, neighbour):
        p.reset()
        p.set_seed(seed)
        p.days = []
    result = np.zeros((len(calendar), 2))
    for t, day in enumerate(calendar):
        me.today = neighbour.today = day
        a1, a2 = me.strategy(neighbour), neighbour.strategy(me)
        if noise and rng.random() < noise:
            a1 = a1.flip()
        if noise and rng.random() < noise:
            a2 = a2.flip()
        me.update_history(a1, a2)
        neighbour.update_history(a2, a1)
        me.days.append(day)
        neighbour.days.append(day)
        result[t] = games[day].score((a1, a2))
    return result


def show_moves(me, neighbour, n_days=14):
    """After play_season: print the type of each day and the moves of both players."""
    days = "".join("B" if d == "busy" else "q" for d in me.days[:n_days])
    print(f"{'day (B=busy, q=quiet)':>24}  {days}")
    for p in (me, neighbour):
        print(f"{p.name:>24}  {''.join(a.name for a in p.history[:n_days])}")


def plot_season(result, names=("me", "neighbour"), ax=None, title=""):
    """Cumulative revenue of both renters over the season."""
    ax = ax or plt.subplots(figsize=(7, 3.5))[1]
    for k, style in enumerate(("-", "--")):
        ax.plot(np.cumsum(result[:, k]), style, lw=2.5, label=names[k])
    ax.set_xlabel("day")
    ax.set_ylabel("cumulative revenue (EUR)")
    ax.set_title(title)
    ax.legend()
    return ax


# ---------------------------------------------------------------- pricing policies
class Renter(axl.Player):
    """Base class of every pricing policy: an axelrod Player that also knows the calendar.
    - today: the type of the current day, "quiet" or "busy" (None before the season)
    - days:  the types of the past days, in the same order as self.history and opponent.history
    """
    def __init__(self):
        super().__init__()
        self.today = None
        self.days = []

    def reset(self):
        super().reset()
        self.today = None
        self.days = []

class Steady(Renter, axl.Cooperator):
    """Always the usual price (axelrod's Cooperator)."""
    name = "Steady"


class Opportunist(Renter, axl.Defector):
    """Always plays the day: undercuts on quiet days, surges on busy days (axelrod's Defector)."""
    name = "Opportunist"


class Reciprocal(Renter, axl.TitForTat):
    """Copies the neighbour's last move, whatever the day (axelrod's Tit For Tat)."""
    name = "Reciprocal"


class DayAware(Renter):
    """Surges on busy days; on quiet days, copies the neighbour's last quiet-day move."""
    name = "Day-aware"

    def strategy(self, opponent):
        if self.today == "busy":
            return D
        quiet_moves = [m for m, d in zip(opponent.history, self.days) if d == "quiet"]
        return quiet_moves[-1] if quiet_moves else C


class Mirror(Renter):
    """Copies the neighbour's last move on the same type of day (C the first time)."""
    name = "Mirror"

    def strategy(self, opponent):
        same_day = [m for m, d in zip(opponent.history, self.days) if d == self.today]
        return same_day[-1] if same_day else C


# ---------- GLOBAL POLICIES AND NEIGHBOURS

POLICIES = [Steady, Opportunist, Reciprocal, DayAware, Mirror]
NEIGHBOURS = [Steady, Opportunist, Reciprocal, DayAware]


# ---------------------------------------------------------------- decisions
def decision_table(policies, neighbours, calendar, noise=0, seed=0):
    """Mean revenue per day of each of my policies (rows) against each neighbour (columns)."""
    table = {N.name: [play_season(P(), N(), calendar, noise=noise, seed=seed)[:, 0].mean()
                      for P in policies] for N in neighbours}
    return pd.DataFrame(table, index=[P.name for P in policies]).round(1)


def plot_table(table, ax=None, title=""):
    """Heatmap of a decision table, with the values written in the cells."""
    ax = ax or plt.subplots(figsize=(7, 4.2))[1]
    im = ax.imshow(table.values, cmap="viridis")
    ax.set_xticks(range(table.shape[1]), table.columns, rotation=25, ha="right")
    ax.set_yticks(range(table.shape[0]), table.index)
    ax.set_xlabel("neighbour's policy")
    ax.set_ylabel("my policy")
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            v = table.values[i, j]
            ax.text(j, i, f"{v:.0f}", ha="center", va="center",
                    color="white" if v < table.values.mean() else "black")
    ax.set_title(title)
    plt.colorbar(im, ax=ax, label="EUR per day")
    return ax


def first_week_of(neighbour, me, week):
    """The neighbour's moves during one week, when I play the policy `me`."""
    n, m = neighbour(), me()
    play_season(m, n, week)
    return list(n.history)
