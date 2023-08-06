#!/usr/bin/python3

"""Compute the Irreproducible Discovery Rate (IDR) from NarrowPeaks files

This section of the project provides facilitites to handle NarrowPeaks files
and compute IDR on the choosen value in the NarrowPeaks columns
"""

from scipy.stats import rankdata
import numpy as np


def compute_rank(x_score, missing=None):
    """
    transform x a n*m matrix of score into an n*m matrix of rank ordered by
    row.

    >>> compute_rank(np.array([[0,0],[10,30],[20,20],[30,10]]))
    array([[1, 1],
           [2, 4],
           [3, 3],
           [4, 2]])
    >>> compute_rank(np.array([[0,0],[10,30],[20,20],[30,10]]), missing=0)
    array([[0, 0],
           [1, 3],
           [2, 2],
           [3, 1]])
    """
    rank = np.empty_like(x_score)
    for i in range(x_score.shape[1]):
        # we want the rank to start at 1
        if missing is None:
            rank[:, i] = rankdata(x_score[:, i], method="ordinal")
        else:
            non_missing = np.where(~(x_score[:, i] == missing))[0]
            rank[non_missing, i] = rankdata(
                x_score[non_missing, i],
                method="ordinal")
            rank[np.where((x_score[:, i] == missing))[0], i] = missing
    return rank


def compute_empirical_marginal_cdf(rank, gaussian=False, missing=None):
    """
    normalize ranks to compute empirical marginal cdf and scale by n / (n+1)

    >>> r = compute_rank(np.array(
    ...    [[0.1,0.1],
    ...    [10.0,30.0],
    ...    [20.0,20.0],
    ...    [30.0,10.0]]))
    >>> compute_empirical_marginal_cdf(r, gaussian=True)
    array([[0.99  , 0.99  ],
           [0.7425, 0.2475],
           [0.495 , 0.495 ],
           [0.2475, 0.7425]])
    >>> r = compute_rank(np.array(
    ...    [[0.0,0.0],
    ...    [10.0,30.0],
    ...    [20.0,20.0],
    ...    [30.0,10.0]]))
    >>> compute_empirical_marginal_cdf(r)
    array([[0.2, 0.2],
           [0.4, 0.8],
           [0.6, 0.6],
           [0.8, 0.4]])
    >>> r = compute_rank(np.array(
    ...    [[0.0,0.0],
    ...    [0.1,0.1],
    ...    [10.0,30.0],
    ...    [20.0,20.0],
    ...    [30.0,10.0]]), missing=0.0)
    >>> compute_empirical_marginal_cdf(r, missing=0.0)
    array([[0. , 0. ],
           [0.2, 0.2],
           [0.4, 0.8],
           [0.6, 0.6],
           [0.8, 0.4]])
    """
    if gaussian:
        n_value = float(rank.shape[0])
        m_sample = float(rank.shape[1])
        # scaling_factor = n_value / (n_value + 1.0)
        # we want a max value of 0.99
        scaling_factor = 0.99
        for i in range(int(n_value)):
            for j in range(int(m_sample)):
                rank[i][j] = (1.0 - (float(rank[i][j] - 1) / n_value)) * \
                                scaling_factor
    else:
        if missing is None:
            rank *= (1.0 / (float(rank.shape[0]) + 1.0))
        else:
            for i in range(rank.shape[1]):
                non_missing = np.where(~(rank[:, i] == missing))[0]
                rank[non_missing, i] *= (
                        1.0 / (float(len(non_missing)) + 1.0)
                )
                rank[np.where((rank[:, i] == missing))[0], i] = missing
    return rank


def benjamini_hochberg(p_vals):
    """
    compute fdr from pvalues
    :param p_vals:
    :return:
    """
    ranked_p_values = rankdata(p_vals)
    fdr = p_vals * len(p_vals) / ranked_p_values
    fdr[fdr > 1] = 1
    return fdr
