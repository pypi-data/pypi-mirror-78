#!/usr/bin/python3

"""Compute the Irreproducible Discovery Rate (IDR) from NarrowPeaks files

Implementation of the IDR methods for two or more replicates.

LI, Qunhua, BROWN, James B., HUANG, Haiyan, et al. Measuring reproducibility
of high-throughput experiments. The annals of applied statistics, 2011,
vol. 5, no 3, p. 1752-1779.

Given a list of peak calls in NarrowPeaks format and the corresponding peak
call for the merged replicate. This tool computes and appends a IDR column to
NarrowPeaks files.
"""

from scipy.optimize import minimize
import numpy as np
import midr.log as log
import midr.archimedean as archimedean
import c_archimedean as c_arch
from midr.auxiliary import compute_empirical_marginal_cdf, compute_rank
from midr.idr import sim_m_samples
import midr.archimediean_plots as archimediean_plots

COPULA_DENSITY = {
    'clayton': c_arch.pdf_clayton,
    'frank': c_arch.pdf_frank,
    'gumbel': c_arch.pdf_gumbel
}
DMLE_COPULA = {
    'clayton': archimedean.dmle_copula_clayton,
    'frank': archimedean.dmle_copula_frank,
    'gumbel': archimedean.dmle_copula_gumbel
}


def copula_density(copula):
    """
    return a copula density function
    :param copula:
    :return:
    """
    return COPULA_DENSITY[copula]


def copula_number():
    """
    return the number of archimedean copula
    :return:
    """
    return len(COPULA_DENSITY)


def copula_names():
    """
    return the name of the copula density functions
    :return:
    """
    return COPULA_DENSITY.keys()


def dmle_copula(copula):
    """
    return a dmle copula density function
    :param copula:
    :return:
    """
    return DMLE_COPULA[copula]


def number_of_missing(u_values, missing=None):
    """
    return number of missing value per row
    :param u_values:
    :param missing:
    :return:
    >>> number_of_missing(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    [0.25148149, 0.0, 0.3378213, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574, 0.6299574],
    ...    [0.39522060, 0.0, 0.0, 0.6299574],
    ...    [0.66878367, 0.38075101, 0.5185625, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525, 0.6809525],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266, 0.3329266]
    ...    ]),
    ...    missing=0.0
    ... )
    array([0, 1, 0, 0, 2, 0, 0, 1, 0, 0])
    """
    return np.sum(u_values == missing, axis=1)


def remove_missing(u_values, missing=None, nb_missing=0):
    """

    :param u_values:
    :param missing:
    :return:
    >>> remove_missing(np.array([
    ...    [0.25148149, 0.0, 0.3378213, 0.3378213],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    ]),
    ...    missing=0.0,
    ...    nb_missing=1,
    ... )
    array([[0.25148149, 0.3378213 , 0.3378213 ],
           [0.82713755, 0.7686878 , 0.7686878 ]])
    """
    return np.reshape(
        u_values[~(u_values == missing)],
        (u_values.shape[0], u_values.shape[1] - nb_missing)
    )


def list_of_u_values(u_values, missing=None):
    """
    return number of missing value per row
    :param u_values:
    :param missing:
    :return:
    >>> list_of_u_values(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    [0.25148149, 0.0, 0.3378213, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574, 0.6299574],
    ...    [0.39522060, 0.0, 0.0, 0.6299574],
    ...    [0.66878367, 0.38075101, 0.5185625, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525, 0.6809525],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266, 0.3329266]
    ...    ]),
    ...    missing=0.0
    ... )
    array([0, 1, 0, 0, 2, 0, 0, 1, 0, 0])
    """
    nb_missing_row = number_of_missing(u_values=u_values, missing=missing)
    list_u_values = [remove_missing(
                u_values=u_values[nb_missing_row == nb_missing, :],
                missing=missing,
                nb_missing=nb_missing
            ) for nb_missing in range(u_values.shape[1])]
    return (nb_missing_row, list_u_values)


