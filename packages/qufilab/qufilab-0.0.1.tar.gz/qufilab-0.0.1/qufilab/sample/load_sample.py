

import pandas as pd
import os

def load_sample(ticker):
    """
    Parameters
    ----------
    ticker : {'AAPL', 'NFLX', 'MSFT'}
        Ticker to load data for.
    
    Returns
    -------
    `DataFrame`
        DataFrame containing `date`, `high`, `low`, `open`, `close`, `volume`.
    """
    if not isinstance(ticker, str):
        raise TypeError("Param 'ticker' needs to be a str.")
    
    if ticker not in ['MSFT', 'NFLX', 'TSLA', 'DJI']:
        raise ValueError("Param 'ticker' needs to be 'MSFT', 'NFLX', 'DJI'" \
                " or 'TSLA'.")

    df = pd.read_csv(os.path.join(os.path.dirname(__file__), ticker + ".csv"))
    pd.to_datetime(df['date'], format = '%Y-%m-%d') 
    return df

