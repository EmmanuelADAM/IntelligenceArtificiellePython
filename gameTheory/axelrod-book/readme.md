# Repeated matrix games with axelrod

In the [nashpy](https://nashpy.readthedocs.io) book, a matrix game is played **once**.  
Here the same 2×2 matrix is played **many times** by the same players, using the
[axelrod](https://axelrod.readthedocs.io) library.   
A *strategy* is then a rule:
"what do I play, given what happened before?".

| Exercise | Question | Main objects |
|---|---|---|
| 1. Matches | What happens when two strategies meet repeatedly? | `axl.Game`, `axl.Match`, `axl.Player` |
| 2. Tournaments | Which strategy does best against all the others? | `axl.Tournament`, `axl.Plot` |
| 3. Evolution | Which strategies survive in a population? | `axl.MoranProcess`, `axl.Ecosystem` |

Each exercise alternates short demonstrations and questions.  
**Every question needs 4 to 10 lines of code.**   
The solution is in the cell just below (folded in the book).

> **Key idea.**  
> In a 2×2 symmetric game, axelrod names the two actions `C` and `D`
> and the payoffs `R` (C,C), `S` (C,D), `T` (D,C), `P` (D,D).
> Changing these four numbers turns the prisoner's dilemma into a stag hunt or a game of chicken.

Use of axelod library is relatively simple.  
> Exemple for a matrix where r=3, s=0, t=5 and p=1 and two strategies TitForTat and Defect that compete for 10 turns

```python
import axelrod as axl
game = axl.Game(r=3, s=0, t=5, p=1)                       # the prisoner's dilemma
match = axl.Match((axl.TitForTat(), axl.Defector()), turns=10, game=game)
match.play(); match.final_score()
```

**Libraries**
You will need jupyter-book>=2, axelrod>=4.13, numpy, matplotlib, ipykernel

- On your own computer, 
  - to install all :Run: `pip install -r requirements.txt`. 
  - to install just axelrod: Run: `pip install axelrod``.
  - Keep `myIGTools.py` next to the notebooks, and open them with  Visual Studio code, Anaconda, .....
  - Do not run the cell dedicated to Colab
- On Colab : 
  - install all the files in a folder on your google drive (ex. "Colab Notebooks/IterativeGames")
  - install axelrod and run the cell dedicated to Colab and check the result ! 
  Adapt the name of the path if it does'nt work.  
  _Do the same with the notebook relative to evolution_


