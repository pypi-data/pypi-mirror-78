"""
@ Qufilab, 2020.
@ Anton Normelius

Python interface for volume indicators.

"""
import time
import numpy as np 

from qufilab.indicators._volume import *

def acdi(close, high, low, volume):
    """
    .. Accumulation distribution

    Parameters
    ----------
    close : `ndarray`
        Array of type float64 or float32 containing closing prices.
    high : `ndarray`
        Array of type float64 or float32 containing high prices.
    low : `ndarray`
        Array of type float64 or float32 containing low prices.
    volume : `ndarray`
        Array of type float64 or float32 containing volume values.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated
        accumulation distribution values.
    """
    return acdi_calc(close, high, low, volume)

def obv(price, volume):
    """
    .. On balance volume

    Parameters
    ----------
    price : `ndarray`
        Array of type float64 or float32 containing prices.
    volume : `ndarray`
        Array of type float64 or float32 containing volume values.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated
        on balance volume values.
    """

    return obv_calc(price, volume)

def cmf(close, high, low, volume, period = 21):
    """
    .. Chaikin money flow

    Parameters
    ----------
    close : `ndarray`
        Array of type float64 or float32 containing closing prices.
    high : `ndarray`
        Array of type float64 or float32 containing high prices.
    low : `ndarray`
        Array of type float64 or float32 containing low prices.
    volume : `ndarray`
        Array of type float64 or float32 containing volume values.
    period : `int`, optional
        Number of periods to use.
        Defaults to 21.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated
        chaikin money flow values.
    """
    return cmf_calc(close, high, low, volume, period)

def ci(close, high, low, volume):
    """
    .. Chaikin indicator

    Parameters
    ----------
    close : `ndarray`
        Array of type float64 or float32 containing closing prices.
    high : `ndarray`
        Array of type float64 or float32 containing high prices.
    low : `ndarray`
        Array of type float64 or float32 containing low prices.
    volume : `ndarray`
        Array of type float64 or float32 containing volume values.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated
        chaikin indicator values.
    """
    return ci_calc(close, high, low, volume)

def pvi(price, volume):
    """
    .. Positive volume index

    Parameters
    ----------
    price : `ndarray`
        Array of type float64 or float32 containing prices.
    volume : `ndarray`
        Array of type float64 or float32 containing volume values.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated
        positive volume index values.
    """
    return pvi_calc(price, volume)

def nvi(price, volume):
    """
    .. Negative volume index

    Parameters
    ----------
    price : `ndarray`
        Array of type float64 or float32 containing prices.
    volume : `ndarray`
        Array of type float64 or float32 containing volume values.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated
        negative volume index values.
    """
    return nvi_calc(price, volume)
