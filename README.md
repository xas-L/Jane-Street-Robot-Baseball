# Robot Baseball full count maximization

## What this is

This repo solves the Jane Street Robot Baseball puzzle. The goal is to choose p so that the chance an at bat reaches a full count is as large as possible under optimal mixed play by both players.

Result

$$
q_{\max} = 0.2959679934 \quad \text{at} \quad p \approx 0.2269732296.
$$

## Puzzle in one paragraph

On each pitch the pitcher secretly chooses Ball or Strike and the batter secretly chooses Wait or Swing. Ball with Wait adds a ball. Strike with Wait adds a strike. Ball with Swing adds a strike. Strike with Swing gives a home run with probability p and payoff four otherwise it adds a strike. The at bat ends at four balls with payoff one or three strikes with payoff zero or on a home run with payoff four. We want the value of p that makes full count most likely under optimal mixed strategies and we want that peak probability to ten decimals.

## Method

I model a small stochastic zero sum game.

* For fixed p I build the 2 by 2 batter payoff at each nonterminal count b comma s. The off diagonal entries match. That makes the saddle simple. This gives the state value V of b comma s.
* From the converged V I get the equilibrium mixes at each state. These mixes define a Markov chain on counts. I then solve a linear system for the chance to ever hit b comma s equals three comma two.
* I treat q at zero comma zero as a function of p. I scan a grid then run a golden section search near the peak.

## Repo layout

* solver.py computes V of b comma s and the mixed strategies
* hitting_prob.py computes the hit full count probability for a fixed p
* optimize.py maximizes q at zero comma zero over p in the closed interval zero to one

## How to run

1. Install Python and NumPy.
2. Run `python optimize.py`.
3. You should see the numbers below.

$$
q_{\max} = 0.2959679934 \quad \text{at} \quad p \approx 0.2269732296.
$$

## Key modeling choices

Terminal values

$$
V(4,s) = 1, \qquad V(b,3) = 0.
$$

Strike Swing payoff at a strike count

$$
\text{Strike Swing value} = p \cdot 4 + (1-p) \cdot V(b,s+1).
$$

Per pitch game payoff matrix for the batter at state b comma s with rows Ball then Strike and columns Wait then Swing

$$
M \;=\;
\begin{pmatrix}
V(b+1,s) & V(b,s+1) \\
V(b,s+1) & p \cdot 4 + (1-p)\,V(b,s+1)
\end{pmatrix}.
$$

Hit full count probability with mixes x for pitcher Ball and y for batter Wait at state b comma s

$$
P(\text{Ball, Wait}) = x y
$$

$$
P(\text{Ball, Swing}) = x (1-y)
$$

$$
P(\text{Strike, Wait}) = (1-x) y
$$

$$
P(\text{Strike, Swing, no HR}) = (1-x)(1-y)(1-p)
$$

$$
P(\text{Strike, Swing, HR}) = (1-x)(1-y)p
$$

Set the boundary conditions for the hit full count system

$$
q(3,2)=1, \qquad q(4,s)=0, \qquad q(b,3)=0.
$$

Then solve for

$$
q(0,0).
$$

## Result

$$
q_{\max} = 0.2959679934 \quad \text{at} \quad p \approx 0.2269732296.
$$