def censored_copula_density(u_values, theta, copula, missing=None):
    """
    compute pdf of copula for censored data
    :param u_values:
    :param theta:
    :param copula:
    :param missing:
    :return:
    >>> censored_copula_density(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    [0.25148149, 0.0, 0.3378213, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574, 0.6299574],
    ...    [0.39522060, 0.0, 0.0, 0.6299574],
    ...    [0.66878367, 0.38075101, 0.5185625, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525, 0.6809525],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266, 0.3329266]
    ...    ]),
    ...    theta=6,
    ...    copula="frank",
    ...    missing=0.0
    ... )
    array([0.01399523, 3.20545262, 0.05619478, 0.04574052, 1.02461261,
           3.41716738, 0.03672658, 4.78125643, 1.02599504, 1.07616887])
    >>> censored_copula_density(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    [0.25148149, 0.3378213, 0.3378213, 0.0],
    ...    [0.79410993, 0.76175687, 0.0709562, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574, 0.6299574],
    ...    [0.0, 0.39522060, 0.0, 0.6299574],
    ...    [0.66878367, 0.38075101, 0.5185625, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525, 0.6809525],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266, 0.3329266]
    ...    ]),
    ...    theta=6,
    ...    copula="frank",
    ...    missing=0.0
    ... )
    array([0.01399523, 3.20545262, 0.05619478, 0.04574052, 1.02461261,
           3.41716738, 0.03672658, 4.78125643, 1.02599504, 1.07616887])
    >>> censored_copula_density(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    [0.25148149, 0.0, 0.3378213, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574, 0.6299574],
    ...    [0.39522060, 0.0, 0.0, 0.6299574],
    ...    [0.66878367, 0.38075101, 0.5185625, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525, 0.6809525],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266, 0.3329266]
    ...    ]),
    ...    theta=2,
    ...    copula="gumbel",
    ...    missing=0.0
    ... )
    array([6.06628394e-03, 2.58088497e+00, 6.63892197e-02, 5.72009627e-02,
           1.11589049e+00, 2.90817712e+00, 7.62035940e-02, 6.16647093e+00,
           1.08801162e+00, 1.22184286e+00])
    >>> censored_copula_density(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    [0.25148149, 0.0, 0.3378213, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574, 0.6299574],
    ...    [0.39522060, 0.0, 0.0, 0.6299574],
    ...    [0.66878367, 0.38075101, 0.5185625, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525, 0.6809525],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266, 0.3329266]
    ...    ]),
    ...    theta=2,
    ...    copula="clayton",
    ...    missing=0.0
    ... )
    array([3.50439735e-02, 3.68342742e+00, 7.46301436e-03, 6.54688263e-06,
           1.10049896e+00, 2.61709390e+00, 5.40124152e-02, 3.30222057e+00,
           6.27832609e-01, 1.25018803e+00])
    >>> COPULA_DENSITY["frank"](np.array([
    ...    [0.42873569, 0.18285458, 0.9514195, 0.9514195],
    ...    [0.25148149, 0.0, 0.3378213, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574, 0.6299574],
    ...    [0.39522060, 0.0, 0.0, 0.6299574],
    ...    [0.66878367, 0.38075101, 0.5185625, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525, 0.6809525],
    ...    [0.0, 0.82713755, 0.7686878, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266, 0.3329266]
    ...    ]),
    ...    6,
    ... )
    array([0.01399523,        nan, 0.05619478, 0.04574052,        nan,
           3.41716738, 0.03672658,        nan, 1.02599504, 1.07616887])
    """
    if missing is None:
        return copula_density(copula)(u_values, theta, False)
    (nb_missing_row, list_u_values) = list_of_u_values(
        u_values=u_values,
        missing=missing
    )
    cdensity = np.zeros(u_values.shape[0])
    for nb_missing in range(u_values.shape[1]):
        cdensity[nb_missing_row == nb_missing] = copula_density(copula)(
            list_u_values[nb_missing],
            theta,
            False
        )
    return cdensity


