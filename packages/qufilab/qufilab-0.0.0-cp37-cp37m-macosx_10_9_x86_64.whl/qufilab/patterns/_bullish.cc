/*
 *  @QufiLab, Anton Normelius, 2020.
 *
 *  Bullish candlestick patterns.
 *
 */

#include <iostream>
#include <string>
#include <cmath>
#include <limits>
#include <numeric>
#include <cstdint>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include "_bullish.h"

#include "candlestick.h"
#include "data_container.h"
#include "pattern_utility.h"
#include "conditions.h"

#include "../indicators/util.h"
#include "../indicators/_trend.h"

namespace py = pybind11;

/*
 *  Implementation of HAMMER.
 *
 *  Params:
 *      high (py::array_t<T>) : Array with high prices.
 *      low (py::array_t<T>) : Array with low prices.
 *      open (py::array_t<T>) : Array with opening prices.
 *      close (py::array_t<T>) : Array with close prices.
 *      trend_period (int) : Specify the period for identify trend.
 *      type (str) : Specify whether 'hammer' or 'inverted_hammer' 
 *          should be calculated.
 *      shadow_marign (T) : How much margin should be allowed on the 
 *          upper shadow.
 */
template <typename T>
py::array_t<bool> hammer_calc(const py::array_t<T> high, 
        const py::array_t<T> low, const py::array_t<T> open, 
        const py::array_t<T> close, const int trend_period, 
        const std::string type, const T shadow_margin) {
    
    const int body_avg_period = 14;

    InputContainer<T> data = {high, low, open, close};
    ResultContainer result_container = {data.size};
    auto trend = get_trend("sma", close, trend_period);
    auto body_avg = get_body_avg(open, close, body_avg_period);

    for (int idx = body_avg_period; idx < data.size; ++idx) {
        Candlestick<T> candle = {data.high[idx], data.low[idx], 
            data.open[idx], data.close[idx], body_avg[idx], trend[idx]};

        bool conditions = hammer_conditions(candle, shadow_margin, type);
        if (conditions == true) {
            result_container.found_pattern(idx);
        }
    }

    return result_container.result;
}


/*
 *  Implementation of DOJI.
 *  
 *  Params:
 *      high (py::array_t<T>) : Array with high prices.
 *      low (py::array_t<T>) : Array with low prices.
 *      open (py::array_t<T>) : Array with opening prices.
 *      close (py::array_t<T>) : Array with close prices.
 *      trend_period (int) : Specify the period for identify trend.
 */
template <typename T>
py::array_t<bool> doji_calc(const py::array_t<T> high, 
        const py::array_t<T> low, const py::array_t<T> open, 
        const py::array_t<T> close, const int trend_period) {

    const int body_avg_period = 14;

    InputContainer<T> data = {high, low, open, close};
    ResultContainer result_container = {data.size};
    auto trend = get_trend("sma", close, trend_period);
    auto body_avg = get_body_avg(open, close, body_avg_period);

    for (int idx = body_avg_period ; idx < data.size; ++idx) {
        Candlestick<T> candle = {data.high[idx], data.low[idx], 
            data.open[idx], data.close[idx], body_avg[idx], trend[idx]};

        bool correct_cond = doji_conditions(candle);
        if (correct_cond) {
            result_container.found_pattern(idx);
        }

    }    

    return result_container.result;
}


/*
 *  Implementation of DRAGONFLY_DOJI.
 *  
 *  Params:
 *      high (py::array_t<T>) : Array with high prices.
 *      low (py::array_t<T>) : Array with low prices.
 *      open (py::array_t<T>) : Array with opening prices.
 *      close (py::array_t<T>) : Array with close prices.
 *      trend_period (int) : Specify the period for identify trend.
 */
template <typename T>
py::array_t<bool> dragonfly_doji_calc(const py::array_t<T> high, 
        const py::array_t<T> low, const py::array_t<T> open, 
        const py::array_t<T> close, const int trend_period) {
    
    const int body_avg_period = 14;

    InputContainer<T> data = {high, low, open, close};
    ResultContainer result_container = {data.size};
    auto trend = get_trend("sma", close, trend_period);
    auto body_avg = get_body_avg(open, close, body_avg_period);

    for (int idx = body_avg_period; idx < data.size; ++idx) {
        Candlestick<T> candle = {data.high[idx], data.low[idx], 
            data.open[idx], data.close[idx], body_avg[idx], trend[idx]};
        
        bool correct_cond = dragonfly_doji_conditions(candle);
        if (correct_cond) {
            result_container.found_pattern(idx);
        }
    }    

    return result_container.result;
}

