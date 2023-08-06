"""
@ Qufilab, 2020.
@ Anton Normelius

Python interface for trend indicators.

"""
import time
import numpy as np

from qufilab.indicators._trend import *


def sma(data, periods):
    """
    .. Simple moving average

    Parameters
    ----------
    data : `ndarray`
        An array containing values.
    periods : `int`
        Number of periods to be used.

    Returns
    -------
    `ndarray`
        An array containing calculated simple moving average values.

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ... 
    >>> # Load a sample dataframe.
    >>> df = ql.load_sample('MSFT')
    >>> print(df['close'].dtype)
    float64
    >>> sma = ql.sma(df['close'], periods = 10)
    >>> print(sma)
    [nan nan nan ... 209.872 209.695 209.749]

    Notes
    -----
    The calculation of sma is a equally weighted mean for the last *n* days.

    .. math::
        sma_K = \\frac{price_K + price_{K-1} + ... + price_{K-(n-1)}}{n} =
        \\frac{1}{n}\sum_{i=0}^{n-1} price_{K-i}

    """
    return sma_calc(data, periods)

def ema(data, periods):
    """
    .. Exponential Moving Average

    Parameters
    ----------
    data : `ndarray`
        An array containing values.
    periods : `int`
        Number of periods to be used.

    Returns
    -------
    `ndarray`
        An array containing calculated exponential moving average values.

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ... 
    >>> # Load a sample dataframe.
    >>> df = ql.load_sample('MSFT')
    >>> print(df['close'].dtype)
    float64
    >>> ema = ql.ema(df['close'], periods = 10)
    >>> print(ema)
    [nan nan nan ... 209.63323895 210.53265005 210.98489549]

    Notes
    -----
    The calculation of ema can be written as a power series:

    .. math:: ema_K = \\alpha[price_K + (1-\\alpha)price_{K-1} + \\
        (1-\\alpha)^2price_{K-2}  + ... +  (1-\\alpha)^{K-(n-1)}price_{K-(n-1)},

    which also can be written as:

    .. math::
        ema_K = ema_{K-1} + \\alpha[price_K - ema_{K-1}],

    where :math:`\\alpha = \\frac{2}{n+1}` is the multiplier and depends on
    the period *n*. Observe that for the first ema value, a simple moving average
    is used.
    """
    return ema_calc(data, periods)


def dema(data, periods):
    """
    .. Double Exponential Moving Average

    Parameters
    ----------
    data : `ndarray`
        An array containing values.
    periods : `int`
        Number of periods to be used.

    Returns
    -------
    `ndarray`
        An array containing calculated double exponential moving average values.

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ... 
    >>> # Load a sample dataframe.
    >>> df = ql.load_sample('MSFT')
    >>> print(df['close'].dtype)
    float64
    >>> dema = ql.ema(df['close'], periods = 10)
    >>> print(dema)
    [nan nan nan ... 210.18599259 211.72078484 212.32702478]

    Notes
    -----
    .. math::
        dema_K = 2 \cdot ema_K - ema(ema_K)

    """
    return dema_calc(data, periods)

def tema(data, periods):
    """
    .. Triple Exponential Moving Average

    Parameters
    ----------
    data : `ndarray`
        An array containing values.
    periods : `int`
        Number of periods to be used.

    Returns
    -------
    `ndarray`
        An array containing calculated triple exponential moving average values.

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ... 
    >>> # Load a sample dataframe.
    >>> df = ql.load_sample('MSFT')
    >>> print(df['close'].dtype)
    float64
    >>> tema = ql.tema(df['close'], periods = 10)
    >>> print(tema)
    [nan nan nan ... 210.00373443 212.09152183 212.75635054]

    Notes
    -----
    The triple exponential moving average is similar to the other exponential
    moving averages, however this one utilize three exponential moving averages.

    .. math::
        tema_K = 3 \cdot ema_K - 3 \cdot ema(ema_K) + ema(ema(ema_K))
    """
    return tema_calc(data, periods)

