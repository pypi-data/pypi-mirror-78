import numpy as np
from random import randint, random
from math import inf

def pmf(M: int, T: int, trial_count: int=10_000) -> np.array:
    """Computes chance of stopping after k rolls of 1dM trying to reach total T

    Args:
        M: positive integer, die roll from 1 -> M (inclusive)
        T: non-negative integer, total we want to meet or exceed

    Kwargs:
        trial_count: positive integer (default 10_000), number of
        simulations used to estimate result probabilities.
        Bigger values give better results but take more time.

    Returns:
        An array of probabilities with shape (T+1,)
        rtn[k] == <chance of stopping after roll k>

    Notes:
        Argument validation is the responsibility of the caller.

    Design:
        This is intended to be a reference implementation to which
        other methods whose correctness is non-obvious can be compared.
        The use of sequence accelerators and other such techniques should
        be relegated to other implementations.
    """
    def simulate():
        t, n = 0, 0
        while t < T:
            t, n = t+randint(1, M), n+1
        return n

    rtn = np.zeros(T+1)
    for _ in range(trial_count):
        rtn[simulate()] += 1

    return rtn/np.sum(rtn)

def zero_pmf(M: int, T: int, p_zero: float, trial_count: int=10_000) -> np.array:
    """Simulates rolling 1dM with a p_zero chance of failure till a total of T is reached

    Args:
        M: positive integer, max die roll
        T: non-negative integer, total we're attempting to reach
        p_zero: float in [0, 1] (inclusive)

    Kwargs:
        trial_count: positive integer (default 10_000), bigger is better
            and slower
    """
    def simulate():
        if p_zero==1:
            return inf
        t, n = 0, 0
        while t < T:
            t, n = t+randint(1,M)*(random()>p_zero), n+1
        return n

    rtn = [0]*(T+1)
    for _ in range(trial_count):
        v = simulate()
        if v==inf:
            continue
        if v >= len(rtn):
            rtn += [0]*max(v+1-len(rtn), len(rtn))
        rtn[v] += 1
    rtn = np.array(rtn)
    s = np.sum(rtn)

    if s:
        return rtn/s
    return rtn
