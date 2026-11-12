# Two bike renters

Two bike rental shops share the same street.  
Every morning, each one sets the price of the day. 
- On a quiet day, the temptation is to **undercut** the neighbour to attract the few customers.
- On a busy day, the temptation is to **raise** the price, since every bike will be rented anyway.

This book uses this situation to answer a concrete question:

> *I am a bike renter. What pricing policy should I adopt for the season, knowing that I do not control what my neighbour does?*

The tools are those of game theory (payoff matrices, repeated games, decision criteria, Bayesian updating) and the [axelrod](https://axelrod.readthedocs.io) library.

| Chapter | Question | What you do |
|---|---|---|
| 1. Two kinds of days | What game do the renters play on a given day? | build the payoff matrices from the assumptions |
| 2. A season on the same street | What happens when they meet every day, quiet or busy? | play a season, write two pricing policies |
| 3. Choosing a pricing policy | Which policy should a renter choose? | build a decision table, compare decision criteria |
| 4. Who is my neighbour? | What if the renter watches the neighbour first? | update a belief with Bayes' rule, decide again |

## How to work

- Read each chapter in order: each one relies on the previous ones.
- Exercises need **4 to 15 lines** of code.
- All the numbers come from a few assumptions written in `bikes.py`.

## The model in one table

| Assumption | Value |
|---|---|
| bikes per shop | 20 |
| prices | usual 15 EUR, undercut 10 EUR, surge 25 EUR |
| customers in the street | 20 on a quiet day, 60 on a busy day |
| at 25 EUR | only 60 % of the customers still rent |
| reputation | 12.5 EUR lost per customer who paid 25 EUR while next door charged 15 EUR; 5 EUR if both charge 25 EUR |
| moves | **C** = usual price; **D** = play the day (undercut if quiet, surge if busy) |

## Running the book

`pip install -r requirements.txt`, then `jupyter book start`, or VisualStudio Code, or [Colab](https://colab.research.google.com/).  
Keep `bikes.py` next to the notebooks.
