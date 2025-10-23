# golden section search for the peak
# prints the p that maximizes q and the max q

import numpy as np
from hitting_prob import compute_q_given_p

def golden_maximize(f, a, b, tol=1e-12, maxiter=80):
    gr = (np.sqrt(5.0) - 1.0) / 2.0
    c = b - gr * (b - a)
    d = a + gr * (b - a)
    fc = f(c)
    fd = f(d)
    for _ in range(maxiter):
        if abs(b - a) < tol:
            break
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = f(d)
    p_best = 0.5 * (a + b)
    return p_best, f(p_best)

if __name__ == "__main__":
    p_opt, q_at_opt = golden_maximize(lambda p: compute_q_given_p(p)[0], 0.0, 1.0)
    q_final, _, _, _ = compute_q_given_p(p_opt)
    print("p_opt =", p_opt)
    print("q_max =", q_final)