/*
 *  Implementation of MARUBOZU_WHITE.
 *  
 *  Params:
 *      high (py::array_t<T>) : Array with high prices.
 *      low (py::array_t<T>) : Array with low prices.
 *      open (py::array_t<T>) : Array with opening prices.
 *      close (py::array_t<T>) : Array with close prices.
 *      shadow_margin (float) : Float specifying what margin should be allowed
 *          for the shadows. For example, by using shadow_marign = 5, one allows
 *          the upper/lower shadows to be as high as 5% of the body size.
 *      trend_period (int) : Specify the period for identify trend.
 */
template <typename T>
py::array_t<bool> marubozu_white_calc(const py::array_t<T> high, 
        const py::array_t<T> low, const py::array_t<T> open, 
        py::array_t<T> close, T shadow_margin, const int trend_period) {

    const int body_avg_period = 14;

    InputContainer<T> data = {high, low, open, close};
    ResultContainer result_container = {data.size};
    auto trend = get_trend("sma", close, trend_period);
    auto body_avg = get_body_avg(open, close, body_avg_period);

    for (int idx = body_avg_period; idx < data.size; ++idx) {
        Candlestick<T> candle = {data.high[idx], data.low[idx], 
            data.open[idx], data.close[idx], body_avg[idx], trend[idx]};
        
        bool correct_cond = marubozu_white_conditions(candle, shadow_margin);
        if (correct_cond) {
            result_container.found_pattern(idx);
        }
    }    

    return result_container.result;
}

/*
 *  Implementation of MARUBOZU_BLACK.
 *  
 *  Params:
 *      high (py::array_t<T>) : Array with high prices.
 *      low (py::array_t<T>) : Array with low prices.
 *      open (py::array_t<T>) : Array with opening prices.
 *      close (py::array_t<T>) : Array with close prices.
 *      shadow_margin (float) : Float specifying what margin should be allowed
 *          for the shadows. For example, by using shadow_marign = 5, one allows
 *          the upper/lower shadows to be as high as 5% of the body size.
 *      trend_period (int) : Specify the period for identify trend.
 */
template <typename T>
py::array_t<bool> marubozu_black_calc(const py::array_t<T> high, 
        const py::array_t<T> low, const py::array_t<T> open, 
        py::array_t<T> close, T shadow_margin, const int trend_period) {

    const int body_avg_period = 14;

    InputContainer<T> data = {high, low, open, close};
    ResultContainer result_container = {data.size};
    auto trend = get_trend("sma", close, trend_period);
    auto body_avg = get_body_avg(open, close, body_avg_period);

    for (int idx = body_avg_period; idx < data.size; ++idx) {
        Candlestick<T> candle = {data.high[idx], data.low[idx], 
            data.open[idx], data.close[idx], body_avg[idx], trend[idx]};
        
        bool correct_cond = marubozu_black_conditions(candle, shadow_margin);
        if (correct_cond) {
            result_container.found_pattern(idx);
        }
    }    

    return result_container.result;
}

/*
 *  Implementation of SPINNING_TOP_WHITE.
 *  
 *  Params:
 *      high (py::array_t<T>) : Array with high prices.
 *      low (py::array_t<T>) : Array with low prices.
 *      open (py::array_t<T>) : Array with opening prices.
 *      close (py::array_t<T>) : Array with close prices.
 *      trend_period (int) : Specify the period for identify trend.
 */
template <typename T>
py::array_t<bool> spinning_top_white_calc(const py::array_t<T> high, 
        const py::array_t<T> low, const py::array_t<T> open, 
        py::array_t<T> close, const int trend_period) {
    
    const int body_avg_period = 14;

    InputContainer<T> data = {high, low, open, close};
    ResultContainer result_container = {data.size};
    auto trend = get_trend("sma", close, trend_period);
    auto body_avg = get_body_avg(open, close, body_avg_period);

    for (int idx = body_avg_period; idx < data.size; ++idx) {
        Candlestick<T> candle = {data.high[idx], data.low[idx], 
            data.open[idx], data.close[idx], body_avg[idx], trend[idx]};

        bool correct_cond = spinning_top_white_conditions(candle);
        if (correct_cond) {
            result_container.found_pattern(idx);
        }
    }    

    return result_container.result;
}

