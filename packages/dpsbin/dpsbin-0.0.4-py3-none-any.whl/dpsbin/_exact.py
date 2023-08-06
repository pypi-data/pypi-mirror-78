import numpy as np

def pmf(M: int, T: int) -> np.array:
    """Computes chance of stopping after k rolls of 1dM trying to reach total T

    Args:
        M: positive integer, die roll from 1 -> M (inclusive)
        T: non-negative integer, total we want to meet or exceed

    Returns:
        An array of probabilities with shape (T+1,)
        rtn[k] == <chance of stopping after roll k>

    Notes:
        Argument validation is the responsibility of the caller.

    Design:
        Let X be a random variable with non-negative integer values, and
        let p(k) := Prob(X = k) be its probability mass function. Let
        f(X, T, k) be the chance that the following function outputs k:

            ```
            def simulate(X, T):
                t, n = 0, 0
                while t < T:
                    t, n = t+X(), n+1
                return n
            ```

        To compute f we break the single event (a simulation) into two
        pieces:
            (1) We first sample the random variable X and achieve some
                value less than T.
            (2) We then meet or exceed T only after exactly k-1 additional
                samples.

        Note that event (2) depends on the exact value achieved in (1). In
        general we find the following recursive relationship (we relied on
        k>=1 in our derivation, and that is actually essential for the
        following relationship to hold, so k==0 and k==1 need to be
        separately computed; thankfully those are easy to derive).

            ```
            f(X, T, k) = sum(p(r)*f(X, T-r, k-1) for r in range(T))
            ```

        As far as I can tell this is hard to simplify for an arbitrary pmf,
        but a useful class of random variables is those which are uniform
        from 1->M (a die roll). In such a case, p(r) is just the constant
        1/M, and instead of actually computing each of those convolutions
        we can get away with a rolling window sum.

        The solution then is essentially a dynamic programming problem from
        that recursive definition. Create a T+1 by k+1 table (note that k==T),
        fill in columns 0 and 1 with the base cases, and compute column j
        by looking at column j-1. Your solution is then the last row of the
        table.

        Here we make two additional modifications to take advantage of
        available numpy primitives and to allow for use in certain kinds of
        resource-constrained environments:
            (1) Let f(r) be some function and s(r)=sum(map(f, range(r+1))),
                then sum(map(f, range(z+1, r+1))) == f(r) - f(z). We exploit
                this fact to compute rolling window sums by first calling
                np.cumsum and then subtracting after an appropriate alignment.
            (2) Our solution to this problem has O(T^2) time complexity, but
                strictly speaking we don't ever need the entire O(T^2) table.
                Under the assumption that most callers only care about some
                small subset of all possible T values, we allocate an O(T)
                buffer and over-write it as we conceptually move from one
                column to the next in the dynamic programming problem. Since
                we then don't have the last row of the table to return, we
                also allocate an O(T) array where we store return values.
    """

    #
    # If the total is 0, we always achieve that in 0 rolls.
    #
    if not T:
        return np.array([1.], dtype=np.longdouble)

    #
    # If the total is positive, we can't possibly get there in
    # 0 rolls, so rtn[0]==0. All other values will be over-written.
    #
    rtn = np.empty(T+1, dtype=np.longdouble)
    rtn[0] = 0.
    buff = np.zeros(T+1, dtype=np.longdouble)

    #
    # The base case k==1. buff[i] is the chance that a single roll
    # meets or exceeds i when 0 rolls would not. Note especially that
    # this means buff[0]==0.
    #
    # Use max(-1, M-T) to make sure we aren't
    # trying to shove something too big into our buffer.
    #
    buff[1:M+2] = np.arange(M, max(-1, M-T), -1)/M

    #
    # We just computed the base case k==1, and we need to shove its
    # results into our return vector before we move further to the right.
    #
    rtn[1] = buff[-1]

    #
    # Move right from column 2 to column T in our dynamic programming problem.
    #
    for k in range(2, T+1):
        #
        # Recall that we're computing values like
        #   sum(col[k]/M for k in some_range)
        # It's just as easy to pre-compute the division and give
        # numpy a fighting chance to perform that in-place.
        #
        buff /= M

        #
        # This is the tricky bit. Assuming M>T we're simply saying the
        # i-th row is the cumulative sum up to row i-1. Afterward though,
        # for every row where we have to start rolling the total off we
        # subtract the same cumulative sum at an appropriate offset.
        #
        # To get an intuition as to the correctness, notice that after the
        # cumsum operation, "new buff[-1]" will contain
        # "old sum(buff[:-1])". At that location we then subtract
        # "old sum(buff[:-M-1])". I.e., "new buff[-1]" now contains
        # "old sum(buff[-M-1:-1])" -- the M rows preceding the last row.
        #
        # It's probably also good to work those indices out for yourself
        # and to examine our test cases if anything looks fishy.
        np.cumsum(buff[:-1], out=buff[1:])
        buff[M:] -= buff[:-M]

        #
        # Buffer is now exactly column k from our dynamic programming problem.
        # Store its last element in our return vector before we over-write it.
        #
        rtn[k] = buff[-1]

    return rtn

