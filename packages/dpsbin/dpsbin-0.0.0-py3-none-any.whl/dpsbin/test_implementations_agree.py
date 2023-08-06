from dpsbin import _exact as exact, _monte as monte
from scipy.stats import wasserstein_distance
import pytest, numpy as np

@pytest.mark.parametrize('M, T', [
    [1, 1],
    [1, 2],
    [1, 3],
    [2, 1],
    [2, 2],
    [2, 3],
    [5, 3],
    [5, 6],
    [5, 7],
])
def test_exact_matches_simulation(M, T):
    a = exact.pmf(M, T)
    b = monte.pmf(M, T)

    assert wasserstein_distance(a, b) < 1e-2

@pytest.mark.parametrize('M, T, p', [
    [1, 1, 0.],
    [5, 7, 0.],
    [3, 8, .6],
    [10, 5, .2],
    [4, 4, 1.],
])
def test_zeros_match_simulation(M, T, p):
    a = exact.with_zeros(T, p, exact.pmf(M, T))
    b = monte.zero_pmf(M, T, p)[:T+1]

    assert wasserstein_distance(a, b) < 1e-2
