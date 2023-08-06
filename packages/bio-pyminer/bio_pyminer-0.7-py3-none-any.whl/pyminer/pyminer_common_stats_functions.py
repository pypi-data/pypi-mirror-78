#!/usr/bin/env python3
from __future__ import division, print_function, absolute_import

import warnings
import math
from collections import namedtuple

# Scipy imports.
from scipy._lib.six import callable, string_types, xrange
from scipy._lib._version import NumpyVersion
from numpy import array, asarray, ma, zeros, var, average
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
import scipy.special as special
import scipy.linalg as linalg
import numpy as np
from scipy.stats import rankdata
from copy import deepcopy
import h5py

from scipy.stats import mstats_basic, rankdata

#from . import distributions
#from . import mstats_basic
#from ._distn_infrastructure import _lazywhere
#from ._stats_mstats_common import _find_repeats, linregress, theilslopes
#from ._stats import _kendall_condis

__all__ = []

# __all__ = ['find_repeats', 'gmean', 'hmean', 'mode', 'tmean', 'tvar',
#            'tmin', 'tmax', 'tstd', 'tsem', 'moment', 'variation',
#            'skew', 'kurtosis', 'describe', 'skewtest', 'kurtosistest',
#            'normaltest', 'jarque_bera', 'itemfreq',
#            'scoreatpercentile', 'percentileofscore', 'histogram',
#            'histogram2', 'cumfreq', 'relfreq', 'obrientransform',
#            'signaltonoise', 'sem', 'zmap', 'zscore', 'iqr', 'threshold',
#            'sigmaclip', 'trimboth', 'trim1', 'trim_mean', 'f_oneway',
#            'pearsonr', 'fisher_exact', 'spearmanr', 'pointbiserialr',
#            'kendalltau', 'linregress', 'theilslopes', 'ttest_1samp',
#            'ttest_ind', 'ttest_ind_from_stats', 'ttest_rel', 'kstest',
#            'chisquare', 'power_divergence', 'ks_2samp', 'mannwhitneyu',
#            'tiecorrect', 'ranksums', 'kruskal', 'friedmanchisquare',
#            'chisqprob', 'betai',
#            'f_value_wilks_lambda', 'f_value', 'f_value_multivariate',
#            'ss', 'square_of_sums', 'fastsort', 'rankdata',
#            'combine_pvalues', ]


def _chk_asarray(a, axis):
    if axis is None:
        a = np.ravel(a)
        outaxis = 0
    else:
        a = np.asarray(a)
        outaxis = axis
    if a.ndim == 0:
        a = np.atleast_1d(a)
    return a, outaxis


def _chk2_asarray(a, b, axis):
    if axis is None:
        a = np.ravel(a)
        b = np.ravel(b)
        outaxis = 0
    else:
        a = np.asarray(a)
        b = np.asarray(b)
        outaxis = axis
    if a.ndim == 0:
        a = np.atleast_1d(a)
    if b.ndim == 0:
        b = np.atleast_1d(b)
    return a, b, outaxis


def _contains_nan(a, nan_policy='propagate'):
    policies = ['propagate', 'raise', 'omit']
    if nan_policy not in policies:
        raise ValueError("nan_policy must be one of {%s}" %
                         ', '.join("'%s'" % s for s in policies))
    try:
        # Calling np.sum to avoid creating a huge array into memory
        # e.g. np.isnan(a).any()
        with np.errstate(invalid='ignore'):
            contains_nan = np.isnan(np.sum(a))
    except TypeError:
        # If the check cannot be properly performed we fallback to omiting
        # nan values and raising a warning. This can happen when attempting to
        # sum things that are not numbers (e.g. as in the function `mode`).
        contains_nan = False
        nan_policy = 'omit'
        warnings.warn("The input array could not be properly checked for nan "
                      "values. nan values will be ignored.", RuntimeWarning)
    if contains_nan and nan_policy == 'raise':
        raise ValueError("The input contains nan values")
    return (contains_nan, nan_policy)

def make_dense(b):
    if b is not None:
        if "todense" in dir(b):
            b=b.todense()
    return(b)


