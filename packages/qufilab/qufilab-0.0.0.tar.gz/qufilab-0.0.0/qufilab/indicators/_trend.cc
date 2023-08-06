/*
 * @ Quant, Anton Normelius, 2020.
 *
 * Module to handle indicator calculations.
 *
 * */

#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <sstream>
#include <limits>
#include <numeric>
#include <type_traits>
#include <cstdint>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include "_trend.h"
#include "util.h" // Init nans.

namespace py = pybind11;

/*
    Implementation of SMA.
    Simple Moving Average.

    @param prices (py::array_t<double>): Array with prices.
    @param periods (int): Number of periods.
 */
template <typename T>
py::array_t<T> sma_calc(const py::array_t<T> price, const int period) {
    py::buffer_info price_buf = price.request();
    auto *price_ptr = (T*) price_buf.ptr;
    const int size = price_buf.shape[0];

    auto sma = py::array_t<T>(price_buf.size);
    auto *sma_ptr = (T*) sma.request().ptr;
    init_nan(sma_ptr, size);

    // Check leading NaNs and adjust calculation below. This is needed if arg prices contain
    // leading NaNs, which will occur when calculating other indicators.
    int adjust_nan = 0;
    for (int idx = 0; idx < size; ++idx) {
        if (std::isnan(price_ptr[idx])) {
            ++adjust_nan;
        }

        else {
            break;
        }
    }

    T temp = 0;
    for (int idx = 0 + adjust_nan; idx < size; ++idx) {
        temp += price_ptr[idx]; 

        if (idx >= period + adjust_nan) {
            temp -= price_ptr[idx - period];
        }   

        if (idx >= (period - 1 + adjust_nan)) {
            sma_ptr[idx] = ((T) temp / period);
        }
    }

    return sma;
}


template <typename T>
py::array_t<T> sma_calc_test(py::array_t<T> price, const int period) {

    py::buffer_info price_buf = price.request();
    T* price_ptr = (T*) price_buf.ptr;
    const int size = price_buf.shape[0];

    py::array_t<T> sma = py::array_t<T>(price_buf.size);
    T* sma_ptr = (T*) sma.request().ptr;
    init_nan(sma_ptr, size);

    // Check leading NaNs and adjust calculation below. This is needed if arg prices contain
    // leading NaNs, which will occur when calculating other indicators.
    int adjust_nan = 0;
    for (int idx = 0; idx < size; ++idx) {
        if (std::isnan(price_ptr[idx])) {
            ++adjust_nan;
        }

        else {
            break;
        }
    }

    T temp = 0;
    for (int idx = 0 + adjust_nan; idx < size; ++idx) {
        temp += price_ptr[idx]; 

        if (idx >= period + adjust_nan) {
            temp -= price_ptr[idx - period];
        }   

        if (idx >= (period - 1 + adjust_nan)) {
            sma_ptr[idx] = ((T) temp / period);
        }
    }

    return sma;
}



/*
    Implementation of EMA.
    Exponential Moving Average

    Math: (close - ema(prev)) * k + ema(prev)

    @param prices (vector<double>): Vector with prices.
    @param periods (int): Number of periods.
 */
template <typename T>
py::array_t<T> ema_calc(const py::array_t<T> prices, const int periods) {
    py::buffer_info prices_buf = prices.request();
    auto *prices_ptr = (T *) prices_buf.ptr;
    const int size = prices_buf.shape[0];
    
    auto ema = py::array_t<T>(prices_buf.size);
    auto *ema_ptr = (T *) ema.request().ptr;
    init_nan(ema_ptr, size);
    
    // Check leading NaNs and adjust calculation below. This is needed if arg prices contain
    // leading NaNs, which will occur when calculating other indicators.
    int adjust_nan = 0;
    for (int idx = 0; idx < size; ++idx) {
        if (std::isnan(prices_ptr[idx])) {
            ++adjust_nan;
        }

        else {
            break;
        }
    }

    // Start with sma for first data point.
    T prev = std::accumulate(prices_ptr + adjust_nan, prices_ptr + periods + adjust_nan, 0.0);
    prev /= periods;

    // Multiplier, i.e. 18.18% weight with period 10;
    T k = (T) 2 / (periods + 1);
    //prev = (prices[periods-1] - prev) * k + prev;
    ema_ptr[periods - 1 + adjust_nan] = prev;

    for (int idx = periods + adjust_nan; idx < size; idx++) {
        prev = (prices_ptr[idx] - prev) * k + prev;
        ema_ptr[idx] = prev;
    }

    return ema;
}