/*
 *  Implementation of ENGULFING.
 *  
 *  Params:
 *      high (py::array_t<T>) : Array with high prices.
 *      low (py::array_t<T>) : Array with low prices.
 *      open (py::array_t<T>) : Array with opening prices.
 *      close (py::array_t<T>) : Array with close prices.
 *      trend_period (int) : Period for moving average in order to identify trend.
 *      type (string) : Specify what kind of engulfing type that should
 *          be calculated. Can choose from 'bull' or 'bear'.
 */
template <typename T>
py::array_t<bool> engulfing_calc(const py::array_t<T> high, 
        const py::array_t<T> low, const py::array_t<T> open, 
        py::array_t<T> close, const int trend_period, 
        const std::string type) {
    
    const int body_avg_period = 14;

    InputContainer<T> data = {high, low, open, close};
    ResultContainer result_container = {data.size};
    auto trend = get_trend("sma", close, trend_period);
    auto body_avg = get_body_avg(open, close, body_avg_period);

    for (int idx = body_avg_period + 1; idx < data.size; ++idx) {
        Candlestick<T> candle_prev = {data.high[idx-1], data.low[idx-1], 
            data.open[idx-1], data.close[idx-1], body_avg[idx-1], trend[idx-1]};

        Candlestick<T> candle = {data.high[idx], data.low[idx], 
            data.open[idx], data.close[idx], body_avg[idx], trend[idx]};
        
        bool correct_cond = engulfing_conditions(candle, candle_prev, type);
        if (correct_cond) {
            result_container.found_pattern(idx);
        }

    }

    return result_container.result;
}

/*
 *  Implementation of HARAMI.
 *  
 *  Params:
 *      high (py::array_t<T>) : Array with high prices.
 *      low (py::array_t<T>) : Array with low prices.
 *      open (py::array_t<T>) : Array with opening prices.
 *      close (py::array_t<T>) : Array with close prices.
 *      trend_period (int) : Period for moving average in order to identify trend.
 *      type (string) : Specify what kind of harami type that should
 *          be calculated. Can choose from 'bull' or 'bear'.
 */
template <typename T>
py::array_t<bool> harami_calc(const py::array_t<T> high, 
        const py::array_t<T> low, const py::array_t<T> open, 
        py::array_t<T> close, const int trend_period, 
        const std::string type) {
    
    const int body_avg_period = 14;

    InputContainer<T> data = {high, low, open, close};
    ResultContainer result_container = {data.size};
    auto trend = get_trend("sma", close, trend_period);
    auto body_avg = get_body_avg(open, close, body_avg_period);
    
    for (int idx = body_avg_period + 1; idx < data.size; ++idx) {
        Candlestick<T> candle_prev = {data.high[idx-1], data.low[idx-1], 
            data.open[idx-1], data.close[idx-1], body_avg[idx-1], trend[idx-1]};

        Candlestick<T> candle = {data.high[idx], data.low[idx], 
            data.open[idx], data.close[idx], body_avg[idx], trend[idx]};
    
        bool correct_cond = harami_conditions(candle, candle_prev, type);
        if (correct_cond) {
            result_container.found_pattern(idx);
        }

    }

    return result_container.result;
}

/*
 *  Implementation of KICKING.
 *   
 *  Params:
 *      high (py::array_t<T>) : Array with high prices.
 *      low (py::array_t<T>) : Array with low prices.
 *      open (py::array_t<T>) : Array with opening prices.
 *      close (py::array_t<T>) : Array with close prices.
 *      trend_period (int) : Period for moving average in order to identify trend.
 *      type (string) : Specify what kind of kicking type that should
 *          be calculated. Can choose from 'bull' or 'bear'.
 *      shadow_margin (float) : Float specifying what margin should be allowed
 *          for the shadows. For example, by using shadow_marign = 5, one allows
 *          the upper/lower shadows to be as long as 5% of the body size.
 */
template <typename T>
py::array_t<bool> kicking_calc(const py::array_t<T> high, 
        const py::array_t<T> low, const py::array_t<T> open, 
        py::array_t<T> close, const int trend_period, const std::string type,
        const float shadow_margin) {

    const int body_avg_period = 14;

    InputContainer<T> data = {high, low, open, close};
    ResultContainer result_container = {data.size};
    auto trend = get_trend("sma", close, trend_period);
    auto body_avg = get_body_avg(open, close, body_avg_period);

    for (int idx = body_avg_period + 1; idx < data.size; ++idx) {
        Candlestick<T> candle_prev = {data.high[idx-1], data.low[idx-1], 
            data.open[idx-1], data.close[idx-1], body_avg[idx-1], trend[idx-1]};

        Candlestick<T> candle = {data.high[idx], data.low[idx], 
            data.open[idx], data.close[idx], body_avg[idx], trend[idx]};
        
        bool correct_cond = kicking_conditions(candle, candle_prev, shadow_margin,
                type);
        if (correct_cond) {
            result_container.found_pattern(idx);
        }
    }

    return result_container.result;
}