def no_p_spear(a, b=None, axis=0, nan_policy='propagate', rm_nans_by_col = False, prop = False):
    a=make_dense(a)
    b=make_dense(b)

    a, axisout = _chk_asarray(a, axis)
    
    contains_nan, nan_policy = _contains_nan(a, nan_policy)

    if contains_nan and rm_nans_by_col:
        ### FINISH THIS
        rm_idxs = np.isna(a)
    
    if contains_nan and nan_policy == 'omit':
        a = ma.masked_invalid(a)
        b = ma.masked_invalid(b)
        return no_p_spear(a, b, axis)
    
    if a.size <= 1:
        return SpearmanrResult(np.nan, np.nan)
    ar = np.apply_along_axis(rankdata, axisout, a)
    
    br = None
    if b is not None:
        b, axisout = _chk_asarray(b, axis)
        
        contains_nan, nan_policy = _contains_nan(b, nan_policy)
        
        if contains_nan and nan_policy == 'omit':
            b = ma.masked_invalid(b)
            return no_p_spear(a, b, axis)
        
        br = np.apply_along_axis(rankdata, axisout, b)
    n = a.shape[axisout]
    if not prop:
        rs = np.corrcoef(ar, br, rowvar=axisout)
    else:
        rs = pp_equivalent_to_cov(ar, br)
    
    olderr = np.seterr(divide='ignore')  # rs can have elements equal to 1
    try:
        # clip the small negative values possibly caused by rounding
        # errors before taking the square root
        t = rs * np.sqrt(((n-2)/((rs+1.0)*(1.0-rs))).clip(0))
    finally:
        np.seterr(**olderr)
    
    if rs.shape == (2, 2):
        return rs[1, 0]
    else:
        return rs


def fast_single_spear(a,b,shuffle = False):
    ## first remove nans
    a_keep = np.logical_not(np.isnan(a))
    b_keep = np.logical_not(np.isnan(b))
    keep = a_keep * b_keep
    a=a[keep]
    b=b[keep]
    ar = rankdata(a,method='dense')
    br = rankdata(b,method='dense')
    if shuffle:
        s_ar = deepcopy(ar)
        np.random.shuffle(s_ar)
        return(np.corrcoef(ar,br)[1,0], np.corrcoef(s_ar,br)[1,0])
    else:
        return(np.corrcoef(ar,br)[1,0])
# def no_p_spear_pairwise(a, b=None, axis=0, nan_policy='propagate', rm_nans_by_col = False, prop = False):
#     ## axis: 1 is row, by row, 0 is column by column
#     if rm_nans_by_col:


#     ar = np.apply_along_axis(rankdata, axisout, a)    
#     br = np.apply_along_axis(rankdata, axisout, b)

#     n = a.shape[axisout]
#     if not prop:
#         rs = np.corrcoef(ar, br, rowvar=axisout)
#     else:
#         rs = pp_equivalent_to_cov(ar, br)
    
#     olderr = np.seterr(divide='ignore')  # rs can have elements equal to 1
#     try:
#         # clip the small negative values possibly caused by rounding
#         # errors before taking the square root
#         t = rs * np.sqrt(((n-2)/((rs+1.0)*(1.0-rs))).clip(0))
#     finally:
#         np.seterr(**olderr)
    
#     if rs.shape == (2, 2):
#         return rs[1, 0]
#     else:
#         return rs


########################################################
########################################################
########################################################
####### proportaionality statistic functions ###########
########################################################
########################################################
########################################################

dummy_array = None
def multi_pp(i):
    global dummy_array
    return(var(dummy_array[i,:] - dummy_array[:,:],axis = 1))

def get_pp(in_mat, verbose = False, do_multi = True):
    ## first get the variance of all genes
    if do_multi:
        threads = multiprocessing.cpu_count()
    else:
        threads = 1
    all_var = var(in_mat, axis = 1)
    if verbose:
        print(all_var)
    ## then get the distance matrix
    ## TODO - make multi-threaded version!
    if do_multi and threads > 1:
        global dummy_array
        dummy_array = in_mat
        indices = list(range(0,in_mat.shape[0]))
        ## set up multi-threaded pool
        pool = ThreadPool(threads)
        all_diff_var = pool.map(multi_pp,indices)
        pool.close()
        pool.join()
        all_diff_var = np.array(all_diff_var)
    else:
        all_diff_var = np.zeros((in_mat.shape[0],in_mat.shape[0]))
        for i in range(0,in_mat.shape[0]):
            all_diff_var[i,:] = var(in_mat[i,:] - in_mat[:,:],axis = 1)
    #all_diff_var = var(in_mat[:,:] - in_mat[:,None,:],axis = 2)
    if verbose:
        print("all_diff_var")
        print(all_diff_var)
    ## then get the pairwise added variance of the original vectors
    all_added_var = all_var + all_var[:,None]
    if verbose:
        print(all_added_var)
    ## then just divide the two matrices by each other
    pp_mat = 1 - (all_diff_var/all_added_var)
    return pp_mat