/*
    Implementation of DEMA.
    Double Exponential Moving Average

    Math: DEMA = 2 * EMA_N - EMA(EMA_N).

    @param prices (py::array_t<double>): Array with prices.
    @param periods (int): Number of periods.
 */
template <typename T>
py::array_t<T> dema_calc(const py::array_t<T> prices, const int periods) {
    
    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];

    auto ema1 = ema_calc(prices, periods);
    auto ema2 = ema_calc(ema1, periods);
    
    auto *ema1_ptr = (T *) ema1.request().ptr;
    auto *ema2_ptr = (T *) ema2.request().ptr;

    auto dema = py::array_t<T>(prices_buf.size);
    auto *dema_ptr = (T*) dema.request().ptr;
    init_nan(dema_ptr, size);

    for (int idx = 2*periods-2; idx < ema1.size(); ++idx) {
        dema_ptr[idx] = 2 * ema1_ptr[idx] - ema2_ptr[idx];
    }

    return dema;
}

/*
    Implementation of TEMA.
    Triple Exponential Moving Average
    Math: TEMA = (3* EMA_1) - (3 * EMA_2) + EMA_3.

    @param prices (py::array_t<double>): Array with prices.
    @param periods (int): Number of periods.
 */
template <typename T>
py::array_t<T> tema_calc(const py::array_t<T> prices, const int periods) {
    
    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];

    auto ema1 = ema_calc(prices, periods);
    auto ema2 = ema_calc(ema1, periods);
    auto ema3 = ema_calc(ema2, periods);
    
    auto *ema1_ptr = (T *) ema1.request().ptr;
    auto *ema2_ptr = (T *) ema2.request().ptr;
    auto *ema3_ptr = (T *) ema3.request().ptr;

    auto tema = py::array_t<T>(prices_buf.size);
    auto *tema_ptr = (T *) tema.request().ptr;
    init_nan(tema_ptr, size);

    for (int idx = 3*periods-3; idx < prices.size(); ++idx) {
        tema_ptr[idx] = (3*ema1_ptr[idx]) - (3*ema2_ptr[idx]) + ema3_ptr[idx];
    }

    return tema;
}

/*
    Implementation of T3.
    T3 Moving Average.

    Math: T3 = c1*e6 + c2*e5 + c3*e4 + c4*e3.
        e1 = EMA (Close, Period)
        e2 = EMA (e1, Period)
        e3 = EMA (e2, Period)
        e4 = EMA (e3, Period)
        e5 = EMA (e4, Period)
        e6 = EMA (e5, Period)
        a is the volume factor, default value is 0.7 but 0.618 can also be used.
        c1 = – a^3
        c2 = 3*a^2 + 3*a^3
        c3 = – 6*a^2 – 3*a – 3*a^3
        c4 = 1 + 3*a + a^3 + 3*a^2

    @param prices (py::array_t<double>): Array with prices.
    @param periods (int): Number of periods.
 */
