# builds 2x2 payoff matrices and solves the value function by Bellman updates
# state index s equals balls times 3 plus strikes
# returns v and mixed strategies x and y

import numpy as np

def build_Ms_payoff(v, p):
    # states 0..11 for b in 0..3 and s in 0..2
    Ms = [None] * 12
    for balls in range(4):
        for strikes in range(3):
            s = balls * 3 + strikes
            M = np.zeros((2, 2))
            # Ball Wait
            if balls + 1 == 4:
                val_bw = 1.0
            else:
                val_bw = v[(balls + 1) * 3 + strikes]
            # Ball Swing acts like a strike on the count
            if strikes + 1 == 3:
                val_bs = 0.0
            else:
                val_bs = v[balls * 3 + (strikes + 1)]
            # Strike Wait
            if strikes + 1 == 3:
                val_sw = 0.0
            else:
                val_sw = v[balls * 3 + (strikes + 1)]
            # Strike Swing gives HR with prob p else next is a strike
            if strikes + 1 == 3:
                cont = 0.0
            else:
                cont = v[balls * 3 + (strikes + 1)]
            val_ss = p * 4.0 + (1.0 - p) * cont

            M[0, 0] = val_bw
            M[0, 1] = val_bs
            M[1, 0] = val_sw
            M[1, 1] = val_ss
            Ms[s] = M
    return Ms


def solve_value_payoff(p, tol=1e-14, maxiter=20000):
    # value iteration using 2x2 saddle formulas or endpoint checks
    v = np.zeros(12)
    for _ in range(maxiter):
        v_new = v.copy()
        Ms = build_Ms_payoff(v, p)
        delta = 0.0
        for s in range(12):
            M = Ms[s]
            M00, M01, M10, M11 = M[0, 0], M[0, 1], M[1, 0], M[1, 1]
            D = (M00 - M01 - M10 + M11)
            if abs(D) < 1e-18:
                # degenerate case
                val0 = max(min(M00, M10), min(M01, M11))
                val = val0
            else:
                q = (M11 - M01) / D  # batter mix on columns
                if q <= 0.0 or q >= 1.0:
                    # pick endpoint on batter side
                    val0 = min(M01, M11)
                    val1 = min(M00, M10)
                    val = max(val0, val1)
                else:
                    f0 = q * M00 + (1.0 - q) * M01
                    f1 = q * M10 + (1.0 - q) * M11
                    val = min(f0, f1)
            v_new[s] = val
            delta = max(delta, abs(v_new[s] - v[s]))
        v = v_new
        if delta < tol:
            break
    return v


def compute_equilibrium_strategies(v, p, eps=1e-12):
    # return pitcher mix x and batter mix y for each state
    Ms = build_Ms_payoff(v, p)
    xs = np.zeros(12)
    ys = np.zeros(12)
    for s in range(12):
        M = Ms[s]
        M00, M01, M10, M11 = M[0, 0], M[0, 1], M[1, 0], M[1, 1]
        D = (M00 - M01 - M10 + M11)
        if abs(D) > eps:
            y = (M11 - M01) / D
            x = (M11 - M10) / D
            x = max(0.0, min(1.0, x))
            y = max(0.0, min(1.0, y))
        else:
            # endpoint fallback
            val0 = min(M01, M11)
            val1 = min(M00, M10)
            y = 1.0 if val1 >= val0 else 0.0
            f0 = y * M00 + (1.0 - y) * M01
            f1 = y * M10 + (1.0 - y) * M11
            if abs(f0 - f1) < 1e-12:
                x = 0.5
            else:
                x = 1.0 if f0 >= f1 else 0.0
        xs[s] = x
        ys[s] = y
    return xs, ys
