/*
 *  @ Quant
 *  @ Anton Normelius, 2020.
 *
 *  Statistics calculations.
 *
 */

#include <iostream>
#include <vector>
#include <string>
#include <limits>
#include <numeric>
#include <cstdint>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include "_stat.h"
#include "_trend.h"
#include "util.h"

namespace py = pybind11;

/*
 * Implementation of STD.
 *
 * Calculates the standard deviation. 
 * Using normalization by default.
*/

template <typename T>
py::array_t<T> std_calc(const py::array_t<T> prices,
         const int period, const bool normalize) {

    py::buffer_info prices_buf = prices.request();
    auto *prices_ptr = (T *) prices_buf.ptr;
    const int size = prices_buf.shape[0];

    auto sma = sma_calc(prices, period);
    auto *sma_ptr = (T *) sma.request().ptr;

    auto std = py::array_t<T>(prices_buf.size);
    auto *std_ptr = (T *) std.request().ptr;
    init_nan(std_ptr, size);

    for (int ii = 0; ii < size - period+ 1; ii++) {
        T temp = 0;

        for (int idx = ii; idx < period+ ii; idx++) {
            temp += pow((prices_ptr[idx] - sma_ptr[ii+period-1]), 2);
        }

        if (normalize == true) {
            temp /= (period - 1);
        }

        else {
            temp /= (period);
        }
  
        temp = sqrt(temp);
        std_ptr[ii+period-1] = temp;
    }

    return std;
}

/*
 * Implementation of VAR.
 *
 * Calculates the variance. 
*/
template <typename T>
py::array_t<T> var_calc(const py::array_t<T> prices,
         const int period, const bool normalize) {

    py::buffer_info prices_buf = prices.request();
    auto *prices_ptr = (T *) prices_buf.ptr;
    const int size = prices_buf.shape[0];

    auto sma = sma_calc(prices, period);
    auto *sma_ptr = (T *) sma.request().ptr;

    auto var = py::array_t<T>(prices_buf.size);
    auto *var_ptr = (T *) var.request().ptr;
    init_nan(var_ptr, size);

    int adjust_nan = 0;
    for (int idx = 0; idx < size; ++idx) {
        if (std::isnan(prices_ptr[idx])) {
            ++adjust_nan;
        }

        else {
            break;
        }
    }

    for (int ii = 0 + adjust_nan; ii < size - period + 1; ii++) {
        T temp = 0;

        for (int idx = ii; idx < period+ ii; idx++) {
            temp += pow((prices_ptr[idx] - sma_ptr[ii+period-1]), 2);
        }

        if (normalize == true) {
            temp /= (period- 1);
        }

        else {
            temp /= (period);
        }
  
        var_ptr[ii+period-1] = temp;
    }

    return var;
}

/*
 * Implementation of COV.
 *
 * Calculates the covariance between one price array and another.. 
*/

template <typename T>
py::array_t<T> cov_calc(const py::array_t<T> prices, const py::array_t<T> market,
         const int period, const bool normalize) {

    py::buffer_info prices_buf = prices.request();
    auto *prices_ptr = (T *) prices_buf.ptr;
    const int size = prices_buf.shape[0];
    auto *market_ptr = (T *) market.request().ptr;

    auto sma = sma_calc(prices, period);
    auto sma_market = sma_calc(market, period);
    auto *sma_ptr = (T *) sma.request().ptr;
    auto *sma_market_ptr = (T *) sma_market.request().ptr;

    auto cov = py::array_t<T>(prices_buf.size);
    auto *cov_ptr = (T *) cov.request().ptr;
    init_nan(cov_ptr, size);
    
    int adjust_nan = 0;
    for (int idx = 0; idx < size; ++idx) {
        if (std::isnan(prices_ptr[idx])) {
            ++adjust_nan;
        }

        else {
            break;
        }
    }

    for (int ii = 0 + adjust_nan; ii < size - period+ 1; ii++) {
        T temp = 0;

        for (int idx = ii; idx < period + ii; idx++) {
            temp += ((prices_ptr[idx] - sma_ptr[ii+period-1]) * 
                (market_ptr[idx] - sma_market_ptr[ii+period-1]));
        }

        if (normalize == true) {
            temp /= (period - 1);
        }

        else {
            temp /= (period);
        }
  
        cov_ptr[ii+period-1] = temp;
    }

    return cov;
}

/*
 * Implementation of BETA.
 *
 * Calculates the beta coefficient for a price array.
 * 
 * @param prices (py::array_t<double>): Array with prices.
 * @param market (py::array_t<double>): Array with market prices that beta is calculated from.
 * @param period (int): Number of periods.
 * @param normalize (bool): Specify whether to normalize the variance of the market.
 *
 * Observe that the first array is the array that beta will be calcualted for, and the second
 * is the market that serves as the comparison.
 *
 */
template <typename T>
py::array_t<T> beta_calc(const py::array_t<T> prices, const py::array_t<T> market,
        const int period, const bool var_normalize) {

    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];
    
    auto prices_pct = pct_change_calc(prices, 1);
    auto market_pct = pct_change_calc(market, 1);

    // Calculate the variance for the market.
    auto var = var_calc(market_pct, period, var_normalize);
    auto *var_ptr = (T *) var.request().ptr;

    // Calculate covariance between price and market.
    auto cov = cov_calc(prices_pct, market_pct, period, false);
    auto *cov_ptr = (T *) cov.request().ptr;
    
    auto beta = py::array_t<T>(prices_buf.size);
    auto *beta_ptr = (T *) beta.request().ptr;
    init_nan(beta_ptr, size);

    for (int idx = period; idx < size; ++idx) {
        beta_ptr[idx] = cov_ptr[idx] / var_ptr[idx];
    }

    return beta;
}

/*
 * Implementation of PCT_CHANGE.
 *
 * Calculates the percentage change of a price array.
 */ 
template <typename T>
py::array_t<T> pct_change_calc(const py::array_t<T> prices, const int period) {
    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];
    auto *prices_ptr = (T *) prices_buf.ptr;

    auto pct_change = py::array_t<T>(prices_buf.size);
    auto *pct_change_ptr = (T *) pct_change.request().ptr;
    init_nan(pct_change_ptr, size);

    for (int idx = period; idx < size; ++idx) {
        pct_change_ptr[idx] = ((prices_ptr[idx] - prices_ptr[idx-period]) / 
            prices_ptr[idx-period]) * 100;
    }

    return pct_change;
}

PYBIND11_MODULE(_stat, m) {
    m.def("std_calc", &std_calc<double>, "Standard Deviation");
    m.def("std_calc", &std_calc<float>, "Standard Deviation");

    m.def("var_calc", &var_calc<double>, "Variance");
    m.def("var_calc", &var_calc<float>, "Variance");

    m.def("cov_calc", &cov_calc<double>, "Covariance");
    m.def("cov_calc", &cov_calc<float>, "Covariance");

    m.def("beta_calc", &beta_calc<double>, "Beta");
    m.def("beta_calc", &beta_calc<float>, "Beta");

    m.def("pct_change_calc", &pct_change_calc<double>, "Percentage change");
    m.def("pct_change_calc", &pct_change_calc<float>, "Percentage change");
}