template <typename T>
py::array_t<T> t3_calc(const py::array_t<T> prices, const int periods,
        const double volume_factor) {
    py::buffer_info prices_buf = prices.request();
    auto *prices_ptr = (T *) prices_buf.ptr;
    const int size = prices_buf.shape[0];

    auto t3 = py::array_t<T>(prices_buf.size);
    auto *t3_ptr = (T *) t3.request().ptr;
    init_nan(t3_ptr, size);
    
    auto ema1 = ema_calc(prices, periods);
    auto ema2 = ema_calc(ema1, periods);
    auto ema3 = ema_calc(ema2, periods);
    auto ema4 = ema_calc(ema3, periods);
    auto ema5 = ema_calc(ema4, periods);
    auto ema6 = ema_calc(ema5, periods);

    auto *ema3_ptr = (T *) ema3.request().ptr;
    auto *ema4_ptr = (T *) ema4.request().ptr;
    auto *ema5_ptr = (T *) ema5.request().ptr;
    auto *ema6_ptr = (T *) ema6.request().ptr;
    
    T c1 = -std::pow(volume_factor, 3);
    T c2 = 3 * std::pow(volume_factor, 2) + 3 * std::pow(volume_factor, 3);
    T c3 = - 6 * std::pow(volume_factor, 2) - 3 * volume_factor - 3 * std::pow(volume_factor, 3);
    T c4 = 1 + 3 * volume_factor + std::pow(volume_factor, 3) + 3 * std::pow(volume_factor, 2);
    
    for (int idx = periods*5-1; idx < size; ++idx) {
        t3_ptr[idx] = c1*ema6_ptr[idx] + c2*ema5_ptr[idx] + c3*ema4_ptr[idx] + c4*ema3_ptr[idx];
    }

    return t3;
}


/*
    Implementation of TMA.
    Triangular Moving Average

    Math: 
        If period is even: first_period = period / 2.
                           second_period = (period / 2) + 1.
        If period is uneven: first_period = second_period = (period+1)/2 rounded up.

        TMA = SMA(SMA(price, first_period), second_period)
    
    @param prices (py::array_t<double>): Array with prices.
    @param periods (int): Number of periods.

    OBSERVE that this implementation uses two sma calculations and can be optimzied
    further by extending the original sma implementation. However, it is going to 
    take some time doing the math so, leaving this for a rainy day.
 */
template <typename T>
py::array_t<T> tma_calc(const py::array_t<T> prices, const int period) {

    int first_period;
    int second_period;

    if (period % 2 == 0) {
        first_period = period / 2;
        second_period = (period / 2) + 1;
    }

    else {
        first_period = std::ceil((T) (period+1)/2);
        second_period = std::ceil((T) (period+1)/2);
    }

    py::array_t<T> sma = sma_calc(prices, first_period);
    py::array_t<T> tma = sma_calc(sma, second_period);

    return tma;
}

/*
   Implementation of SMMA.
   Smoothed Moving Average.

Math: 
1. First value = sma.
2. SMMA(i) = (SMMA1(i - 1) * (periods - 1) + prices(i)) / periods.

@param prices (vector<double>): Vector with prices.
@param periods (int): Number of periods.
@param defualt_size (int): Specify whether the returned vector
should be the default size with NaNs or not.
*/
template <typename T>
py::array_t<T> smma_calc(const py::array_t<T> prices, const int periods) {

    py::buffer_info prices_buf = prices.request();
    auto *prices_ptr = (T *) prices_buf.ptr;
    const int size = prices_buf.shape[0];

    auto smma = py::array_t<T>(prices_buf.size);
    auto *smma_ptr = (T *) smma.request().ptr;
    init_nan(smma_ptr, size);

    // Start with sma for first data point.
    T prev = std::accumulate(prices_ptr, prices_ptr + periods, 0.0);
    prev /= periods;
    //double prev = (smma1 * (periods - 1) + prices[periods-1]) / periods;
    smma_ptr[periods-1] = prev;

    for (int idx = periods; idx < size; idx++) {
        prev = (prev * (periods - 1) + prices_ptr[idx]) / periods;
        smma_ptr[idx] = prev;
    }

    return smma;
}


