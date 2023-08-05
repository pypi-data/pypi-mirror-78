"""Statistical significance utils.

This is an adaptation of Philipp Stinger's implementation of
the Steiger's (1980) test available here:
https://github.com/psinger/CorrelationStats/blob/master/corrstats.py
"""
import numpy as np
from scipy import stats

__all__ = ('steiger_test_pval')


# pylint: disable=C0103
def steiger_test_pval(xy, xz, yz, n, twotailed=True):
    """Calculate statisticical significance between two dependent correlations.

    @param xy: correlation coefficient between x and y
    @param xz: correlation coefficient between x and z
    @param yz: correlation coefficient between y and z
    @param n: number of elements in x, y and z
    @param twotailed: whether to calculate a one or two tailed test
    @return: p-val
    """
    d = xy - xz
    determin = 1 - xy * xy - xz * xz - yz * yz + 2 * xy * xz * yz
    av = (xy + xz)/2
    cube = (1 - yz) * (1 - yz) * (1 - yz)
    t2 = d * np.sqrt((n - 1) * (1 + yz)/(((2 * (n - 1)/(n - 3)) * determin + av * av * cube)))
    p = 1 - stats.t.cdf(abs(t2), n - 3)
    if twotailed:
        p *= 2
    return p
