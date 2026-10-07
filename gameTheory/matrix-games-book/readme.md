# Matrix games with nashpy

Five two-player games, solved by hand and checked with [nashpy](https://nashpy.readthedocs.io).  
Each exercise is in a chapter: statement and matrix, questions with their solutions, and a Python cell that checks them with nashpy.

> **Key method: use of the indifference principle.**  
> In a mixed equilibrium, each player's probabilities make the **opponent** indifferent between their actions.  
> Equalising your **own** payoffs only works in **zero-sum** games.

**Nashpy compute all the equilibria from given matrices !**

```python
import numpy as np, nashpy as nash
# A is the payoff matrix from the player A point of view
# B is the payoff matrix from the player B point of view
game = nash.Game(A, B) # or nash.Game(A) for a zero-sum game
# list all equilibria, pure AND mixed
# list(game.support_enumeration())       
```

**Libraries**
You will need jupyter-book>=2, nashpy, numpy, matplotlib, ipykernel

- On your own computer, 
  - to install all : Run: `pip install -r requirements.txt`. 
  - to install just nashpy : Run: `pip install nashpy`.
  - Keep `myNashTools.py` next to the notebooks, and open them with  Visual Studio code, Anaconda, .....
  - Do not run the cell dedicated to Colab
- On Colab : 
  - install all the files in a folder on your google drive (ex. "Colab Notebooks/GameMatrix")
  - install nashLib and run the cell dedicated to Colab and check the result ! 
  Adapt the name of the path if it does'nt work.