/*
   Implementation of LWMA.
   Linear Weighted Moving Average

Math: LWMA = sum(prices[i] * W(i)) / sum(W),
where W are the weights, ranging from 1-periods.

@param prices (vector<double>): Vector with prices.
@param periods (int): Number of periods.
@param defualt_size (int): Specify whether the returned vector
should be the default size with NaNs or not.
*/
template <typename T>
py::array_t<T> lwma_calc(const py::array_t<T> prices, const int periods) {

    py::buffer_info prices_buf = prices.request();
    auto *prices_ptr = (T*) prices_buf.ptr;
    const int size = prices_buf.shape[0];

    auto lwma = py::array_t<T>(prices_buf.size);
    auto *lwma_ptr = (T*) lwma.request().ptr;
    init_nan(lwma_ptr, size);

    for (int ii = 0; ii < size - periods + 1; ii++) {
        T temp = 0;
        int W = 1;
        int W_sum = 0;
        for (int idx = ii; idx < periods + ii; idx++) {
            temp += (prices_ptr[idx] * W);
            W_sum += W;
            W++;
        }

        temp /= W_sum;
        lwma_ptr[ii+periods-1] = temp;
    }

    return lwma;
}

/*
   Implementation of WC.
   Weighted Close.

Math: wc[i] = ((close * 2) + high + low) / 4,

@param prices (vector<double>): Vector with closing prices.
@param highs (vector<double>): Vector with high prices.
@param lows (vector<double>): Vector with low prices.
*/
template <typename T>
py::array_t<T> wc_calc(const py::array_t<T> closes, const py::array_t<T> highs,
     const py::array_t<T> lows) {

    py::buffer_info closes_buf = closes.request();
    auto *closes_ptr = (T*) closes_buf.ptr;
    py::buffer_info highs_buf = highs.request();
    auto *highs_ptr = (T*) highs_buf.ptr;
    py::buffer_info lows_buf = lows.request();
    auto *lows_ptr = (T*) lows_buf.ptr;

    const int size = closes_buf.shape[0];
    auto wc = py::array_t<T>(closes_buf.size);
    py::buffer_info wc_buf = wc.request();
    auto *wc_ptr = (T*) wc_buf.ptr;
    init_nan(wc_ptr, size);

    for (int idx = 0; idx < size; ++idx) {
        wc_ptr[idx] = ((closes_ptr[idx] * 2) + highs_ptr[idx] + lows_ptr[idx]) / 4;
    }

return wc;
}


PYBIND11_MODULE(_trend, m) {
    m.def("sma_calc", &sma_calc<double>, "Simple Moving Average");
    m.def("sma_calc", &sma_calc<float>, "Simple Moving Average");

    m.def("ema_calc", &ema_calc<double>, "Exponential Moving Average");
    m.def("ema_calc", &ema_calc<float>, "Exponential Moving Average");

    m.def("dema_calc", &dema_calc<double>, "Double Exponential Moving Average");
    m.def("dema_calc", &dema_calc<float>, "Double Exponential Moving Average");

    m.def("tema_calc", &tema_calc<double>, "Triple Exponential Moving Average");
    m.def("tema_calc", &tema_calc<float>, "Triple Exponential Moving Average");

    m.def("t3_calc", &t3_calc<double>, "T3 Moving Average");
    m.def("t3_calc", &t3_calc<float>, "T3 Moving Average");

    m.def("tma_calc", &tma_calc<double>, "Triangular Moving Average");
    m.def("tma_calc", &tma_calc<float>, "Triangular Moving Average");

    m.def("smma_calc", &smma_calc<double>, "Smoothed Moving Average");
    m.def("smma_calc", &smma_calc<float>, "Smoothed Moving Average");

    m.def("lwma_calc", &lwma_calc<double>, "Linear Weighted Moving Average");
    m.def("lwma_calc", &lwma_calc<float>, "Linear Weighted Moving Average");

    m.def("wc_calc", &wc_calc<double>, "Weighted Close");
    m.def("wc_calc", &wc_calc<float>, "Weighted Close");
}
