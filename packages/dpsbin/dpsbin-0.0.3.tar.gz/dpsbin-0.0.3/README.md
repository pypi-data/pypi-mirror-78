# dpsbin

Computes the probability mass function for an extended negative binomial distribution essential for accurate DPS calculations in a variety of turn/tick-based games.


# Description

Common methods for estimating how long it takes to finish off an opponent in typical hack-and-slash games are inaccurate due to factors like overkill. Those crude calculations are often good enough, but in case they're not you can turn to this library to get an exact answer.

# Installation

dpsbin requires Python 3 or greater and is available on PyPI.

```
python -m pip install dpsbin
```

Alternatively, the latest version can be easily downloaded and installed locally.
```
git clone https://github.com/hmusgrave/dpsbin.git
cd dpsbin
python -m pip install -e .
```

# Using dpsbin

The only notable entry point is `dpsbin.pmf`. Suppose you want to know how many times you'll have to roll a 6-sided die to reach a total of 40 or more.

```
import dpsbin, numpy as np, math

probs = dpsbin.pmf(6, 40)

# probs[k] is the probability you need to roll k times.
assert math.isclose(np.sum(probs), 1)

# easily find out how many rolls you'll need on average.
avg = np.dot(probs, np.arange(len(probs)))

# if you have a 90% chance to miss and not deal the 1d6 damage then
# you can use with_zeros() to translate the old probability mass array
# into one that accounts for zeros. Truncate to only considering up
# to 80 rolls.
hard_to_hit = dpsbin.with_zeros(80, .9, probs)
```