def delta(params_list, threshold):
    """
    Return true if the difference between two iteration of samic if less than
    the threhsold
    :param params_list: list of model parameters
    :param threshold: flood withe the minimal difference to reach
    :return: bool
    >>> delta(
    ...    params_list={
    ...        'pi': 0.8,
    ...        'pi_old': 0.8,
    ...        'alpha': np.array([0.3333, 0.3333, 0.3333]),
    ...        'alpha_old': np.array([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2},
    ...        'clayton': {'theta': 8, 'pi': 0.2, 'theta_old': 6, 'pi_old': 2.3}
    ...    },
    ...    threshold=0.1
    ... )
    True
    >>> delta(
    ...    params_list={
    ...        'pi': 0.8,
    ...        'pi_old': 0.8,
    ...        'alpha': np.array([0.3333, 0.3333, 0.3333]),
    ...        'alpha_old': np.array([0.3333, 0.3333, 0.3333]),
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2, 'theta_old': 6, 'pi_old': 0.2}
    ...    },
    ...    threshold=0.1
    ... )
    False
    """
    max_delta = [
        max(abs(params_list['alpha'] - params_list['alpha_old'])),
        abs(params_list['pi'] - params_list['pi_old']),
    ]

    for copula in copula_names():
        max_delta.append(
            abs(params_list[copula]['theta'] - params_list[copula]['theta_old'])
        )
    return max(max_delta) >= threshold


def expectation_k(u_values, params_list, dcopula=None):
    """
    compute proba for each copula mix to describe the data
    :param u_values:
    :param params_list:
    :param dcopula:
    :return:
    >>> expectation_k(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6},
    ...        'gumbel': {'theta': 6},
    ...        'clayton': {'theta': 6},
    ...        'missing': None
    ...    }
    ... )
    array([0.00724737, 0.12708761, 0.00081767, 0.00660034, 0.00861115,
           0.18035533, 0.00356172, 0.00996085, 0.08777781, 0.05167504])
    """
    if dcopula is None:
        k_state = np.zeros(u_values.shape[0])
        for copula in copula_names():
            k_state += partial_loglikelihood_copula(
                u_values=u_values,
                copula=copula,
                params_list=params_list
            )
    else:
        k_state = np.sum(dcopula, axis=1)
    k_state *= (1 - params_list['pi'])
    return k_state / (params_list['pi'] + k_state)


def expectation_l(u_values, params_list, dcopula=None):
    """
    compute proba for each copula mix to describe the data
    :param u_values:
    :param params_list:
    :param dcopula:
    :return:
    >>> np.sum(expectation_l(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': None
    ...    }
    ... ), axis=1)
    array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1.])
    >>> expectation_l(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': None
    ...    }
    ... )
    array([[9.99241613e-01, 5.13503781e-07, 7.57873317e-04],
           [9.84106292e-01, 1.58920980e-02, 1.61032426e-06],
           [9.99999854e-01, 1.41403781e-07, 5.09198107e-09],
           [9.99993441e-01, 6.55870887e-06, 1.00492585e-12],
           [9.99993118e-01, 6.88235836e-06, 1.72340850e-13],
           [5.77654946e-01, 1.12341237e-01, 3.10003817e-01],
           [9.99788543e-01, 8.08002235e-07, 2.10648992e-04],
           [9.94643749e-01, 2.06163638e-05, 5.33563491e-03],
           [8.68352025e-01, 8.87728833e-02, 4.28750915e-02],
           [9.43093479e-01, 5.21635253e-03, 5.16901688e-02]])
    """
    l_state = np.zeros((u_values.shape[0], copula_number()))
    if dcopula is None:
        dcopula = partial_loglikelihood_theta(
            u_values=u_values,
            params_list=params_list
        )
    for copula in copula_names():
        l_state[:, params_list['order'][copula]] = (
                dcopula[:, params_list['order'][copula]] /
                np.sum(dcopula, axis=1)
        )
    return l_state