def t3(data, periods, volume_factor = 0.7):
    """
    .. T3 Moving Average

    Parameters
    ----------
    data : `ndarray`
        An array containing values.
    periods : `int`
        Number of periods to be used.
    volume_factor : `float`, optional
        What volume factor to be used when calculating the constants. 
        See `Notes` below for implementation.

    Returns
    -------
    `ndarray`
        An array containing calculated t3 moving average values.

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ... 
    >>> # Load a sample dataframe.
    >>> df = ql.load_sample('MSFT')
    >>> print(df['close'].dtype)
    float64
    >>> t3 = ql.t3(df['close'], periods = 10)
    >>> print(t3)
    [nan nan nan ... 210.08668472 210.2348457 210.47802463]

    Notes
    -----
    The t3 moving average indicator utilize many different 
    exponential moving averages and is calculated with:

    .. math::
        t3 = c_1e_6 + c_2e_5 + c_3e_4 + c_4e_3

        e_1 = ema(data)

        e_2 = ema(e_1)

        e_3 = ema(e_2)

        e_4 = ema(e_3)

        e_5 = ema(e_4)

        e_6 = ema(e_5)

        c_1 = -a^3

        c_2 = 3a^2 + 3a^3

        c_3 = –6a^2–3a–3a^3

        c_4 = 1 + 3a + a^3 + 3a^2

    where *a* is the volume factor and is typically set to `0.7`.
    """
    if volume_factor < 0:
        raise ValueError("Param 'volume_factor' needs to be bigger than zero")

    return t3_calc(data, periods, volume_factor)


def tma(data, periods):
    """
    .. Triangular Moving Average

    Parameters
    ----------
    data : `ndarray`
        An array containing values.
    periods : `int`
        Number of periods to be used.

    Returns
    -------
    `ndarray`
        An array containing calculated triangular moving average values.

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ... 
    >>> # Load a sample dataframe.
    >>> df = ql.load_sample('MSFT')
    >>> print(df['close'].dtype)
    float64
    >>> tma = ql.tma(df['close'], periods = 10)
    >>> print(tma)
    [nan nan nan ... 208.93833333 209.115 209.684]

    Notes
    -----
    The triangular moving average is calculated by taking an sma of an sma.

    .. math::
        tma = sma(sma(price, n_1), n_2)

    As seen above, two different periods are used in this
    implementation. If the parameter `periods` is even

    .. math::
        n_1 = \\frac{periods}{2}

        n_2 = \\frac{periods}{2} + 1

    otherwise they are rounded up after the following calculation

    .. math::
        n_1 = n_2 = \\frac{periods + 1}{2}
    """
    return tma_calc(data, periods)

def smma(data, periods):
    """
    .. Smoothed Moving Average

    Parameters
    ----------
    data : `ndarray`
        An array containing values.
    periods : `int`
        Number of periods to be used.

    Returns
    -------
    `ndarray`
        An array containing calculated smoothed moving average values.

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ... 
    >>> # Load a sample dataframe.
    >>> df = ql.load_sample('MSFT')
    >>> print(df['close'].dtype)
    float64
    >>> smma = ql.smma(df['close'], periods = 10)
    >>> print(smma)
    [nan nan nan ... 208.85810754 209.43029679 209.78926711]
    """
    return smma_calc(data, periods)

def lwma(data, periods):
    """
    .. Linear Weighted Moving Average

    Parameters
    ----------
    data : `ndarray`
        An array containing values.
    periods : `int`
        Number of periods to be used.

    Returns
    -------
    `ndarray`
        An array containing calculated linear weighted moving average values.

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ... 
    >>> # Load a sample dataframe.
    >>> df = ql.load_sample('MSFT')
    >>> print(df['close'].dtype)
    float64
    >>> lwma = ql.lwma(df['close'], periods = 10)
    >>> print(lwma)
    [nan nan nan ... 209.50327273 210.35927273 210.96381818]

    Notes
    -----
    The linear weighted moving average is calculated similar to the simple
    moving average, except that the values aren't equally weighted, but
    linearly weighted with the highest weight going first and then decreasing
    linearly. This implementation use the number of periods as the highest
    weight, and thereafter decreasing down to one.

    .. math:: lwma_K = \\frac{price_K \cdot w_n + price_{K-1} \cdot w_{n-1} \\
            + ... + price_{K-(n-1)} \cdot w_1}{\sum_{i=1}^n w_i},

    where :math:`w_1 = 1, w_2 = 2,... w_n = n`
    """
    return lwma_calc(data, periods)

def wc(high, low, close):
    """
    .. Weighted Close

    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    close : `ndarray`
        An array containing closing prices.

    Returns
    -------
    `ndarray`
        An array containing calculated weighted close values.

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ... 
    >>> # Load a sample dataframe.
    >>> df = ql.load_sample('MSFT')
    >>> wc = ql.wc(df['high'], df['low'], df['close'])
    >>> print(wc)
    [153.1975 154.09 154.3075 ... 210.1875 213.2675 213.785]

    Notes
    -----
    The weighted close is defined as:

    .. math:: wc_K = \\frac{2 \cdot close_K + high_K + low_K}{4}

    """
    return wc_calc(close, high, low)