def get_pp_2(in_mat_a, in_mat_b, verbose = False):
    in_mat_a=make_dense(in_mat_a)
    in_mat_b=make_dense(in_mat_b)

    ## first get the variance of all genes
    all_var_a = var(in_mat_a, axis = 1)
    all_var_b = var(in_mat_b, axis = 1)
    ## then get the distance matrix
    all_diff_var = np.zeros((in_mat_a.shape[0],in_mat_b.shape[0]))
    for i in range(0,in_mat_a.shape[0]):
        all_diff_var[i,:] = var(in_mat_a[i,:] - in_mat_b[:,:],axis = 1)
    #all_diff_var = var(in_mat[:,:] - in_mat[:,None,:],axis = 2)
    if verbose:
        print("all_diff_var")
        print(all_diff_var)
    ## then get the pairwise added variance of the original vectors
    all_added_var = all_var_a[:,None] + all_var_b[None,:]
    if verbose:
        print(all_added_var)
    ## then just divide the two matrices by each other
    pp_mat = 1 - (all_diff_var/all_added_var)
    return pp_mat


def pp_equivalent_to_cov(m, y=None, rowvar=True, bias=False, ddof=None, fweights=None,
        aweights=None):
    """
    Estimate a covariance matrix, given data and weights.
    Covariance indicates the level to which two variables vary together.
    If we examine N-dimensional samples, :math:`X = [x_1, x_2, ... x_N]^T`,
    then the covariance matrix element :math:`C_{ij}` is the covariance of
    :math:`x_i` and :math:`x_j`. The element :math:`C_{ii}` is the variance
    of :math:`x_i`.
    See the notes for an outline of the algorithm.
    Parameters
    ----------
    m : array_like
        A 1-D or 2-D array containing multiple variables and observations.
        Each row of `m` represents a variable, and each column a single
        observation of all those variables. Also see `rowvar` below.
    y : array_like, optional
        An additional set of variables and observations. `y` has the same form
        as that of `m`.
    rowvar : bool, optional
        If `rowvar` is True (default), then each row represents a
        variable, with observations in the columns. Otherwise, the relationship
        is transposed: each column represents a variable, while the rows
        contain observations.
    bias : bool, optional
        Default normalization (False) is by ``(N - 1)``, where ``N`` is the
        number of observations given (unbiased estimate). If `bias` is True,
        then normalization is by ``N``. These values can be overridden by using
        the keyword ``ddof`` in numpy versions >= 1.5.
    ddof : int, optional
        If not ``None`` the default value implied by `bias` is overridden.
        Note that ``ddof=1`` will return the unbiased estimate, even if both
        `fweights` and `aweights` are specified, and ``ddof=0`` will return
        the simple average. See the notes for the details. The default value
        is ``None``.
        .. versionadded:: 1.5
    fweights : array_like, int, optional
        1-D array of integer frequency weights; the number of times each
        observation vector should be repeated.
        .. versionadded:: 1.10
    aweights : array_like, optional
        1-D array of observation vector weights. These relative weights are
        typically large for observations considered "important" and smaller for
        observations considered less "important". If ``ddof=0`` the array of
        weights can be used to assign probabilities to observation vectors.
        .. versionadded:: 1.10
    Returns
    -------
    out : ndarray
        The covariance matrix of the variables.
    See Also
    --------
    corrcoef : Normalized covariance matrix
    Notes
    -----
    Assume that the observations are in the columns of the observation
    array `m` and let ``f = fweights`` and ``a = aweights`` for brevity. The
    steps to compute the weighted covariance are as follows::
        >>> m = np.arange(10, dtype=np.float64)
        >>> f = np.arange(10) * 2
        >>> a = np.arange(10) ** 2.
        >>> ddof = 9 # N - 1
        >>> w = f * a
        >>> v1 = np.sum(w)
        >>> v2 = np.sum(w * a)
        >>> m -= np.sum(m * w, axis=None, keepdims=True) / v1
        >>> cov = np.dot(m * w, m.T) * v1 / (v1**2 - ddof * v2)
    Note that when ``a == 1``, the normalization factor
    ``v1 / (v1**2 - ddof * v2)`` goes over to ``1 / (np.sum(f) - ddof)``
    as it should.
    Examples
    --------
    Consider two variables, :math:`x_0` and :math:`x_1`, which
    correlate perfectly, but in opposite directions:
    >>> x = np.array([[0, 2], [1, 1], [2, 0]]).T
    >>> x
    array([[0, 1, 2],
           [2, 1, 0]])
    Note how :math:`x_0` increases while :math:`x_1` decreases. The covariance
    matrix shows this clearly:
    >>> np.cov(x)
    array([[ 1., -1.],
           [-1.,  1.]])
    Note that element :math:`C_{0,1}`, which shows the correlation between
    :math:`x_0` and :math:`x_1`, is negative.
    Further, note how `x` and `y` are combined:
    >>> x = [-2.1, -1,  4.3]
    >>> y = [3,  1.1,  0.12]
    >>> X = np.stack((x, y), axis=0)
    >>> np.cov(X)
    array([[11.71      , -4.286     ], # may vary
           [-4.286     ,  2.144133]])
    >>> np.cov(x, y)
    array([[11.71      , -4.286     ], # may vary
           [-4.286     ,  2.144133]])
    >>> np.cov(x)
    array(11.71)
    """
    # Check inputs
    if ddof is not None and ddof != int(ddof):
        raise ValueError(
            "ddof must be integer")

    # Handles complex arrays too
    m = np.asarray(m)
    if m.ndim > 2:
        raise ValueError("m has more than 2 dimensions")

    if y is None:
        dtype = np.result_type(m, np.float64)
    else:
        y = np.asarray(y)
        if y.ndim > 2:
            raise ValueError("y has more than 2 dimensions")
        dtype = np.result_type(m, y, np.float64)

    X = array(m, ndmin=2, dtype=dtype)
    if not rowvar and X.shape[0] != 1:
        X = X.T
    if X.shape[0] == 0:
        return np.array([]).reshape(0, 0)
    if y is not None:
        y = array(y, copy=False, ndmin=2, dtype=dtype)
        if not rowvar and y.shape[0] != 1:
            y = y.T
        X = np.concatenate((X, y), axis=0)

    if ddof is None:
        if bias == 0:
            ddof = 1
        else:
            ddof = 0

    # Get the product of frequencies and weights
    w = None
    if fweights is not None:
        fweights = np.asarray(fweights, dtype=float)
        if not np.all(fweights == np.around(fweights)):
            raise TypeError(
                "fweights must be integer")
        if fweights.ndim > 1:
            raise RuntimeError(
                "cannot handle multidimensional fweights")
        if fweights.shape[0] != X.shape[1]:
            raise RuntimeError(
                "incompatible numbers of samples and fweights")
        if any(fweights < 0):
            raise ValueError(
                "fweights cannot be negative")
        w = fweights
    if aweights is not None:
        aweights = np.asarray(aweights, dtype=float)
        if aweights.ndim > 1:
            raise RuntimeError(
                "cannot handle multidimensional aweights")
        if aweights.shape[0] != X.shape[1]:
            raise RuntimeError(
                "incompatible numbers of samples and aweights")
        if any(aweights < 0):
            raise ValueError(
                "aweights cannot be negative")
        if w is None:
            w = aweights
        else:
            w *= aweights

    avg, w_sum = average(X, axis=1, weights=w, returned=True)
    w_sum = w_sum[0]

    # Determine the normalization
    if w is None:
        fact = X.shape[1] - ddof
    elif ddof == 0:
        fact = w_sum
    elif aweights is None:
        fact = w_sum - ddof
    else:
        fact = w_sum - ddof*sum(w*aweights)/w_sum

    if fact <= 0:
        warnings.warn("Degrees of freedom <= 0 for slice",
                      RuntimeWarning, stacklevel=3)
        fact = 0.0

    X -= avg[:, None]
    if w is None:
        X_T = X.T
    else:
        X_T = (X*w).T
    c = get_pp(X)
    c *= np.true_divide(1, fact)
    return c.squeeze()


########################################################
########################################################
########################################################


def get_Z_cutoff(vect, z=4.5,positive = False):
    ## this is for a half distribution, so mult by -1 to make it 'normal'
    vect_original = np.array(deepcopy(vect))
    keep = np.logical_not(np.isnan(vect_original))
    vect_original = vect_original[keep]
    vect = deepcopy(vect_original)
    vect = list(vect)
    vect += list(np.array(vect)*-1)
    vect = np.array(vect)
    ## get the mean, & SD
    v_mean = np.mean(vect)
    v_std = np.std(vect)
    cutoff = v_std * z
    if not positive:
        cutoff *= -1
        cutoff = max([-0.9,cutoff])
    else:
        cutoff = min([0.9,cutoff])
    print('cutoff:',cutoff)
    if not positive:
        num_sig = np.sum(np.array(vect_original<cutoff,dtype = bool))
        total_num = vect_original.shape[0]
        print(num_sig, "/", total_num, 'significant')
        FPR = max([1,total_num])/num_sig
        return(cutoff, FPR)
    else:
        return(cutoff)