def partial_loglikelihood_copula(u_values, copula, params_list):
    """
    pdf of the samic mixture for a given copula
    :param u_values:
    :param copula:
    :param params_list:
    :return:
    """
    return params_list['alpha'][params_list['order'][copula]] * \
        censored_copula_density(
            u_values=u_values,
            theta=params_list[copula]['theta'],
            copula=copula,
            missing=params_list['missing']
        )


def partial_loglikelihood_theta(u_values, params_list):
    """
    pdf of the samic mixture for a given copula
    :param u_values:
    :param params_list:
    :return:

    >>> partial_loglikelihood_theta(
    ...    u_values = np.array([
    ...       [0.42873569, 0.18285458, 0.9514195],
    ...       [0.25148149, 0.05617784, 0.3378213],
    ...       [0.79410993, 0.76175687, 0.0709562],
    ...       [0.02694249, 0.45788802, 0.6299574],
    ...       [0.39522060, 0.02189511, 0.6332237],
    ...       [0.66878367, 0.38075101, 0.5185625],
    ...       [0.90365653, 0.19654621, 0.6809525],
    ...       [0.28607729, 0.82713755, 0.7686878],
    ...       [0.22437343, 0.16907646, 0.5740400],
    ...       [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': None
    ...    }
    ... )
    array([[2.91789605e-02, 1.49948785e-08, 2.21307392e-05],
           [5.73105482e-01, 9.25494385e-03, 9.37790632e-07],
           [3.27335992e-03, 4.62865538e-10, 1.66678892e-11],
           [2.65765927e-02, 1.74309277e-07, 2.67076801e-14],
           [3.47435253e-02, 2.39119037e-07, 5.98776988e-15],
           [5.08430787e-01, 9.88786536e-02, 2.72854038e-01],
           [1.42948001e-02, 1.15526733e-08, 3.01182210e-06],
           [4.00287013e-02, 8.29690299e-07, 2.14728677e-04],
           [3.34225756e-01, 3.41683824e-02, 1.65024776e-02],
           [2.05559880e-01, 1.13697404e-03, 1.12665660e-02]])
    """
    dcopula = np.zeros((u_values.shape[0], copula_number()))
    for copula in copula_names():
        dcopula[:, params_list['order'][copula]] = \
            partial_loglikelihood_copula(
                u_values=u_values,
                copula=copula,
                params_list=params_list
            )
    return dcopula


def loglikelihood_theta(theta, u_values, copula, params_list, dcopula=None):
    """
    pdf of the samic mixture for a given copula
    :param u_values:
    :param copula:
    :param theta:
    :param dcopula:
    :param params_list:
    :return:
    >>> loglikelihood_theta(
    ...    theta=2,
    ...    u_values = np.array([
    ...       [0.42873569, 0.18285458, 0.9514195],
    ...       [0.25148149, 0.05617784, 0.3378213],
    ...       [0.79410993, 0.76175687, 0.0709562],
    ...       [0.02694249, 0.45788802, 0.6299574],
    ...       [0.39522060, 0.02189511, 0.6332237],
    ...       [0.66878367, 0.38075101, 0.5185625],
    ...       [0.90365653, 0.19654621, 0.6809525],
    ...       [0.28607729, 0.82713755, 0.7686878],
    ...       [0.22437343, 0.16907646, 0.5740400],
    ...       [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    copula = "frank",
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': None
    ...    }
    ... )
    1.4747355660553327
    >>> loglikelihood_theta(
    ...    theta=2,
    ...    u_values = np.array([
    ...       [0.42873569, 0.18285458, 0.9514195],
    ...       [0.25148149, 0.05617784, 0.3378213],
    ...       [0.79410993, 0.76175687, 0.0709562],
    ...       [0.02694249, 0.45788802, 0.6299574],
    ...       [0.39522060, 0.02189511, 0.6332237],
    ...       [0.0, 0.38075101, 0.5185625],
    ...       [0.66878367, 0.38075101, 0.5185625],
    ...       [0.90365653, 0.19654621, 0.6809525],
    ...       [0.28607729, 0.82713755, 0.7686878],
    ...       [0.22437343, 0.16907646, 0.5740400],
    ...       [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    copula = "frank",
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': 0.0
    ...    }
    ... )
    1.4072509026421056
    """
    if dcopula is None:
        dcopula = partial_loglikelihood_theta(
            u_values=u_values,
            params_list=params_list
        )
    dcopula[:, params_list['order'][copula]] = (
        params_list['alpha'][params_list['order'][copula]] *
        censored_copula_density(
            u_values=u_values,
            theta=theta,
            copula=copula,
            missing=params_list['missing']
        )
    )
    return -np.sum(
        np.log(
            params_list['pi'] +
            (1 - params_list['pi']) *
            np.sum(dcopula, axis=1)
        ),
        axis=0
    )


