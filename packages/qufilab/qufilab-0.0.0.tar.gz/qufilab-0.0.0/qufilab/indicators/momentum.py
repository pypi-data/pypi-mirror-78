"""
@ Qufilab, 2020.
@ Anton Normelius

Python interface for momentum indicators.

"""
import time
import numpy as np 

from qufilab.indicators._momentum import *

def rsi(price, period, rsi_type = "smoothed"):
    """
    .. Relative strength index
    
    Parameters
    ----------
    price : `ndarray`
        Array of type float64 or float32 containing the data to calculate rsi from.
    period : `int`
        Number of periods to be used.
    rsi_type : {'smoothed', 'standard'}, optional
        Specify what kind of averaging should be used for calculating the average gain/
        average loss. Standard is the Wilder's smoothing.
    
    Returns
    -------
    `ndarray`
        Returns a numpy ndarray with type float64 or float32.
    """
    return rsi_calc(price, period, rsi_type.lower())

def macd(price):
    """
    .. MACD

    Parameters
    ----------
    price : `ndarray`
        Array of type float64 or float32 containing the prices to calculate macd from.

    Returns
    -------
    macd : `ndarray`
        Array of type float64 or float32 containing the macd values.
    signal : `ndarray`
        Array of type float64 or float32 containing the signal values.
    """
    return macd_calc(price)

def willr(close, high, low, period):
    """
    .. William's R

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
        Array of type float64 or float32 containing the william's r values.
    """
    return willr_calc(close, high, low, period)

def roc(price, period):
    """
    .. Price Rate of Change

    Parameters
    ----------
    price : `ndarray`
        Array of type float64 or float32 containing price values.
    period : `int`
        Number of periods to be used.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated rate
        of change values.
    """
    return roc_calc(price, period)

def vpt(price, volume):
    """
    .. Volume Price Trend

    Parameters
    ----------
    price : `ndarray`
        Array of type float64 or float32 containing price values.
    volume : `ndarray`
        Array of type float64 or float32 containing volume values.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated volume
        price trend values.
    """
    return vpt_calc(price, volume)

def mi(price, period):
    """
    .. Momentum Indicator

    Parameters
    ----------
    price : `ndarray`
        Array of type float64 or float32 containing price values.
    period : `int`
        Number of periods to be used.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated momentum
        indicator values.
    """
    return mi_calc(price, period)

def apo(price, period_slow = 26, period_fast = 12, ma = "sma"):
    """
    .. Absolute Price Oscillator

    Parameters
    ----------
    price : `ndarray`
        Array of type float64 or float32 containing price values.
    period_slow : `int`, optional
        Number of periods for the slow moving average.
        Default to 26.
    period_fast : `int`, optional
        Number of fast periods for the fast moving average.
        Default to 12.
    ma : {'sma', 'ema'}, optional
        Type of moving average to be used. 
        Default to 'sma'

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated absolute
        price oscillator values.
    """
    if ma.lower() not in ["sma", "ema"]:
        raise ValueError("param 'ma' needs to be 'ema' or 'sma'")

    return apo_calc(price, period_slow, period_fast, ma.lower())

def bop(high, low, open_, close):
    """
    .. Balance of Power

    Parameters
    ----------
    high : `ndarray`
        Array of type float64 or float32 containing high prices.
    low : `ndarray`
        Array of type float64 or float32 containing low prices.
    open_ : `ndarray`
        Array of type float64 or float32 containing open prices.
    close : `ndarray`
        Array of type float64 or float32 containing closing prices.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated 
        balance of power values.
    """
    return bop_calc(high, low, open_, close)

def cmo(close, period):
    """
    .. Chande Momentum Indicator

    Parameters
    ----------
    close : `ndarray`
        Array of type float64 or float32 containing closing prices.
    period : `int`
        Number of periods to be used.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated chande
        momentum values.
    """
    return cmo_calc(close, period)

def mfi(high, low, close, volume, period):
    """
    .. Money Flow Index

    Parameters
    ----------
    high : `ndarray`
        Array of type float64 or float32 containing high prices.
    low : `ndarray`
        Array of type float64 or float32 containing low prices.
    close : `ndarray`
        Array of type float64 or float32 containing closing prices.
    volume : `ndarray`
        Array of type float64 or float32 containing volume values.
    period : `int`
        Number of periods to be used.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated money
        flow index values.
    """
    return mfi_calc(high, low, close, volume, period)

def ppo(price, period_fast = 12, period_slow = 26, ma = "ema"):
    """
    .. Percentage Price Oscillator
    
    Parameters
    ----------
    price : `ndarray`
        Array of type float64 or float32 containing price values.
    period_fast : `int`, optional
        Number of fast periods for the fast moving average.
        Default to 12.
    period_slow : `int`, optional
        Number of periods for the slow moving average.
        Default to 26.
    ma : {'ema', 'sma'}, optional
        Type of moving average to be used. 
        Default to 'ema'

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated 
        percentage price values.
    """
    if ma.lower() not in ["sma", "ema"]:
        raise ValueError("Param 'ma' needs to be 'sma' or 'ema'")

    return ppo_calc(price, period_fast, period_slow, ma.lower())

#def stochastic(close, high, low, mode = "fast", period_k = 10, method = "ema"):
#    """
#    Returns %K and %D stochastics.
#
#    :param close: Closing prices.
#    :type close: List.
#    :param high: High prices.
#    :type high: List.
#    :param low: Low prices.
#    :type low: List.
#    :param mode: Specify whether to calculate 'fast' or 'slow' stochastic.
#    :type mode: Str.
#    :param period_k: Specify the number of periods used in the Stochastic (%K)
#        calculation.
#    :type period_k: Int.
#    :param method: Specify the method that is used to calculate Stochastic (%D) 
#        calculation.
#    :type method: Str.
#    :return tuple: A tuple containing (%K, %D).
#    """
#    if method and method.lower() not in ['sma', 'ema']:
#        raise ValueError("Param 'method' needs to be 'sma' or 'ema'.")
#    
#    if mode and mode.lower() not in ['fast', 'slow']:
#        raise ValueError("Param 'mode' needs to be 'fast' or 'slow'.")
#    
#    if not isinstance(period_k, int):
#        raise ValueError("Param 'period_k' needs to be an int.")
#
#    return stochastic_calc(close, high, low, mode, period_k, method)


def cci(close, high, low, period = 20):
    """
    .. Commodity Channel Index

    Parameters
    ----------
    close : `ndarray`
        Array of type float64 or float32 containing closing prices.
    high : `ndarray`
        Array of type float64 or float32 containing high prices.
    low : `ndarray`
        Array of type float64 or float32 containing low prices.
    period : `int`, optional
        Number of periods to be used.
        Defaults to 20.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated commodity
        channel index values.
    """
    return cci_calc(close, high, low, period)

def aroon(high, low, period = 20):
    """
    .. Aroon Indicator
    
    Parameters
    ----------
    high : `ndarray`
        Array of type float64 or float32 containing high prices.
    low : `ndarray`
        Array of type float64 or float32 containing low prices.
    period : `int`, optional
        Number of periods to be used.
        Defaults to 20.

    Returns
    -------
    `ndarray`
        Array of type float64 or float32 containing the calculated
        aroon indicator values.
    """
    return aroon_calc(high, low, period)

#def tsi(close, period = 25, period_double = 13):
#    return tsi_calc(close, period, period_double)
