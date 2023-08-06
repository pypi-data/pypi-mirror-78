"""
@ Qufilab, 2020.
@ Anton Normelius

Python interface for statistics indicators.

"""
import numpy as np 

from qufilab.indicators._stat import *

def std(data, periods, normalize = True):
    """
    .. Standard Deviation

    Parameters
    ----------
    data : `ndarray`
        An array containing values.
    periods : `int`
        Number of periods to be used.
    normalize : `bool`, optional
        Specify whether to normalize the standard deviation with 
        n - 1 instead of n.
        Defaults to True.

    Returns
    -------
    `ndarray`
        An array containing standard deviation values for the specified periods.

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ...
    >>> # Load a sample dataframe.
    >>> df = ql.load_sample('MSFT')
    >>> print(df['close'].dtype)
    float64
    >>> sma = ql.std(df['close'], periods = 10)
    >>> print(sma)
    [nan nan nan ... 3.31897842 2.9632574  3.02394683]
    """
    return std_calc(data, periods, normalize)

def var(data, periods, normalize = True):
    """
    .. Variance

    Parameters
    ----------
    data : `ndarray`
        An array containing values.
    periods : `int`
        Number of periods to be used.
    normalize : `bool`, optional
        Specify whether to normalize the standard deviation with 
        n - 1 instead of n.
        Defaults to `True`.

    Returns
    -------
    `ndarray`
        An array containing variance values.

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ...
    >>> # Load a sample dataframe.
    >>> df = ql.load_sample('MSFT')
    >>> print(df['close'].dtype)
    float64
    >>> var = ql.var(df['close'], periods = 10)
    >>> print(var)
    [nan nan nan ... 11.01561778  8.78089444 9.14425444]
    """
    return var_calc(data, periods, normalize)

def cov(data, market, periods, normalize = True):
    """
    .. Covariance

    Parameters
    ----------
    data : `ndarray`
        An array containing values.
    market : `ndarray`
        An array containing market values to be used as the comparison
        when calculating beta.
    periods : `int`
        Number of periods to be used.
    normalize : `bool`, optional
        Specify whether to normalize covariance with 
        n - 1 instead of n.
        Defaults to `True`.

    Returns
    -------
    `ndarray`
        An array containing covariance values.

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ...
    >>> # Load sample dataframe.
    >>> df = ql.load_sample('MSFT')
    >>> df_market = ql.load_sample('DJI')
    >>> cov = ql.cov(df['close'], df_market['close'], periods = 10)
    >>> print(cov)
    [nan nan nan ... -360.37842558  -99.1077715 60.84627274]
    """
    return cov_calc(data, market, periods, normalize)

def beta(data, market, periods, normalize = False):
    """
    .. Beta

    Parameters
    ----------
    data : `ndarray`
        An array containing values.
    market : `ndarray`
        An array containing market values to be used as the comparison
        when calculating beta.
    periods : `int`
        Number of periods to be used.
    normalize : `bool`, optional
        Specify whether to normalize the standard deviation calculation
        within the beta calculation with n - 1 instead of n.
        Defaults to False.

    Returns
    -------
    `ndarray`
        An array containing beta values.

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ...
    >>> # Load sample dataframe.
    >>> df = ql.load_sample('MSFT')
    >>> df_market = ql.load_sample('DJI')
    >>> beta = ql.beta(df['close'], df_market['close'], periods = 10)
    >>> print(beta)
    [nan nan nan ... 0.67027616 0.45641977 0.3169785]
    """
    return beta_calc(data, market, periods, normalize)

def pct_change(data, periods):
    """
    .. Percentage Change

    Parameters
    ----------
    data : `ndarray`
        An array containing values.
    periods : `int`
        Number of periods to be used.

    Returns
    -------
    `ndarray`
        An array containing percentage change for the specified periods.

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ...
    >>> # Load sample dataframe.
    >>> df = ql.load_sample('MSFT')
    >>> pct_change = ql.pct_change(df['close'], periods = 10)
    >>> print(pct_change)
    [nan nan nan ... -1.52155537 -0.81811879 0.25414157]
    """
    return pct_change_calc(data, periods)
