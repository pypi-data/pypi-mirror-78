# Standard Library
from functools import reduce # For plotting inequalities
import random # For shuffling

# Third Party
import numpy as np
import sympy as sp
from scipy.stats import norm as normal # For z-table
import matplotlib.pyplot as plt # For plotting inequalities
import matplotlib.ticker as ticker
import inflect

say = inflect.engine().number_to_words
choose = sp.binomial

def pick(n, r):
    result = reduce(lambda a, b: a*b, range(n - r + 1, n + 1))
    return sp.sympify(result)

def variety(items: list):
    """Yields shuffled items, then reshuffles when items are exhausted."""

    while True:
        index = 0
        random.shuffle(items)
        while index < len(items):
            yield items[index]
            index += 1

def get_pmf(size, digits=1):
    """Generates a probability mass function with probabilities that have 'precision' decimal places."""

    # Create the list of possible values as integers to avoid floating point calculations
    entries = list(range(1, 10**digits))

    # Randomly select values to cut the interval [0, 1)
    cuts = np.random.choice(entries, size = size - 1, replace = False)

    # Ensure there are cuts at 0 and 1
    cuts = np.append(cuts, 0)
    cuts = np.append(cuts, 10**digits)

    # Probabilities are the difference between each cut from least to greatest
    cuts = np.sort(cuts)
    pmf = [b - a for a, b in zip(cuts[:-1], cuts[1:])]

    # Convert the integers to probabilities
    pmf = [entry/10**digits for entry in pmf]

    return sp.sympify(pmf)

def negative_y_coef(K, B, R=None):
    """Returns the same system, but the y-coefficients are always negative."""

    diag_signs = tuple(map(sp.sign, K.col(1)))
    y_signs = sp.diag(*diag_signs)
    K = -1 * y_signs * K
    B = -1 * y_signs * B

    # Multiplying an inequality by -1, requires the relation to be reversed
    if R:
        reversedsign = {sp.Le:sp.Ge, sp.Ge:sp.Le, sp.Lt:sp.Gt, sp.Gt:sp.Lt }
        new_R = []
        for sign, relation in zip(diag_signs, R):
            if sign > 0:
                new_R.append(reversedsign[relation])
            else:
                new_R.append(relation)
        return K, B, sp.Matrix(new_R)

    return K, B

# A Sympy inequality does have an attribute that returns itself multiplied by -1
# But I need to keep K, R, B separated to convert them into a LaTeX system of inequalities
"""
# Construct the inequalities
ineqs = []
x, y = sp.symbols('x y')
X = sp.Matrix([x, y])
for expr, r, b in zip(K*X, R, B):
    ineqs.append(r(expr, b))

for ineq in ineqs:
display(ineq)

for index, y_coef in enumerate(K.col(1)):
    if y_coef < 0:
        ineqs[index] = ineqs[index].reversedsign

for ineq in ineqs:
    display(ineq)
"""

# Override MultipleLocator to remove tick labels at zero
def tick_values(self, vmin, vmax):
    if vmax < vmin:
        vmin, vmax = vmax, vmin
    step = self._edge.step
    vmin = self._edge.ge(vmin) * step
    n = (vmax - vmin + 0.001 * step) // step
    locs = vmin - step + np.arange(n + 3) * step
    locs = [i for i in locs if i != 0]
    return self.raise_if_exceeds(locs)
ticker.MultipleLocator.tick_values = tick_values

def set_cartesian_plane(axes, xmin=-11.5, xmax=11.5, ymin=-11.5, ymax=11.5, multiples_of=5):
    """Styles a Matplotlib.Axes object to that of a textbook cartesian plane"""

    ax = axes
    # Center the axes on the origin
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    # Set the min/max of the axes
    ax.axis([xmin, xmax, ymin, ymax])
    # Set the tick marks
    ax.minorticks_on()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    #########################
    # There were multiple issues with matplotlib's gridlines
    # - The x-minor gridlines ignore their z-order and were graphed on top of everything including the text labels
    # - The x-minor gridlines did not appear outside of the vertical range of the plotted lines
    #
    # SOLUTION: Plot gridlines manually
    #########################
    # Set the grid
    xlength = abs(xmax - xmin)
    ylength = abs(ymax - ymin)
    minorticks = ax.xaxis.get_minorticklocs()
    for tick in minorticks:
        ax.arrow(xmin, tick,
                 xlength, 0,
                 head_width=0.0,
                 head_length=0.0,
                 length_includes_head=False,
                 color=(0.5,0.5,0.5),
                 zorder=1,
                )
    for tick in minorticks:
        ax.arrow(tick, ymin,
                 0, ylength,
                 head_width=0.0,
                 head_length=0.0,
                 length_includes_head=False,
                 color=(0.5,0.5,0.5),
                 zorder=1,
                )
    majorticks = ax.xaxis.get_majorticklocs()
    for tick in majorticks:
        ax.arrow(xmin, tick,
                 xlength, 0,
                 head_width=0.0,
                 head_length=0.0,
                 length_includes_head=False,
                 color=(0.3,0.3,0.3),
                 zorder=1,
                )
    for tick in majorticks:
        ax.arrow(tick, ymin,
                 0, ylength,
                 head_width=0.0,
                 head_length=0.0,
                 length_includes_head=False,
                 color=(0.3,0.3,0.3),
                 zorder=1,
                )
    #########################

    # Draw and label the x- and y-axis with arrowheads
    ax.set_xlabel('$x$', usetex=True, position=(1,0), fontsize='x-large')
    ax.arrow(xmin, 0,
             xlength, 0,
             head_width=0.5,
             head_length=0.5,
             length_includes_head=True,
             color='black',
             zorder=5,
            )
    ax.set_ylabel('$y$', usetex=True, position=(0,1), fontsize='x-large')
    ax.arrow(0, ymin,
             0, ylength,
             head_width=0.5,
             head_length=0.5,
             length_includes_head=True,
             color='black',
             zorder=5,
            )
    ax.set_aspect('equal')

