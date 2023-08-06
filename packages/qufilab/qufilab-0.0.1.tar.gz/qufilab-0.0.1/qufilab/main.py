"""
@ Quant
@ Anton Normelius, 2020.

Interface for the quantitative models.
"""

import pandas as pd

#from quant.models import openChange

class Models():
    def __init__(self, data):
        """
        Params:
            data (pd DataFrame).
        """
        self.data = data
        self.close = self.data['close'].tolist()
        self.open = self.data['open'].tolist()
        self.high = self.data['high'].tolist()
        self.low = self.data['low'].tolist()
        self.date = self.data['date'].tolist()
    
    def openChange(self, mode, entry, direction, cover, stop_loss = 0.0, 
            show_positions = False):
        """
        Model to analyse change on initial opening.
        """
        if entry == 0:
            raise ValueError("Param entry can't be 0")

        mode = mode.lower()
        if mode not in ['daily', 'percentage']:
            raise ValueError("Param mode needs to be 'daily' or 'percentage'.")

        if mode == 'daily':
            if not isinstance(cover, int):
                raise ValueError("Param cover needs to be an int," \
                        " specifying number of days before covering position.")

            openChange(self.date, self.close, self.open, self.high, self.low,
                    entry, mode, direction, cover, stop_loss, show_positions)

        elif mode == 'percentage':
            if (stop_loss == 0.0):
                raise ValueError("Param stop_loss needs to be specified")

            if (cover <= 0 or cover >= 1):
                raise ValueError("Param cover needs to be bigger than zero" \
                        " but less than one.")


            #openChange(self.date, self.close, self.open, self.high, self.low,
            #        entry, mode, direction, cover, stop_loss, show_positions)

    
    #def trendCrossover(self, indicator, periods, deviation = 0):
    #    """
    #    Model to analyze positions when price cross trend indicator.
    #    """
    #    indicators = ['sma', 'ema', 'smma', 'lwma', 'bollinger_bands']

    #    indicator = indicator.lower()

    #    if indicator not in indicators:
    #        raise ValueError("param 'indicator' needs to be specified")
    #    
    #    if not periods:
    #        raise ValueError("param 'periods' needs to be speicified.")
    #
    #    if indicator == 'bb' and std_dev == 0:
    #        raise ValueError("param 'std_dev' needs to be speicified.")

    #    if indicator == 'bb' and not isinstance(std_dev, int):
    #        raise ValueError("param 'std_dev' needs to be an int.")

    #    trendCrossover(self.date, self.close, self.open, self.high, self.low,
    #            indicator, periods, deviation)





