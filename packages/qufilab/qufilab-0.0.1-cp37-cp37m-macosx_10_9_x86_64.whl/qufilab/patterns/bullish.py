"""
@ QufiLab, 2020.
@ Anton Normelius

Python interface for bullish patterns.

"""
import numpy as np

from qufilab.patterns._bullish import *

def hammer(high, low, open_, close, periods = 10, shadow_margin = 5.0):
    """
    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.
    shadow_margin : `float`, optional
        Specify what margin should be allowed for the shadows. By using i.e.
        5%, upper shadow can be as long as 5% of the candlestick body size. 
        This exist to allow some margin and not exclude the shadows entirely.

    Returns
    -------
    hammer : `ndarray`
        A numpy array of type bool specifying true whether
        a pattern has been found or false otherwise. 

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ... 
    >>> df = ql.load_sample('MSFT')
    >>> hammer = ql.hammer(df['high'], df['low'], df['open'], df['close'])
    >>> print(hammer)
    [False False False ... False False False]
    
    Notes
    -----
    Observe that the lower shadow shall be bigger than 2x the body, but lower
    than 3x the body.

    .. image:: images/hammer.png

    """
    hammer_type = "hammer"
    hammer = hammer_calc(high, low, open_, close, periods, hammer_type, shadow_margin)
    return hammer
    
def inverted_hammer(high, low, open_, close, periods = 10, shadow_margin = 5.0):
    """
    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.
    shadow_margin : `float`, optional
        Specify what margin should be allowed for the shadows. By using i.e.
        5%, lower shadow can be as long as 5% of the candlestick body size. 
        This exist to allow some margin and not exclude the shadows entirely.

    Returns
    -------
    inverted_hammer : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ... 
    >>> df = ql.load_sample('MSFT')
    >>> inverted_hammer = ql.inverted_hammer(df['high'], df['low'], df['open'], df['close'])
    >>> print(inverted_hammer)
    [False False False ... False False False]


    """
    hammer_type = "inverted_hammer"
    hammer = hammer_calc(high, low, open_, close, periods, hammer_type, shadow_margin)
    return hammer

def doji(high, low, open_, close, periods = 10):
    """
    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.

    Returns
    -------
    doji : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ... 
    >>> df = ql.load_sample('MSFT')
    >>> doji = ql.doji(df['high'], df['low'], df['open'], df['close'])
    >>> print(doji)
    [False False False ... False False False]

    """
    doji = doji_calc(high, low, open_, close, periods)
    return doji

def dragonfly_doji(high, low, open_, close, periods = 10):
    """
    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.

    Returns
    -------
    dragonfly_doji : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ... 
    >>> df = ql.load_sample('MSFT')
    >>> dragonfly_doji = ql.dragonfly_doji(df['high'], df['low'], df['open'], df['close'])
    >>> print(dragonfly_doji)
    [False False False ... False False False]

    """
    dragonfly_doji = dragonfly_doji_calc(high, low, open_, close, periods)
    return dragonfly_doji

def marubozu_white(high, low, open_, close, shadow_margin = 5.0, periods = 10):
    """
    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    shadow_margin : `float`, optional
        Specify what margin should be allowed for the shadows. By using for 
        example 5%, both the lower and upper shadow can be as high as 5%
        of the candlestick body size. This exist to allow some margin (not
        restrict to no shadow).
    periods : `int`, optional
        Specifying number of periods for trend identification.

    Returns
    -------
    marubozu_white : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 

    Examples
    --------
    >>> import qufilab as ql
    >>> import numpy as np
    ... 
    >>> df = ql.load_sample('MSFT')
    >>> marubozu_white = ql.marubozu_white(df['high'], df['low'], df['open'], df['close'])
    >>> print(marubozu_white)
    [False False False ... False False False]
    """
    marubozu_white = marubozu_white_calc(high, low, open_, close, shadow_margin, periods)
    return marubozu_white

def marubozu_black(high, low, open_, close, shadow_margin = 5.0, periods = 10):
    """
    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    shadow_margin : `float`, optional
        Specify what margin should be allowed for the shadows. By using for 
        example 5%, both the lower and upper shadow can be as high as 5%
        of the candlestick body size. This exist to allow some margin (not
        restrict to no shadow).
    periods : `int`, optional
        Specifying number of periods for trend identification.

    Returns
    -------
    marubozu_black : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 
    """
    pattern = marubozu_black_calc(high, low, open_, close, shadow_margin, periods)
    return pattern

def spinning_top_white(high, low, open_, close, periods = 10):
    """
    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.

    Returns
    -------
    spinning_top_white : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 
    """
    spinning_top_white = spinning_top_white_calc(high, low, open_, close, periods)
    return spinning_top_white

