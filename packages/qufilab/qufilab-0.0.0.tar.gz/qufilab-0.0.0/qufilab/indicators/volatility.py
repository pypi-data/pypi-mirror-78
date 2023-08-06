"""
@ Qufilab, 2020.
@ Anton Normelius

Python interface for volatility indicators.

"""
import numpy as np 

from qufilab.indicators._volatility import *

def bbands(price, period, deviation = 2):
    """
    .. Bollinger Bands

    Parameters
    ----------
    price : `ndarray`
        Array of type float64 or float32 containing the prices.
    period : `int`
        Number of periods to be used.
    deviation : `int`, optional
        Number of standard deviations from the mean.
        Defaults to 20.

    Returns
    -------
    upper : `ndarray`
        Upper bollinger band.
    middle : `ndarray`
        middle bollinger band.
    lower : `ndarray`
        lower bollinger band.
    """
    return bbands_calc(price, period, deviation)

def kc(close, high, low, period = 20, period_atr = 20, deviation = 2):
    """
    .. Keltner channels

    Parameters
    ----------
    close : `ndarray`
        Array of type float64 or float32 containing the closing prices.
    high : `ndarray`
        Array of type float64 or float32 containing the high prices.
    low : `ndarray`
        Array of type float64 or float32 containing the low prices.
    period : `int`, optional
        Number of periods to be used.
        Defaults to 20.
    period_atr : `int`, optional
        Number of periods to be used for the average true range calculations.
        Defaults to 20.
    deviation : `int`, optional
        Number of deviations from the mean.
        Defaults to 2.

    Returns
    -------
    upper : `ndarray`
        Upper keltner band.
    middle : `ndarray`
        middle keltner band.
    lower : `ndarray`
        lower keltner band.
    """
    return kc_calc(close, high, low, period, period_atr, deviation)

def atr(close, high, low, period):
    """
    .. Average true range

    Parameters
    ----------
    close : `ndarray`
        Array of type float64 or float32 containing the closing prices.
    high : `ndarray`
        Array of type float64 or float32 containing the high prices.
    low : `ndarray`
        Array of type float64 or float32 containing the low prices.
    period : `int`
        Number of periods to be used.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated
        average true range values.
    """
    return atr_calc(close, high, low, period)

def cv(high, low, period = 10, smoothing_period = 10):
    """
    .. Chaikin volatility

    Parameters
    ----------
    high : `ndarray`
        Array of type float64 or float32 containing the high prices.
    low : `ndarray`
        Array of type float64 or float32 containing the low prices.
    period : `int`, optional
        Number of periods to be used.
        Defaults to 10.
    smooting_period : `int`, optional
        Number of periods to be used for smoothing chaikin volatility values.
        Defaults to 10.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated
        chaikin volatility values.
    """
    return cv_calc(high, low, period, smoothing_period)
