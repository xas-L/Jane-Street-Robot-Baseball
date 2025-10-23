# builds the absorption system and solves for q at state 0 0
# full count state is index 11
# walk out and homerun are absorbing and give zero to this probability

import numpy as np
from solver import solve_value_payoff, compute_equilibrium_strategies

def compute_q_given_p(p):
    v = solve_value_payoff(p)
    xs, ys = compute_equilibrium_strategies(v, p)

    unknown_idx = [s for s in range(12) if s != 11]
    m = len(unknown_idx)
    A = np.zeros((m, m))
    b = np.zeros(m)

    for i, s in enumerate(unknown_idx):
        x = xs[s]
        y = ys[s]
        probs = {}
        probs['bw'] = x * y
        probs['bs'] = x * (1.0 - y)
        probs['sw'] = (1.0 - x) * y
        probs['ss'] = (1.0 - x) * (1.0 - y)

        trans = {}
        def add(t, pb):
            trans[t] = trans.get(t, 0.0) + pb

        balls = s // 3
        strikes = s % 3

        # Ball Wait
        if balls + 1 == 4:
            add('walk', probs['bw'])
        else:
            ns = (balls + 1) * 3 + strikes
            add('full' if ns == 11 else ns, probs['bw'])

        # Ball Swing counts as a strike on the count
        if strikes + 1 == 3:
            add('out', probs['bs'])
        else:
            ns = balls * 3 + (strikes + 1)
            add('full' if ns == 11 else ns, probs['bs'])

        # Strike Wait
        if strikes + 1 == 3:
            add('out', probs['sw'])
        else:
            ns = balls * 3 + (strikes + 1)
            add('full' if ns == 11 else ns, probs['sw'])

        # Strike Swing splits into HR and no HR
        add('homerun', probs['ss'] * p)
        if strikes + 1 == 3:
            add('out', probs['ss'] * (1.0 - p))
        else:
            ns = balls * 3 + (strikes + 1)
            add('full' if ns == 11 else ns, probs['ss'] * (1.0 - p))

        A[i, i] = 1.0
        rhs = 0.0
        for target, prob in trans.items():
            if target == 'full':
                rhs += prob
            elif target in ('walk', 'out', 'homerun'):
                pass
            else:
                j = unknown_idx.index(target)
                A[i, j] -= prob
        b[i] = rhs

    h = np.linalg.solve(A, b)
    q00 = h[unknown_idx.index(0)]
    return q00, v, xs, ys