/*
 *  Implementation of PIERCING.
 *  
 *  Params:
 *      high (py::array_t<T>) : Array with high prices.
 *      low (py::array_t<T>) : Array with low prices.
 *      open (py::array_t<T>) : Array with opening prices.
 *      close (py::array_t<T>) : Array with close prices.
 *      trend_period (int) : Period for moving average in order to identify trend.
 */
template <typename T>
py::array_t<bool> piercing_calc(const py::array_t<T> high, 
        const py::array_t<T> low, const py::array_t<T> open, 
        py::array_t<T> close, const int trend_period) {

    const int body_avg_period = 14;

    InputContainer<T> data = {high, low, open, close};
    ResultContainer result_container = {data.size};
    auto trend = get_trend("sma", close, trend_period);
    auto body_avg = get_body_avg(open, close, body_avg_period);
    
    for (int idx = body_avg_period + 1; idx < data.size; ++idx) {
        Candlestick<T> candle_prev = {data.high[idx-1], data.low[idx-1], 
            data.open[idx-1], data.close[idx-1], body_avg[idx-1], trend[idx-1]};

        Candlestick<T> candle = {data.high[idx], data.low[idx], 
            data.open[idx], data.close[idx], body_avg[idx], trend[idx]};
    
        bool correct_cond = piercing_conditions(candle, candle_prev);
        if (correct_cond) {
            result_container.found_pattern(idx);
        }
    }

    return result_container.result;
}

/*
 *  Implementation of THREE WHITE SOLDIERS.
 *  
 *  Params:
 *      high (py::array_t<T>) : Array with high prices.
 *      low (py::array_t<T>) : Array with low prices.
 *      open (py::array_t<T>) : Array with opening prices.
 *      close (py::array_t<T>) : Array with close prices.
 *      trend_period (int) : Period for moving average in order to identify trend.
 */
template <typename T>
py::array_t<bool> tws_calc(const py::array_t<T> high, 
        const py::array_t<T> low, const py::array_t<T> open, 
        py::array_t<T> close, const int trend_period) {

    const int body_avg_period = 14;

    InputContainer<T> data = {high, low, open, close};
    ResultContainer result_container = {data.size};
    auto trend = get_trend("sma", close, trend_period);
    auto body_avg = get_body_avg(open, close, body_avg_period);

    for (int idx = body_avg_period + 2; idx < data.size; ++idx) {
        Candlestick<T> c1 = {data.high[idx], data.low[idx], 
            data.open[idx], data.close[idx], body_avg[idx], trend[idx]};

        Candlestick<T> c2 = {data.high[idx-1], data.low[idx-1], 
            data.open[idx-1], data.close[idx-1], body_avg[idx-1], trend[idx-1]};

        Candlestick<T> c3 = {data.high[idx-2], data.low[idx-2], 
            data.open[idx-2], data.close[idx-2], body_avg[idx-2], trend[idx-2]};

        auto correct_cond = tws_conditions(c1, c2, c3);
        if (correct_cond) {
            result_container.found_pattern(idx);
        }
    }

    return result_container.result;;
}

/*
 *  Implementation of ABANDONED BABY.
 *  
 *  Params:
 *      high (py::array_t<T>) : Array with high prices.
 *      low (py::array_t<T>) : Array with low prices.
 *      open (py::array_t<T>) : Array with opening prices.
 *      close (py::array_t<T>) : Array with close prices.
 *      trend_period (int) : Period for moving average in order to identify trend.
 */