def plot_inequalities(K, R, B, name='', xmin=-11.5, xmax=11.5, ymin=-11.5, ymax=11.5):
    # Construct the inequalities
    ineqs = []
    x, y = sp.symbols('x y')
    X = sp.Matrix([x, y])
    for expr, r, b in zip(K*X, R, B):
        ineqs.append(r(expr, b))
    # Construct the boundary equations for plotting
    eqs = []
    #boundaries = []
    for expr, b in zip(K*X, B):
        eq = sp.Eq(expr, b)
        eqs.append(eq)


    ################## Plot ###########

    # Plot the solution set
    p = sp.plot_implicit(reduce(sp.And, ineqs), (x, xmin, xmax), (y, ymin, ymax), line_color=(0.7, 0.7, 0.7), show=False)

    # Plot the boundary equations
    for eq in eqs:
        if y in eq.free_symbols:
            function = sp.solve(eq, y)[0]
            p_next = sp.plot(function, (x, xmin, xmax), line_color='black', show=False)
        elif x in eq.free_symbols:
            inverse_func = sp.solve(eq, x)[0]
            p_next = sp.plot_parametric(inverse_func, y, (y, ymin, ymax), line_color='black', show=False)
        p.append(p_next[0])
    plot = p.backend(p)
    plot.process_series()
    fig = plot.fig
    ax = plot.ax[0]
    set_cartesian_plane(ax, xmin, xmax, ymin, ymax)

    # Save the plot as a PDF file
    fig.savefig(f'{name}_key_plot.pdf', dpi=80, bbox_inches="tight")

    # Create a blank cartesian plane for the student
    blank_fig, blank_ax = plt.subplots()
    set_cartesian_plane(blank_ax, xmin, xmax, ymin, ymax)
    blank_fig.savefig(f'{name}_blank_plot.pdf', dpi=80, bbox_inches="tight")

def partition_set(E, size):
    # Partitions the set E into 'size' non-empty subsets of random length
    if size > len(E):
        raise ValueError('Size cannot be greater than the length of the set.')

    # Randomly select the sizes of the partitions
    cuts = sorted(np.random.choice(range(1,len(E)), size = size - 1, replace = False))
    sizes = [cuts[i] - cuts[i - 1] for i in range(len(cuts))]
    sizes[0] = cuts[0]

    partitions = []
    for size in sizes:
        # Select a random subset from E of length size
        random_subset = set([E.pop() for i in range(size)])
        partitions.append(random_subset)
    partitions.append(E)

    return partitions

def get_set_tex(E, sort=True):
    if sort:
        E = sorted(E)

    elements = ', '.join(map(str, E))
    return r'\{{ {0} \}}'.format(elements)

def rand_nonzero(mag_of_entries: int, size: tuple):
    """Returns a size-tuple with random integer entries where 0 < abs(entries) <= magnitude"""

    coeff = [c for c in range(-mag_of_entries, mag_of_entries+1) if c != 0]
    entries = np.random.choice(coeff, size=size, replace=False)
    return entries

############################### NOT USED YET
class Ztable(object):
    def __init__(self):
        pass

    def get_prob(self, z):
        """Calculates the probability for a given z-score.

        Parameters
        ----------
        z: float
            A z-score. This will be rounded to two decimal places to match the
            PDF z-table.

        Returns
        -------
        float
            The probability, rounded to 4 decimal places, for the given z-score.
        """
        z = round(z, 2)
        if z > 3.49:
            return 1.0
        elif z < -3.49:
            return 0.0
        else:
            return round(normal.cdf(z, 0, 1), 4)

    def get_zscore(self, p):
        """Calculates the z-score for a given probability.

        Parameters
        ----------
        float
            A probability. This will be rounded to 4 decimal places to match the
            PDF z-table.

        Returns
        -------
        z: float
            The z-score, rounded to two decimal places, for the given probability.
        """

        p = round(p, 4)
        return round(normal.ppf(p, 0, 1), 2)

def get_finite_dist(count, precision):
    # Returns a finite probability distribution
    # Returns a finite list, P, of 'count' probabilities rounded to 'precision' decimal places such that sum(P) = 1
    cuts = np.sort(np.random.choice(range(1, 10**precision), size = count - 1, replace = False)/10**precision)
    P = np.zeros(count)
    for i in range(0, count - 1):
        P[i] = cuts[i] - np.sum(P)
    P[-1] = 1 - np.sum(P)
    return P