def local_idr(u_values, params_list, missing=None):
    """
    Compute local idr for the samic method
    :param u_values:
    :param params_list:
    :return:
    >>> local_idr(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]),
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': None
    ...    }
    ... )
    array([0.79535495, 0.71654265, 0.79947661, 0.7957702 , 0.79447936,
           0.6802532 , 0.79771887, 0.79361233, 0.74281835, 0.76658261])
    """
    return 1 - expectation_k(u_values=u_values, params_list=params_list)


def minimize_alpha(l_state):
    """
    compute maximization of alpha
    >>> minimize_alpha(np.array([
    ...    [0.42873569, 0.18285458, 0.9514195],
    ...    [0.25148149, 0.05617784, 0.3378213],
    ...    [0.79410993, 0.76175687, 0.0709562],
    ...    [0.02694249, 0.45788802, 0.6299574],
    ...    [0.39522060, 0.02189511, 0.6332237],
    ...    [0.66878367, 0.38075101, 0.5185625],
    ...    [0.90365653, 0.19654621, 0.6809525],
    ...    [0.28607729, 0.82713755, 0.7686878],
    ...    [0.22437343, 0.16907646, 0.5740400],
    ...    [0.66752741, 0.69487362, 0.3329266]
    ...    ]))
    array([0.46469085, 0.37489573, 0.16041342])
    """
    alpha = np.zeros(l_state.shape[1])
    alpha[:-1] = np.sum(l_state[:, :-1], axis=0) / float(l_state.shape[0])
    alpha[-1] = 1.0 - np.sum(alpha[:-1])
    return alpha


def build_bounds(copula, eps=1e-4):
    """
    return set of bound for a given copula
    :param copula:
    :param eps:
    :return:
    >>> build_bounds("frank")
    (0.0001, 744.9999)
    >>> build_bounds("clayton")
    (0.0001, 999.9999)
    >>> build_bounds("gumbel")
    (1.0001, 99.9999)
    """
    thetas = {
        'clayton': {
            'theta_min': 0.0,
            'theta_max': 1000.0
        },
        'frank': {
            'theta_min': 0.0,
            'theta_max': 745.0
        },
        'gumbel': {
            'theta_min': 1.0,
            'theta_max': 100
        }
    }
    return (
        thetas[copula]['theta_min'] + eps, thetas[copula]['theta_max'] - eps
    )


def minimize_pi(k_state):
    """
    find theta that minimize the likelihood of the copula density
    :param k_state:
    :return:
    >>> minimize_pi(
    ...     k_state = np.array([0.99275263, 0.87291238, 0.99918233, 0.99339966,
    ...                         0.99138885, 0.81964467, 0.99643828, 0.99003915,
    ...                         0.91222219, 0.94832496]))
    0.95163051
    """
    return float(np.sum(k_state)) / float(len(k_state))