template <typename T>
py::array_t<bool> abandoned_baby_calc(const py::array_t<T> high, 
        const py::array_t<T> low, const py::array_t<T> open, 
        py::array_t<T> close, const int trend_period, const std::string type) {

    const int body_avg_period = 14;

    InputContainer<T> data = {high, low, open, close};
    ResultContainer result_container = {data.size};
    auto trend = get_trend("sma", close, trend_period);
    auto body_avg = get_body_avg(open, close, body_avg_period);

    for (int idx = body_avg_period + 2; idx < data.size; ++idx) {
        Candlestick<T> c1 = {data.high[idx], data.low[idx], 
            data.open[idx], data.close[idx], body_avg[idx], trend[idx]};

        Candlestick<T> c2 = {data.high[idx-1], data.low[idx-1], 
            data.open[idx-1], data.close[idx-1], body_avg[idx-1], trend[idx-1]};

        Candlestick<T> c3 = {data.high[idx-2], data.low[idx-2], 
            data.open[idx-2], data.close[idx-2], body_avg[idx-2], trend[idx-2]};

        bool correct_cond = abandoned_baby_conditions(c1, c2, c3, type);
        if (correct_cond) {
            result_container.found_pattern(idx);
        }
    }

    return result_container.result;
}

/*
 *  Implementation of Belt Hold.
 *  
 *  Params:
 *      high (py::array_t<T>) : Array with high prices.
 *      low (py::array_t<T>) : Array with low prices.
 *      open (py::array_t<T>) : Array with opening prices.
 *      close (py::array_t<T>) : Array with close prices.
 *      trend_period (int) : Period for moving average in order to identify trend.
 */
template <typename T>
py::array_t<bool> belthold_calc(const py::array_t<T> high, 
        const py::array_t<T> low, const py::array_t<T> open, 
        py::array_t<T> close, const int trend_period, const std::string type,
        const float shadow_margin) {

    const int body_avg_period = 14;

    InputContainer<T> data = {high, low, open, close};
    ResultContainer result_container = {data.size};
    auto trend = get_trend("sma", close, trend_period);
    auto body_avg = get_body_avg(open, close, body_avg_period);

    for (int idx = body_avg_period; idx < data.size; ++idx) {
        Candlestick<T> candle = {data.high[idx], data.low[idx], 
            data.open[idx], data.close[idx], body_avg[idx], trend[idx]};

        bool correct_cond = belthold_conditions(candle, type, shadow_margin);
        if (correct_cond) {
            result_container.found_pattern(idx);
        }
    }

    return result_container.result;
}


PYBIND11_MODULE(_bullish, m) {
    m.def("hammer_calc", &hammer_calc<double>, "Hammer pattern");
    m.def("hammer_calc", &hammer_calc<double>, "Hammer pattern");

    m.def("doji_calc", &doji_calc<double>, "Doji pattern");
    m.def("doji_calc", &doji_calc<float>, "Doji pattern");

    m.def("dragonfly_doji_calc", &dragonfly_doji_calc<double>, "Dragonfly doji pattern");
    m.def("dragonfly_doji_calc", &dragonfly_doji_calc<float>, "Dragonfly doji pattern");

    m.def("marubozu_white_calc", &marubozu_white_calc<double>, "Marubozu white pattern");
    m.def("marubozu_white_calc", &marubozu_white_calc<float>, "Marubozu white pattern");

    m.def("marubozu_black_calc", &marubozu_black_calc<double>, "Marubozu black pattern");
    m.def("marubozu_black_calc", &marubozu_black_calc<float>, "Marubozu black pattern");

    m.def("spinning_top_white_calc", &spinning_top_white_calc<double>, "Spinning top white pattern");
    m.def("spinning_top_white_calc", &spinning_top_white_calc<float>, "Spinning top white pattern");

    m.def("engulfing_calc", &engulfing_calc<double>, "Engulfing pattern");
    m.def("engulfing_calc", &engulfing_calc<float>, "Engulfing pattern");

    m.def("harami_calc", &harami_calc<double>, "Harami pattern");
    m.def("harami_calc", &harami_calc<float>, "Harami pattern");

    m.def("kicking_calc", &kicking_calc<double>, "Kicking pattern");
    m.def("kicking_calc", &kicking_calc<float>, "Kicking pattern");

    m.def("piercing_calc", &piercing_calc<double>, "Piercing pattern");
    m.def("piercing_calc", &piercing_calc<float>, "Piercing pattern");

    m.def("tws_calc", &tws_calc<double>, "Three White Soldiers pattern");
    m.def("tws_calc", &tws_calc<float>, "Three White Soldiers pattern");

    m.def("abandoned_baby_calc", &abandoned_baby_calc<double>, "Abandoned baby pattern");
    m.def("abandoned_baby_calc", &abandoned_baby_calc<float>, "Abandoned baby pattern");

    m.def("belthold_calc", &belthold_calc<double>, "Belt Hold pattern");
    m.def("belthold_calc", &belthold_calc<float>, "Belt Hold pattern");

}

