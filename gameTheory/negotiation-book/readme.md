# Negotiation for mobility


> *Two agents could both gain from an agreement. Which agreement will they reach, which one is "fair", and what gives one of them more bargaining power?*

| Chapter | Question | What you do |
|---|---|---|
| 1. Sharing a ride | How much should the passenger pay the driver? | build $(S, d)$, compute the Nash solution, add an outside option |
| 2. An eco-bonus for electric bikes | Who really benefits from a subsidy? | compare Nash and Kalai-Smorodinsky, add a price cap, a risk-averse buyer |
| 3. A shared loading bay | How to share three delivery slots? | isolated agreements, social welfare, lotteries (alternating days) |
| 4. Offers in turn | What price for the ride when Alice and Bob make offers in turn? | ultimatum game, Rubinstein model, patience, complete information |

## Content

- Books 1 to 3 are the cooperative approach, 4  the non-cooperative one.
- Exercises need **3 to 8 lines** of code. Try first; an example of  solution is in the cell below (folded in the book).
- `bargain.py` contains generic little functions (compute equilibirum, pareto points, ...) and specific ones, dedicated to the exercises, with predefined values (you can cut and paste the functions to try other values) .

## The notations (like in lectures)

| Notation | Meaning |
|---|---|
| $u_1, u_2$ | gain (utility) of agent 1 and agent 2 |
| $S$ | set of pairs $(u_1, u_2)$ reachable by an agreement |
| $d = (d_1, d_2)$ | disagreement point: what each agent gets if the negotiation fails |
| $f(S, d)$ | a solution: the agreement chosen in $S$ |
| $a = (a_1, a_2)$ | ideal point: best utility each agent can hope for while the other still accepts |
| $\delta_i$ | discount factor of agent $i$: a share $x$ one round later is worth $\delta_i\,x$ now |

## Running the book

`pip install -r requirements.txt` on your local machine, or install : 
-numpy, pandas, matplotlib 

**Keep `bargain.py` next to the notebooks.**  
(cf the previous notebooks to see how to connect your drive to the books)