def minimize_theta(u_values, copula, params_list, dcopula=None):
    """
    find theta that minimize the likelihood of the copula density
    :param u_values:
    :param copula:
    :param params_list:
    :param dcopula:
    :return:
    >>> # data generated with theta = 5
    >>> minimize_theta(np.array([
    ...    [0.2104386, 0.6909995, 0.2195247],
    ...    [0.9185531, 0.9172150, 0.9201070],
    ...    [0.2869368, 0.3535080, 0.2931358],
    ...    [0.3124657, 0.2484218, 0.0519745],
    ...    [0.6768665, 0.6989673, 0.5448870],
    ...    [0.5302475, 0.9583231, 0.8025312],
    ...    [0.7562460, 0.9274616, 0.6933584],
    ...    [0.3130325, 0.3607322, 0.5237398],
    ...    [0.4842922, 0.3572355, 0.3118641],
    ...    [0.5733899, 0.5767076, 0.1369106],
    ...    ]),
    ...    copula="frank",
    ...    params_list={
    ...        'pi': 0.01,
    ...        'alpha': [0.005, 0.005, 0.99],
    ...        'order': {'frank': 2, 'gumbel': 0, 'clayton': 1},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': None
    ...    }
    ... )
    5.443893056499774
    >>> # data generated with theta = 5 and 10% missing
    >>> minimize_theta(np.array([
    ...    [0.2104386, 0.6909995, 0.2195247],
    ...    [0.9185531, 0.0000000, 0.9201070],
    ...    [0.2869368, 0.3535080, 0.2931358],
    ...    [0.3124657, 0.2484218, 0.0519745],
    ...    [0.0000000, 0.6989673, 0.5448870],
    ...    [0.5302475, 0.9583231, 0.0000000],
    ...    [0.7562460, 0.9274616, 0.6933584],
    ...    [0.3130325, 0.3607322, 0.5237398],
    ...    [0.4842922, 0.3572355, 0.3118641],
    ...    [0.5733899, 0.5767076, 0.1369106],
    ...    ]),
    ...    copula="frank",
    ...    params_list={
    ...        'pi': 0.01,
    ...        'alpha': [0.005, 0.005, 0.99],
    ...        'order': {'frank': 2, 'gumbel': 0, 'clayton': 1},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': 0.0
    ...    }
    ... )
    4.979948165192934
    >>> # data generated with theta = 5
    >>> minimize_theta(np.array([
    ...    [0.24078826, 0.37870827, 0.16061743],
    ...    [0.25736139, 0.18174993, 0.38443831],
    ...    [0.16239852, 0.21764999, 0.23479306],
    ...    [0.22269799, 0.24225874, 0.21488540],
    ...    [0.32328339, 0.53500332, 0.31741874],
    ...    [0.07236942, 0.16006716, 0.08322168],
    ...    [0.01503262, 0.02696656, 0.07374267],
    ...    [0.14510121, 0.13951564, 0.20262086],
    ...    [0.03519165, 0.14688405, 0.00565128],
    ...    [0.58870457, 0.68505697, 0.58995495]
    ...    ]),
    ...    copula="gumbel",
    ...    params_list={
    ...        'pi': 0.01,
    ...        'alpha': [0.005, 0.005, 0.99],
    ...        'order': {'frank': 0, 'gumbel': 2, 'clayton': 1},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': None
    ...    }
    ... )
    4.5616062095128775
    >>> # data generated with theta = 5 and 10% missing
    >>> minimize_theta(np.array([
    ...    [0.24078826, 0.37870827, 0.16061743],
    ...    [0.25736139, 0.18174993, 0.38443831],
    ...    [0.16239852, 0.21764999, 0.00000000],
    ...    [0.22269799, 0.24225874, 0.21488540],
    ...    [0.32328339, 0.53500332, 0.31741874],
    ...    [0.07236942, 0.16006716, 0.00000000],
    ...    [0.01503262, 0.02696656, 0.07374267],
    ...    [0.00000000, 0.13951564, 0.20262086],
    ...    [0.03519165, 0.14688405, 0.00565128],
    ...    [0.58870457, 0.68505697, 0.58995495]
    ...    ]),
    ...    copula="gumbel",
    ...    params_list={
    ...        'pi': 0.01,
    ...        'alpha': [0.005, 0.005, 0.99],
    ...        'order': {'frank': 0, 'gumbel': 2, 'clayton': 1},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': 0.0
    ...    }
    ... )
    4.106380760237294
    >>> # data generated with theta = 5
    >>> minimize_theta(np.array([
    ...    [0.10112599, 0.13290793, 0.180375718],
    ...    [0.91367700, 0.89759850, 0.805749718],
    ...    [0.58878457, 0.91666470, 0.661574429],
    ...    [0.90617569, 0.92697520, 0.907013741],
    ...    [0.70750326, 0.51343695, 0.519591735],
    ...    [0.32777265, 0.24957232, 0.427083826],
    ...    [0.01446402, 0.01232720, 0.009718799],
    ...    [0.31459652, 0.24885640, 0.315366745],
    ...    [0.09053508, 0.06687791, 0.075200268],
    ...    [0.46313275, 0.59155993, 0.573731314],
    ...    ]),
    ...    copula="clayton",
    ...    params_list={
    ...        'pi': 0.01,
    ...        'alpha': [0.005, 0.005, 0.99],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': None
    ...    }
    ... )
    5.340785328498203
    >>> # data generated with theta = 5 and 10% missing data
    >>> minimize_theta(np.array([
    ...    [0.00000000, 0.13290793, 0.180375718],
    ...    [0.91367700, 0.89759850, 0.805749718],
    ...    [0.58878457, 0.91666470, 0.00000000],
    ...    [0.90617569, 0.92697520, 0.907013741],
    ...    [0.00000000, 0.51343695, 0.519591735],
    ...    [0.32777265, 0.24957232, 0.427083826],
    ...    [0.01446402, 0.01232720, 0.009718799],
    ...    [0.31459652, 0.24885640, 0.315366745],
    ...    [0.09053508, 0.06687791, 0.075200268],
    ...    [0.46313275, 0.59155993, 0.573731314],
    ...    ]),
    ...    copula="clayton",
    ...    params_list={
    ...        'pi': 0.01,
    ...        'alpha': [0.005, 0.005, 0.99],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2},
    ...        'missing': 0.0
    ...    }
    ... )
    5.677473176653246
    """
    log.logging.debug("%s", copula + " minimize_theta")
    old_theta = params_list[copula]['theta']
    log.logging.debug("%s", str([build_bounds(copula)]) + " minimize() bounds")
    log.logging.debug("%s", str(old_theta) + " old_theta")
    if log.logging.root.level == log.logging.DEBUG:
        archimediean_plots.pdf_copula_plot(
            lower=build_bounds(copula)[0],
            upper=build_bounds(copula)[1],
            copula=copula,
            pdf_function=loglikelihood_theta,
            u_values=u_values,
            params_list=params_list,
        )
    if dcopula is None:
        dcopula = partial_loglikelihood_theta(
            u_values=u_values,
            params_list=params_list
        )
    res = minimize(
        fun=loglikelihood_theta,
        args=(u_values, copula, params_list, dcopula),
        x0=old_theta,
        bounds=[build_bounds(copula)],
    )
    log.logging.debug("%s", res)
    if np.isnan(res.x[0]):
        log.logging.debug("%s", str(old_theta) + " new_theta = old_theta")
        return old_theta
    else:
        log.logging.debug("%s", str(res.x[0]) + " new_theta")
        return res.x[0]


