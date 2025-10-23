# Robot Baseball: full count maximization

## What did i cook?

This is my solution to Jane Street’s Robot Baseball puzzle. I'll throw a LaTeX write-up as an alternative to this too. The goal is to pick (p) so that the chance an at bat reaches a full count is as large as possible, under optimal mixed play by both players. The puzzle rules set the stage game on each pitch and define walk, strikeout, and home run payoffs. 

The result I report is
(q_{\max}=0.2959679934) at (p\approx 0.2269732296).
This is the number in my notes and in the cleaned write up. 

## Puzzle in one paragraph

On each pitch the pitcher secretly chooses Ball or Strike and the batter secretly chooses Wait or Swing. Ball with Wait adds a ball. Strike with Wait adds a strike. Ball with Swing adds a strike. Strike with Swing gives a home run with probability (p) for payoff four, otherwise it adds a strike. An at bat ends at four balls for payoff one, or three strikes for payoff zero, or on a home run for payoff four. We want the value of (p) that makes full count most likely under optimal mixed strategies, and we want that peak probability to ten decimals. 

## Method

I solve a small stochastic zero sum game.

* For fixed (p), set the batter payoff matrix at each non terminal count ((b,s)). The off diagonal entries match, which simplifies the saddle point. From that I compute the stage value (V(b,s)). 
* From the converged (V) I extract the equilibrium mixes at each state. Those mixes define a Markov chain on counts. I then solve a linear system for the probability of ever hitting ((3,2)). 
* I view (q(0,0)) as a function of (p). I scan a coarse grid to bracket the peak, then refine with a golden section search. 

This pipeline is the one in your PDF notes and it is the same as the short write up. 

## Repo layout

* `solver.py` computes (V(b,s)) for a given (p) and the per state mixed strategies
* `hitting_prob.py` computes the hit full count probability for a given (p)
* `optimisation.py` maximizes (q(0,0)) over (p\in[0,1])

These files mirror the sections in your notes and produce the same numbers that appear in your write up. 

## How to run the code

1. Make sure Python and NumPy are installed.
2. Run `python optimisation.py`.
3. The script prints the argmax (p) and the peak (q).

The target numbers you should see are
(q_{\max}=0.2959679934) at (p\approx 0.2269732296). 

## Key modeling choices

* Terminal values: (V(4,s)=1), (V(b,3)=0). A swing at a strike pays (4) with chance (p) and otherwise moves to ((b,s+1)). 
* Per pitch game: rows are Ball and Strike, columns are Wait and Swing. The off diagonal entries match, so in interior cases the mixes coincide at that state. 
* Hit probability system: with mixes ((x,y)) at state ((b,s)),
  (P(\text{Ball,Wait})=xy),
  (P(\text{Ball,Swing})=x(1-y)),
  (P(\text{Strike,Wait})=(1-x)y),
  (P(\text{Strike,Swing,no HR})=(1-x)(1-y)(1-p)),
  (P(\text{Strike,Swing,HR})=(1-x)(1-y)p).
  Set (q(3,2)=1), and set all other absorbing states to zero, then solve for (q(0,0)). 

## Checks

I verified the peak by three simple passes that agree within tight tolerances: value iteration with analytic (2\times2) saddle at each state, a grid scan in (p), and a golden section search near the peak. The numbers line up with the write up. 

## Result

The maximal chance that an at bat reaches full count is
(q_{\max}=0.2959679934)
at
(p\approx 0.2269732296). 