def engulfing_bull(high, low, open_, close, periods = 10):
    """
    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.

    Returns
    -------
    engulfing : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 

    """
    engulfing_type = "bull"
    engulfing = engulfing_calc(high, low, open_, close, periods, engulfing_type)
    return engulfing

def engulfing_bear(high, low, open_, close, periods = 10):
    """
    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.

    Returns
    -------
    engulfing : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 
    """
    engulfing_type = "bear"
    engulfing = engulfing_calc(high, low, open_, close, periods, engulfing_type)
    return engulfing

def harami_bull(high, low, open_, close, periods = 10):
    """
    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.

    Returns
    -------
    harami_bull : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 
    """
    harami_type = "bull"
    harami = harami_calc(high, low, open_, close, periods, harami_type)
    return harami

def harami_bear(high, low, open_, close, periods = 10):
    """
    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.

    Returns
    -------
    harami_bear : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 
    """
    harami_type = "bear"
    harami = harami_calc(high, low, open_, close, periods, harami_type)
    return harami

def kicking_bull(high, low, open_, close, periods = 10, shadow_margin = 5.0):
    """
    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.
    shadow_margin : `float`, optional
        Specify what margin should be allowed for the shadows. By using for 
        example 5%, both the lower and upper shadow can be as high as 5%
        of the candlestick body size. This exist to allow some margin (not
        restrict to no shadow).

    Returns
    -------
    kicking_bull : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 
    """
    kicking_type = "bull"
    kicking = kicking_calc(high, low, open_, close, periods, kicking_type, shadow_margin)
    return kicking
    
def kicking_bear(high, low, open_, close, periods = 10, shadow_margin = 5.0):
    """
    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.
    shadow_margin : `float`, optional
        Specify what margin should be allowed for the shadows. By using for 
        example 5%, both the lower and upper shadow can be as high as 5%
        of the candlestick body size. This exist to allow some margin (not
        restrict to no shadow).

    Returns
    -------
    kicking_bear : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 
    """
    kicking_type = "bear"
    kicking = kicking_calc(high, low, open_, close, periods, kicking_type, shadow_margin)
    return kicking

def piercing(high, low, open_, close, periods = 10):
    """
    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.

    Returns
    -------
    piercing : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 
    """
    piercing = piercing_calc(high, low, open_, close, periods)
    return piercing

def tws(high, low, open_, close, periods = 10):
    """
    Three White Soldiers

    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.

    Returns
    -------
    tws : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 
    """
    tws = tws_calc(high, low, open_, close, periods)
    return tws

def abandoned_baby_bull(high, low, open_, close, periods = 10):
    """
    Abandoned Baby Bull

    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.

    Returns
    -------
    pattern : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 
    """
    type_ = "bull"
    pattern = abandoned_baby_calc(high, low, open_, close, periods, type_)
    return pattern

def abandoned_baby_bear(high, low, open_, close, periods = 10):
    """
    Abandoned Baby Bear

    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.

    Returns
    -------
    pattern : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 
    """
    type_ = "bear"
    pattern = abandoned_baby_calc(high, low, open_, close, periods, type_)
    return pattern


def belthold_bull(high, low, open_, close, periods = 10, shadow_margin = 5.0):
    """
    Belt Hold Bull

    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.
    shadow_margin : `float`, optional
        Specify what margin should be allowed for the shadows. By using for 
        example 5%, both the lower and upper shadow can be as high as 5%
        of the candlestick body size. This exist to allow some margin (not
        restrict to no shadow).

    Returns
    -------
    pattern : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 
    """
    type_ = "bull"
    pattern = belthold_calc(high, low, open_, close, periods, type_, shadow_margin)
    return pattern
    

def belthold_bear(high, low, open_, close, periods = 10, shadow_margin = 5.0):
    """
    Belt Hold Bear

    Parameters
    ----------
    high : `ndarray`
        An array containing high prices.
    low : `ndarray`
        An array containing low prices.
    open_ : `ndarray`
        An array containing open prices.
    close : `ndarray`
        An array containing close prices.
    periods : `int`, optional
        Specifying number of periods for trend identification.
    shadow_margin : `float`, optional
        Specify what margin should be allowed for the shadows. By using for 
        example 5%, both the lower and upper shadow can be as high as 5%
        of the candlestick body size. This exist to allow some margin (not
        restrict to no shadow).

    Returns
    -------
    pattern : `ndarray`
        A numpy ndarray of type bool specifying true whether
        a pattern has been found or false otherwise. 
    """
    type_ = "bear"
    pattern = belthold_calc(high, low, open_, close, periods, type_, shadow_margin)
    return pattern