def _binarr(k: int) -> np.array:
    """[comb(k-1, k-r) for r in range(1, k+1)]

    Args:
        k: non-negative integer

    Notes:
        Argument validation is the responsibility of the caller.
    """
    if not k:
        return np.array([], dtype=np.longdouble)

    r = np.arange(1, k, dtype=np.longdouble)
    multiplicand = np.empty(k, dtype=np.longdouble)
    multiplicand[0] = 1.
    multiplicand[1:] = (k-r)/r
    return np.cumprod(multiplicand, out=multiplicand)

def with_zeros(k: int, p: float, pma: np.array) -> np.array:
    """Converts a probability mass array for positive random variables to what would have been generated with zero allowed.

    Args:
        pma: non-negative 1D numpy array summing to 1.0
        p: float in [0, 1] (inclusive), probability of a zero
        k: max number of turns for which we'll return probabilities

    Returns:
        non-negative numpy array with shape (k+1,) summing to at most 1.0.
        rtn[i] is the chance that we can stop after roll i

    Notes:
        Argument validation is the responsibility of the caller.

    Design:
        The special case where we have a chance to hit and then have a
        different distribution of positive values of damage that might
        apply is common enough that we want to give it special treatment.
        Doing so is especially convenient because in the absence of 0 as
        an option, other routines have a bounded return size and can be
        optimized thusly. With 0s we need to hide or expose a method for
        truncating the usually infinite stream of probabilities.

        The underlying idea is that we can decouple the chance of a 0 from
        the number of non-zero turns and convolve the probabilities to
        generate our new probability mass array. In particular, let
        p represent the probability of a zero, f(x) the chance that
        we need exactly x non-zero rolls to reach our goals, and g(x)
        the chance that we need exactly x rolls to reach our goals. Then

            ```
            def g(x):
                return sum(f(r)*comb(x-1, x-r)*(1-p)**r*p**(x-r)
                    for r in range(x+1))
            ```

        is a valid identity, give or take the boundary cases. At the
        expense of some floating point error though, it's wasteful to
        repeat all of those combinatorial operations when computing
        an entire probability mass array. Our approach is to

        (1) Compute an array

            ```
            [f(r)*comb(x-1, x-r)*(1-p)**r*p**(x-r)
                    for r in range(x+1)]
            ```
        (2) In a loop, sum the array and apply an element-wise scaling
            factor to transform it into the same array corresponding to
            the next row.

    Todo:
        If L==len(pma) then this should be achievable in O(k * L) time. We're
        taking some shortcuts that bring it up to O(k^2). For typical use we
        roughly expect L<k<10*L, so this is just a small, constant-factor
        slowdown no worse than what we induce using numpy rather than a
        dedicated low-level implementation, but it'd still be nice to shore up.
    """

    if k==0:
        return pma[:1]

    rtn = np.zeros(k+1, dtype=np.longdouble)

    #
    # If it's possible to achieve the goal with 0 actions and if actions are
    # the only random variable of interest, then it is _always_ possible to
    # achieve the goal with 0 actions.
    #
    if pma[0]:
        rtn[0] = 1.
        return rtn

    #
    # We lazily examine pma[r] to evaluate probabilities of interest. Reshape
    # the probability mass array to fit our needs and make the rest of the
    # routine nicer.
    #
    if len(pma)<k+1:
        pma = np.pad(pma, (0, k+1-len(pma)))
    elif len(pma)>k+1:
        pma = pma[:k+1]

    #
    # As a shortcut we divide by p later, so we need to do _something_ now. As
    # it happens, if p==0 then the new distribution is identical to the old, so
    # just return its information (which has already been resized to the
    # shape our callers are expecting)
    #
    if p==0:
        return pma

    #
    # There's a recursive relationship between comb(k-1, k-r) and
    # comb((k-1)-1, (k-1)-r). Exploit that with cumprod to generate the last
    # row of point probabilities.
    #
    buff = np.cumprod(np.full(k, (1-p)/p))*p**k*_binarr(k)*pma[1:]
    rtn[-1] = np.sum(buff)
    for i in range(2, k):
        #
        # Note that as we iterate through this loop we're looking at less
        # and less of the tail of buff. That memory is still occupied, so
        # be careful not to use it in any calculations.
        #
        a = k+1-i
        buff[:1-i] =(a-np.arange(a, dtype=np.longdouble))/(a)/p*buff[:1-i]
        rtn[-i] = np.sum(buff[:1-i])

    #
    # The recusive relationship we're using between rows has singularities
    # when we get this far. Thankfully these two elements don't have much
    # going on.
    #
    rtn[0] = 0.
    rtn[1] = pma[1]*(1-p)

    return rtn

__all__ = ['pmf', 'with_zeros']
