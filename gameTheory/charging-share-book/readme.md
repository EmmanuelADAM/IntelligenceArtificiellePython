# Sharing a charging station

Alice owns a house with a **22 kW wallbox** in her yard; she works during the day and mostly uses her electric car at the weekend.  
Bob, her neighbour, is a home nurse: he chains short visits in the district and often comes home between two visits.  
He has just bought an electric car; he has not the possibility to install a charger.  
Bob asks Alice to share her charger.  
They must agree on the terms: the price of the kWh (Alice's tariff plus a margin), how often Bob can charge, when, how long in advance he must book, and for how long the agreement holds.

This practical session follows the [tutorial negotiation book](https://github.com/EmmanuelADAM/IntelligenceArtificiellePython/tree/master/gameTheory/carpool-agents-book) (carpool), and answers one question:

> *How can two agents find a good agreement on several issues, when each one only knows its own preferences?*

| Part | Question | What you do | 
|---|---|---|
| 1. One issue: the price | Which price, between Alice's cost and the public charger? | ZOPA, Nash price, time-dependent agents | 
| 2. Several issues | What is a good package? | scoring sheets, Pareto frontier, Nash package, logrolling | 
| 3. Agents with several issues | How do agents exchange packages? | blind agent vs trade-off agent | 
| 4. Five issues   | And with two more issues (notice, duration)? | non-monotonic preferences, options both prefer, your own agent | 

---

## The model in one table

| Issue | Options | Alice (owner) | Bob (user) |
|---|---|---|---|
| margin over Alice's tariff (EUR/kWh) | 0.00 ... 0.14 | high | low (public charger: 0.35 EUR/kWh) |
| charges per month | 4, 6, 8, 10, 12 | few | many (he needs about 8) |
| time slot | 7h-18h, 18h-22h, 22h-7h | the day (she is at work); the night, but noise; not the evening (power peak) | the day (between two visits); then the night |
| notice | 0 h, 2 h, 12 h, 24 h, 48 h | long (24 h) | short, but not none (2 h) |
| duration | 1, 3, 6, 12 months | short (3 months) | long (12 months) |

Bob pays Alice's tariff of the slot (0.20 EUR/kWh during the day and the evening, 0.16 at night) plus the margin.

Each agent scores a package with a **private scoring sheet** (points per option, `ALICE_SHEET` and `BOB_SHEET` in `charging.py`)
and refuses any package below its **reservation score** (no deal: Alice keeps her charger, Bob uses the public charger).

---
## How to work

- A **strategy** is a plain function `strategy(r, T, mine, theirs)`: no class needed.
  In chapter 1 it returns a price; in chapters 3 and 4 it returns a **package** (a dict, e.g. `{"margin": 0.10, "charges": 10, "slot": "7h-18h"}`).
- An agent only uses **its own** sheet: Alice's strategy never reads `BOB_SHEET`.
- `charging.py` contains the scoring sheets, the negotiation loops (`negotiate_price`, `negotiate`), the plots and the strategies of the course.


## About the numbers

- Regulated tariff in France (August 2026): about 0.20 EUR/kWh (base option), 0.16 EUR/kWh in off-peak hours.
- The public charger at 0.35 EUR/kWh is an assumption of the scenario (public prices vary a lot).
- A charge of 25 kWh takes a little more than 1 h at 22 kW: Bob can charge between two visits.
- Bob drives about 1200 km per month: about 200 kWh, i.e. 8 charges of 25 kWh.

## Running the book

You just need the small library `charging.py` next to the notebooks, and the classical numpy and matplotlib.
