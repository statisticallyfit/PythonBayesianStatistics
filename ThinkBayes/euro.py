"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com
Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

"""This file contains a partial solution to a problem from
MacKay, "Information Theory, Inference, and Learning Algorithms."
    Exercise 3.15 (page 50): A statistical statement appeared in
    "The Guardian" on Friday January 4, 2002:
        When spun on edge 250 times, a Belgian one-euro coin came
        up heads 140 times and tails 110.  'It looks very suspicious
        to me,' said Barry Blight, a statistics lecturer at the London
        School of Economics.  'If the coin were unbiased, the chance of
        getting a result as extreme as that would be less than 7%.'
MacKay asks, "But do these data give evidence that the coin is biased
rather than fair?"
"""

import thinkbayes
import thinkplot


class Euro(thinkbayes.Suite):
    """Represents hypotheses about the probability of heads."""

    def likelihood(self, data, hypo):
        """Computes the likelihood of the data under the hypothesis.
        hypo: integer value of x, the probability of heads (0-100)
        data: string 'H' or 'T'
        """
        x = hypo / 100.0
        if data == 'H':
            return x
        else:
            return 1-x


class Euro2(thinkbayes.Suite):
    """Represents hypotheses about the probability of heads."""

    def likelihood(self, data, hypo):
        """Computes the likelihood of the data under the hypothesis.
        hypo: integer value of x, the probability of heads (0-100)
        data: tuple of (number of heads, number of tails)
        """
        x = hypo / 100.0
        heads, tails = data
        like = x**heads * (1-x)**tails
        return like


def uniformPrior():
    """Makes a Suite with a uniform prior."""
    suite = Euro(range(0, 101))
    return suite


def trianglePrior():
    """Makes a Suite with a triangular prior."""
    suite = Euro()
    for x in range(0, 51):
        suite.set(x, x)
    for x in range(51, 101):
        suite.set(x, 100-x)
    suite.normalize()
    return suite


def runUpdate(suite, heads=140, tails=110):
    """Updates the Suite with the given number of heads and tails.
    suite: Suite object
    heads: int
    tails: int
    """
    dataset = 'H' * heads + 'T' * tails

    for data in dataset:
        suite.update(data)


def summarize(suite):
    """Prints summary statistics for the suite."""
    print(suite.prob(50))

    print('MLE', suite.maximumLikelihood())

    print('Mean', suite.mean())
    print('Median', thinkbayes.percentile(suite, 50))

    print('5th %ile', thinkbayes.percentile(suite, 5))
    print('95th %ile', thinkbayes.percentile(suite, 95))

    print('CI', thinkbayes.credibleInterval(suite, 90))


def plotSuites(suites, root):
    """Plots two suites.
    suite1, suite2: Suite objects
    root: string filename to write
    """
    thinkplot.clf()
    thinkplot.prePlot(len(suites))
    thinkplot.pmfs(suites)

    thinkplot.save(root=root,
                   xlabel='x',
                   ylabel='Probability',
                   formats=['pdf', 'eps'])


def main():
    # make the priors
    suite1 = uniformPrior()
    suite1.name = 'uniform'

    suite2 = trianglePrior()
    suite2.name = 'triangle'

    # plot the priors
    plotSuites([suite1, suite2], 'euro2')

    # update
    runUpdate(suite1)
    summarize(suite1)

    runUpdate(suite2)
    summarize(suite2)

    # plot the posteriors
    plotSuites([suite1], 'euro1')
    plotSuites([suite1, suite2], 'euro3')

    # NOTE: the priors (triangle and uniform) end up making the same posterior.
    # note: this convergence happens when you have enough data.


if __name__ == '__main__':
    main()