def samic(x_score, threshold=1e-4, missing=None):
    """
    implementation of the samic method for m samples
    :param x_score np.array of score (measures x samples)
    :param threshold float min delta between every parameters between two
    iterations
    :param missing: float value equal to the value considered to be missing
    :return (theta: dict, lidr: list) with theta the model parameters and
    lidr the local idr values for each measures
    >>> THETA_TEST_0 = {'mu': 0.0, 'sigma': 1.0, 'rho': 0.0}
    >>> THETA_TEST_1 = {'pi': 0.1, 'mu': 4.0, 'sigma': 3.0, 'rho': 0.75}
    >>> DATA = sim_m_samples(n_value=10000,
    ...                      m_sample=20,
    ...                      theta_0=THETA_TEST_0,
    ...                      theta_1=THETA_TEST_1)
    >>> lidr = samic(DATA["X"], threshold=0.0001)
    >>> (np.sum((lidr < 0.5).all() == DATA["K"]) / len(lidr)) # <= 0.11
    True
    """
    log.logging.info("%s", "computing idr")
    u_values = compute_empirical_marginal_cdf(
        compute_rank(
            x_score=x_score,
            missing=missing
        ),
        gaussian=True,
        missing=missing
    )
    params_list = {'order': {}}
    i = 0
    for copula in copula_names():
        if missing is None:
            params_list[copula] = {
                'theta': dmle_copula(copula)(u_values),
                'theta_old': np.nan,
            }
        else:
            params_list[copula] = {
                'theta': 4.0,
                'theta_old': np.nan,
            }
        params_list['order'][copula] = i
        i += 1
    params_list['missing'] = missing
    params_list['k_state'] = np.zeros(u_values.shape[0])
    params_list['l_state'] = np.zeros((u_values.shape[0], copula_number()))
    params_list['pi'] = 0.5
    params_list['pi_old'] = 0.0
    params_list['alpha'] = np.repeat(1.0 / copula_number(), copula_number())
    params_list['alpha_old'] = params_list['alpha'][:]
    dcopula = partial_loglikelihood_theta(
        u_values=u_values,
        params_list=params_list
    )
    while delta(params_list, threshold):
        params_list['k_state'] = expectation_k(
            u_values=u_values,
            params_list=params_list,
            dcopula=dcopula
        )
        params_list['l_state'] = expectation_l(
            u_values=u_values,
            params_list=params_list,
            dcopula=dcopula
        )
        params_list['alpha_old'] = params_list['alpha'][:]
        params_list['pi_old'] = params_list['pi']
        params_list['pi'] = minimize_pi(
            k_state=params_list['k_state']
        )
        params_list['alpha'] = minimize_alpha(
            l_state=params_list['l_state']
        )
        log.logging.info(
            "%s",
            log_samic(params_list)
        )
        for copula in COPULA_DENSITY:
            params_list[copula]['theta_old'] = params_list[copula]['theta']
            params_list[copula]['theta'] = minimize_theta(
                u_values=u_values,
                copula=copula,
                params_list=params_list,
                dcopula=dcopula
            )
            dcopula[:, params_list['order'][copula]] = \
                partial_loglikelihood_copula(
                u_values=u_values,
                copula=copula,
                params_list=params_list
            )
            log.logging.info(
                "%s %s",
                copula,
                log_samic(params_list)
            )
    return local_idr(
        u_values=u_values,
        params_list=params_list
    )


def log_samic(params_list):
    """
    return str of pseudo_likelihood parameter estimate
    :param params_list:
    :return:
    >>> log_samic(
    ...    params_list={
    ...        'pi': 0.8,
    ...        'alpha': [0.3333, 0.3333, 0.3333],
    ...        'order': {'frank': 0, 'gumbel': 1, 'clayton': 2},
    ...        'frank': {'theta': 6, 'pi': 0.2},
    ...        'gumbel': {'theta': 6, 'pi': 0.2},
    ...        'clayton': {'theta': 6, 'pi': 0.2}
    ...    })
    '{"pi": 0.8, \n"alpha": [0.3333, 0.3333, 0.3333], \n"clayton": \
    {"theta": 6}, \n"frank": {"theta": 6}, \n"gumbel": {"theta": 6} }'
    """
    log_str = str('{' +
                  '"pi": ' + str(params_list['pi'])
                  )
    for copula in copula_names():
        log_str += str(
            ', \n"' + copula + '": {' +
            '"alpha": ' +
            str(params_list['alpha'][params_list["order"][copula]]) +
            ', ' '"theta": ' +
            str(params_list[copula]['theta']) +
            '}')
    return log_str + ' }'


if __name__ == "__main__":
    import doctest

    doctest.testmod()
