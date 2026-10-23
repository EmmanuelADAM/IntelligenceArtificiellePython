# Negotiating agents: a carpool price

Alice drives tomorrow to Valenciennes; Bob needs a ride. On a carpool app, a software agent negotiates the price
for each of them, offer after offer, before the departure.

This short book follows the last part of module 5 (*Link with multi-agent negotiation*) and answers one question:

> *How should an agent concede when it knows neither the patience nor the limit price of the other?*

| Chapter | Question | What you do |
|---|---|---|
| 1. The protocol | How do two agents negotiate a price? | write strategies as small functions, run a negotiation |
| 2. Boulware or Conceder | Should an agent concede early or late? | time-dependent strategies, risk of breakdown |
| 3. Tit-for-Tat and Distance | What if the agent watches the other? | reciprocity, conceding fast costs |

## The model in one table

| | Alice (driver) | Bob (passenger) |
|---|---|---|
| first offer | asks 18 EUR | offers 4 EUR |
| limit | never less than 4 EUR (her detour) | never more than 18 EUR (the train) |
| gain at price $p$ | $p - 4$ | $18 - p$ |

Protocol: 10 rounds; at each round both agents send an offer; deal as soon as the offers cross (price = middle); no deal at the departure: both gain 0.

## How to work

- A **strategy** is a plain function `strategy(r, T, mine, theirs)` that returns the next offer: no class needed.
- Exercises need **3 to 10 lines** of code. Try first; the solution is in the cell below (folded in the book).
- `carpool.py` contains the negotiation loop (`negotiate`), a plot (`show`) and the strategies of the course.

## Running the book

you just need the small library carpool.py to set next to the notebooks, and the classicals numpy and matpolib.
