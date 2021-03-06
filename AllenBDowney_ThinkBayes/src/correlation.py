"""This file contains code used in "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import math
import random

from src import thinkstats


def covariance(xs, ys, mux=None, muy=None):
    """Computes Cov(X, Y).

    Args:
        xs: sequence of values
        ys: sequence of values
        mux: optional float mean of xs
        muy: optional float mean of ys

    Returns:
        Cov(X, Y)
    """
    if mux is None:
        mux = thinkstats.mean(xs)
    if muy is None:
        muy = thinkstats.mean(ys)

    total = 0.0
    for x, y in zip(xs, ys):
        total += (x-mux) * (y-muy)

    return total / len(xs)


def correlation(xs, ys):
    """Computes Corr(X, Y).

    Args:
        xs: sequence of values
        ys: sequence of values

    Returns:
        Corr(X, Y)
    """
    xbar, varx = thinkstats.meanAndVariance(xs)
    ybar, vary = thinkstats.meanAndVariance(ys)

    corr = covariance(xs, ys, xbar, ybar) / math.sqrt(varx * vary)

    return corr


def serialCorr(xs):
    """Computes the serial correlation of a sequence."""
    return correlation(xs[:-1], xs[1:])


def spearmanCorr(xs, ys):
    """Computes Spearman's rank correlation.

    Args:
        xs: sequence of values
        ys: sequence of values

    Returns:
        float Spearman's correlation
    """
    xranks = mapToRanks(xs)
    yranks = mapToRanks(ys)
    return correlation(xranks, yranks)


def leastSquares(xs, ys):
    """Computes a linear least squares fit for ys as a function of xs.

    Args:
        xs: sequence of values
        ys: sequence of values

    Returns:
        tuple of (intercept, slope)
    """
    xbar, varx = thinkstats.meanAndVariance(xs)
    ybar, vary = thinkstats.meanAndVariance(ys)

    slope = covariance(xs, ys, xbar, ybar) / varx
    inter = ybar - slope * xbar

    return inter, slope


def fitLine(xs, inter, slope):
    """Returns the fitted line for the range of xs.

    xs: x values used for the fit
    slope: estimated slope
    inter: estimated intercept
    """
    fxs = min(xs), max(xs)
    fys = [x * slope + inter for x in fxs]
    return fxs, fys


def residuals(xs, ys, inter, slope):
    """Computes residuals for a linear fit with parameters inter and slope.

    Args:
        xs: independent variable
        ys: dependent variable
        inter: float intercept
        slope: float slope

    Returns:
        list of residuals
    """
    res = [y - inter - slope*x for x, y in zip(xs, ys)]
    return res


def coefDetermination(ys, res):
    """Computes the coefficient of determination (R^2) for given residuals.

    Args:
        ys: dependent variable
        res: residuals

    Returns:
        float coefficient of determination
    """
    ybar, vary = thinkstats.meanAndVariance(ys)
    resbar, varres = thinkstats.meanAndVariance(res)
    return 1 - varres / vary


def mapToRanks(t):
    """Returns a list of ranks corresponding to the elements in t.

    Args:
        t: sequence of numbers

    Returns:
        list of integer ranks, starting at 1
    """
    # pair up each value with its index
    pairs = enumerate(t)

    # sort by value
    sorted_pairs = sorted(pairs, key=lambda pair: pair[1])

    # pair up each pair with its rank
    ranked = enumerate(sorted_pairs)

    # sort by index
    resorted = sorted(ranked, key=lambda trip: trip[1][0])

    # extract the ranks
    ranks = [trip[0]+1 for trip in resorted]
    return ranks


def correlatedGenerator(rho):
    """Generates standard normal variates with correlation.

    rho: target coefficient of correlation

    Returns: iterable
    """
    x = random.gauss(0, 1)
    yield x

    sigma = math.sqrt(1 - rho**2);
    while True:
        x = random.gauss(x * rho, sigma)
        yield x


def correlatedNormalGenerator(mu, sigma, rho):
    """Generates normal variates with correlation.

    mu: mean of variate
    sigma: standard deviation of variate
    rho: target coefficient of correlation

    Returns: iterable
    """
    for x in correlatedGenerator(rho):
        yield x * sigma + mu


def main():
    pass


if __name__ == '__main__':
    main()
