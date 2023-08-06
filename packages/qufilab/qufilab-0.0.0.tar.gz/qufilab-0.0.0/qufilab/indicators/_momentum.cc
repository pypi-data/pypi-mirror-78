/*
* @ Quant, Anton Normelius, 2020.
*
* Module to handle momentum indicator calculations.
*
*/

#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <cstdlib>
#include <limits>
#include <numeric>
#include <cstdint>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include "_momentum.h"
#include "_trend.h"
#include "util.h"   // Init nans.

namespace py = pybind11;

/*
*   Implementation of RSI.
*
*   @param prices (vector<double>): Vector with prices.
*   @param periods (int): Number of periods.
*   @param rsi_type (std::string): Specifies how the following gains/losses 
*       shall be calculated. 'standard' or 'smoothed'.
*/
template <typename T>
py::array_t<T> rsi_calc(const py::array_t<T> prices,
        const int periods, const std::string rsi_type) {

    py::buffer_info prices_buf = prices.request();
    auto *prices_ptr = (T *) prices_buf.ptr;
    const int size = prices_buf.shape[0];
    
    auto rsi = py::array_t<T>(prices_buf.size);
    auto *rsi_ptr = (T *) rsi.request().ptr;

    auto gains = py::array_t<T>(prices_buf.size);
    auto *gains_ptr = (T *) gains.request().ptr;

    auto losses = py::array_t<T>(prices_buf.size);
    auto *losses_ptr = (T*) losses.request().ptr;

    init_nan(rsi_ptr, size);
    init_zeros(gains_ptr, size);
    init_zeros(losses_ptr, size);
    
    // Calculate average gains and losses vector, size -1 compared to prices.
    for (int idx = 1; idx < size; ++idx) {
        T diff = prices_ptr[idx] - prices_ptr[idx-1];
        if (diff > 0) {
            gains_ptr[idx] = diff;
        }

        else if (diff < 0) {
            losses_ptr[idx] = diff * -1.0;
        }
    }
    
    // First average gain/loss.
    T AG = 0.0;
    T AL = 0.0;

    for (int idx = 1; idx <= periods; ++idx) {
        AG += gains_ptr[idx];
        AL += losses_ptr[idx];
    }

    AG /= periods;
    AL /= periods;
    rsi_ptr[periods] = 100 - (100 / (1 + (AG / AL)));
    
    for (int idx = periods+1; idx < size; ++idx) {
        if (rsi_type == "smoothed") {
            AG = ((AG * (periods-1)) + gains_ptr[idx]) / periods;
            AL = ((AL * (periods-1)) + losses_ptr[idx]) / periods;
        }
        
        else if (rsi_type == "standard") { 
            for (int idx1 = idx - periods + 1; idx1 <= idx; ++idx1) {
                AG += gains_ptr[idx];
                AL += losses_ptr[idx];
            }
            AG /= periods;
            AL /= periods;
        }

        rsi_ptr[idx] = 100 - (100 / (1 + (AG / AL)));
    }

    return rsi;
}

/*
 *  Implementation of MACD.
 *
*   @param prices (vector<double>): Vector with prices.
*   @param default_size (bool): Specify whether returned vector should be same length
*       filled with NaNs.
*/

template <typename T>
std::tuple<py::array_t<T>, py::array_t<T>> macd_calc(const py::array_t<T> prices) {
    
    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];
    auto *prices_ptr = (T *) prices_buf.ptr;
    
    auto macd = py::array_t<T>(prices_buf.size);
    auto signal = py::array_t<T>(prices_buf.size);

    auto *macd_ptr = (T *) macd.request().ptr;
    auto *signal_ptr = (T *) signal.request().ptr;

    init_nan(macd_ptr, size);
    init_nan(signal_ptr, size);

    py::array_t<T> ema26 = ema_calc(prices, 26);
    py::array_t<T> ema12 = ema_calc(prices, 12);
    auto *ema26_ptr = (T *) ema26.request().ptr;
    auto *ema12_ptr = (T *) ema12.request().ptr;
    
    for (int idx = 25; idx < size; ++idx) {
        macd_ptr[idx] = ema12_ptr[idx] - ema26_ptr[idx];
    }
    
    T k = (T) 2 / (10);
    // SMA for the first signal value.
    T prev = std::accumulate(macd_ptr + 25, macd_ptr + 34, 0.0) / 9;
    signal_ptr[33] = prev;
    
    // EMA for the rest.
    for (int idx = 34; idx < size; ++idx) {
        prev = (macd_ptr[idx] - prev) * k + prev;
        signal_ptr[idx] = prev;
    }

    return std::make_tuple(macd, signal);
}

/*
*   Implementation of WILLR.
*
*   @param prices (vector<double>): Vector with closing prices.
*   @param highs (vector<double>): Vector with high prices.
*   @param lows (vector<double>): Vector with low prices.
*   @param periods (int): Number of periods.
 */
template <typename T>
py::array_t<T> willr_calc(const py::array_t<T> prices,
        const py::array_t<T> highs, const py::array_t<T> lows,
        const int periods) {

    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];

    auto *prices_ptr = (T *) prices_buf.ptr;
    auto *highs_ptr = (T *) highs.request().ptr;
    auto *lows_ptr = (T *) lows.request().ptr;
    
    auto william = py::array_t<T>(prices_buf.size);
    auto *will_ptr = (T *) william.request().ptr;

    init_nan(will_ptr, size);

    for (size_t idx = periods-1; idx < size; ++idx) {
        T max = *std::max_element(highs_ptr + idx - periods + 1, highs_ptr + idx + 1);
        T min = *std::min_element(lows_ptr + idx - periods + 1, lows_ptr + idx + 1);
        will_ptr[idx] = ((max - prices_ptr[idx]) / (max - min)) * -100.0;
    }

    return william;
}

/*
*   Stochastic Indicator
*   @param prices (vector<double>): Vector with closing prices.
*   @param highs (vector<double>): Vector with high prices.
*   @param lows (vector<double>): Vector with low prices.
*   @param period (int): Number of periods.
*   @param smooth_period (int): Number of periods to smooth the %K line.
 */

/*
std::tuple<std::vector<double>, std::vector<double>> stochastic_calc(const std::vector<double> prices,
        const std::vector<double> highs, const std::vector<double> lows,
        std::string mode, const int period, std::string method) {

    std::vector<double> stoch_k(prices.size(), std::numeric_limits<double>::quiet_NaN());
    double max = *std::max_element(highs.begin(), highs.begin() + period);
    double min = *std::min_element(lows.begin(), lows.begin() + period);

    // %K
    for (int idx = 0; idx < prices.size(); ++idx) {
        if (idx >= period) {
            max = *std::max_element(highs.begin()+idx-period+1, highs.begin()+idx+1);
            min = *std::min_element(lows.begin()+idx-period+1, lows.begin()+idx+1);
        }
        stoch_k[idx] = ((prices[idx] - min) / (max - min)) * 100.0;
    }

    if (mode == "slow") {
        const int internal_smoothing = 3; // In case slow stochastic
        stoch_k = ema_calc(stoch_k, internal_smoothing, false);
    }

    const int smooth_period = 3; // Smooth to get %D.
    std::vector<double> stoch_d;
    if (method == "sma") {
        stoch_d = sma_calc(stoch_k, smooth_period);
    }
    
    else if (method == "ema"){
        stoch_d = ema_calc(stoch_k, smooth_period);
    }

    // If slow stochastic, insert NaNs at the beginning to get correct size.
    const int increment = prices.size() - stoch_k.size();
    for (int idx = 0; idx < increment; ++idx) {
        stoch_k.insert(stoch_k.begin(), std::numeric_limits<double>::quiet_NaN());
        stoch_d.insert(stoch_d.begin(), std::numeric_limits<double>::quiet_NaN());
    }

    return std::make_tuple(stoch_k, stoch_d);
}
*/


/*
*   Implementation of ROC.
*
*   Math: (price_now - price_periods) / (price_periods) * 100;
*   @param prices (vector<double>): Vector with closing prices.
*   @param periods (int): Number of periods.
*/
template <typename T>
py::array_t<T> roc_calc(const py::array_t<T> prices, const int periods) {
    py::buffer_info prices_buf = prices.request();
    auto *prices_ptr = (T *) prices_buf.ptr;
    const int size = prices_buf.shape[0];
    
    auto roc = py::array_t<T>(prices_buf.size);
    auto *roc_ptr = (T *) roc.request().ptr;
    init_nan(roc_ptr, size);
    
    for (int idx = periods; idx < size; ++idx) {
        roc_ptr[idx] = ((prices_ptr[idx] - prices_ptr[idx-periods]) 
                / prices_ptr[idx-periods]) * 100.0;
    }

    return roc;

}
   
/*
*   Implementation of VPT.
*
*   Math: (((close - close_yesterday) / (close_yesterday)) * volume) + pvt_yesterday
*   @param prices (vector<double>): Vector with closing prices.
*   @param volumes (vector<double>): Vector with volume prices.
 */
template <typename T>
py::array_t<T> vpt_calc(const py::array_t<T> prices, 
        const py::array_t<T> volumes) {

    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];

    auto vpt = py::array_t<T>(prices_buf.size);

    auto *prices_ptr = (T *) prices_buf.ptr;
    auto *volumes_ptr = (T *) volumes.request().ptr;
    auto *vpt_ptr = (T *) vpt.request().ptr;

    init_nan(vpt_ptr, size);
    // Need a first value for the vpt.
    vpt_ptr[0] = volumes_ptr[0];

    for (size_t idx = 1; idx < size; ++idx) {
        vpt_ptr[idx] = (((prices_ptr[idx] - prices_ptr[idx-1]) / 
                    prices_ptr[idx-1]) * volumes_ptr[idx]) + vpt_ptr[idx-1];
    }

    return vpt;
}

/*
*   Implementation of MI.
*
*   Math: close - close_periods
*   @param prices (vector<double>): Vector with closing prices.
*   @param periods (int): Number of periods.
*/
template <typename T>
py::array_t<T> mi_calc(const py::array_t<T> prices, 
        const int periods) {

    py::buffer_info prices_buf = prices.request();
    auto *prices_ptr = (T *) prices_buf.ptr;
    const int size = prices_buf.shape[0];
    
    auto momentum = py::array_t<T>(prices_buf.size);
    auto *momentum_ptr = (T *) momentum.request().ptr;
    init_nan(momentum_ptr, size);

    for (int idx = periods; idx < prices.size(); ++idx) {
        momentum_ptr[idx] = prices_ptr[idx] - prices_ptr[idx-periods];
    }

    return momentum;
}


/*
 *   Implementation of CCI.
 *
 *   Math: CCI = (TP - TP_sma) / (0.015 - MD).
 *      TP = Typical price = (high + low + close) / 3;
 *      MD = Mean deviation, calcualted with:
 *          sum of the absolute values between recent tp_sma and all 
 *          tp for the lookback period.
 *          Finally, MD = sum / period.
 *
 *   @param close (vector<double>): Vector with closing prices.
 *   @param high (vector<double>): Vector with high prices.
 *   @param low (vector<double>): Vector with low prices.
 *   @param period (int): Number of periods.
 *   @return: Vector with cci-values.
 */
template <typename T>
py::array_t<T> cci_calc(const py::array_t<T> close,
        const py::array_t<T> high, const py::array_t<T> low,
        const int period) {

    py::buffer_info close_buf = close.request();
    T *close_ptr = (T *) close_buf.ptr;
    const int size = close_buf.shape[0];

    auto cci = py::array_t<T>(close_buf.size);
    auto *cci_ptr = (T *) cci.request().ptr;
    auto *high_ptr = (T *) high.request().ptr;
    auto *low_ptr = (T *) low.request().ptr;
    init_nan(cci_ptr, size);

    auto tp = py::array_t<T>(close_buf.size);
    auto *tp_ptr = (T *) tp.request().ptr;

    for (int idx = 0; idx < size; ++idx) {
        tp_ptr[idx] = (close_ptr[idx] + high_ptr[idx] + low_ptr[idx]) / 3.0;
    }

    py::array_t<T> tpsma = sma_calc(tp, period);
    auto *tpsma_ptr = (T *) tpsma.request().ptr;

    const T constant = 0.015;

    for (int idx = period-1; idx < size; ++idx) {
        // Mean deviation
        T mean_dev = 0.0;
        for (int idx1 = idx-period+1; idx1 <= idx; ++idx1) {
            mean_dev += abs(tpsma_ptr[idx] - tp_ptr[idx1]);
        }

        mean_dev /= period;
        cci_ptr[idx] = (tp_ptr[idx] - tpsma_ptr[idx]) / (constant * mean_dev);
    }

    return cci;
}


/*
 *   Implementation of AROON.
 *
 *   @param high (vector<double>): Vector with high prices.
 *   @param low (vector<double>): Vector with low prices.
 *   @param period (int): Number of periods.
 *   @return: Tuple with aroon-os, aroon-up, aroon-down.
 */
template <typename T>
py::array_t<T> aroon_calc(const py::array_t<T> high, 
        const py::array_t<T> low, const int period) {

    py::buffer_info high_buf = high.request();
    auto *high_ptr = (T *) high.request().ptr;
    auto *low_ptr = (T *) low.request().ptr;
    
    const int size = high_buf.shape[0];

    auto aroon = py::array_t<T>(high_buf.size);
    auto *aroon_ptr = (T *) aroon.request().ptr;

    init_nan(aroon_ptr, size);
    
    for (int idx = period; idx < size; ++idx) {
        int max = std::distance(high_ptr, 
                std::max_element(high_ptr + idx - period, high_ptr + idx + 1));
        int min = std::distance(low_ptr, 
                std::min_element(low_ptr + idx - period, low_ptr + idx + 1));

        int days_up = idx - max;
        int days_down = idx - min;

        T aroon_up = ((T)(period - days_up) / period) * 100;
        T aroon_down = ((T)(period - days_down) / period) * 100;
        aroon_ptr[idx] = aroon_up - aroon_down;
    }
    
    return aroon;
}

/*
 *   Implementation of APO.
 *
 *   Math: MA(period_fast) - MA(period_slow), where:
 *   MA can be specified as:
 *      SMA
 *      EMA
 *
 *   @param price(py::array_t<double>): Array with prices.
 *   @param period_slow (int): Slow period.
 *   @param period_fast (int): Fast period.
 *   @param ma (string): Type of moving average to be specified.
 *
 */
template <typename T>
py::array_t<T> apo_calc(const py::array_t<T> prices, const int period_slow,
        const int period_fast, const std::string ma) {

    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];

    py::array_t<T> ma_fast;
    py::array_t<T> ma_slow; 
    
    if (ma == "sma") {
        ma_fast = sma_calc(prices, period_fast);
        ma_slow = sma_calc(prices, period_slow);
    }
    
    else if (ma == "ema") {
        ma_fast = ema_calc(prices, period_fast);
        ma_slow = ema_calc(prices, period_slow);
    }

    auto *ma_fast_ptr = (T *) ma_fast.request().ptr;
    auto *ma_slow_ptr = (T *) ma_slow.request().ptr;

    auto apo = py::array_t<T>(prices_buf.size);
    auto *apo_ptr = (T *) apo.request().ptr;
    init_nan(apo_ptr, size);

    for (int idx = period_slow-1; idx < size; ++idx) {
        apo_ptr[idx] = ma_fast_ptr[idx] - ma_slow_ptr[idx];
    }
    
    return apo;
}

/*
 *   Implementation of BPO.
 *
 *   Math: (close - open) / (high - low);
 *
 *   @param close (py::array_t<double>): Array with close prices.
 *   @param open (py::array_t<double>): Array with opening prices.
 *   @param high (py::array_t<double>): Array with high prices.
 *   @param low (py::array_t<double>): Array with low prices.
 *
 */
template <typename T>
py::array_t<T> bop_calc(const py::array_t<T> high, const py::array_t<T> low,
        const py::array_t<T> open, const py::array_t<T> close) {
    
    py::buffer_info close_buf = close.request();
    const int size = close_buf.shape[0];

    auto *high_ptr = (T *) high.request().ptr;
    auto *low_ptr = (T *) low.request().ptr;
    auto *open_ptr = (T *) open.request().ptr;
    auto *close_ptr = (T *) close_buf.ptr;
    
    auto bop = py::array_t<T>(close_buf.size);
    auto *bop_ptr = (T *) bop.request().ptr;
    init_zeros(bop_ptr, size);

    for (int idx = 0; idx < size; ++idx) {
        T numerator = high_ptr[idx] - low_ptr[idx];
        if (numerator > 0) {
            bop_ptr[idx] = (close_ptr[idx] - open_ptr[idx]) / numerator;
        }
    }
    
    return bop;
}


/*
 *   Implementation of CMO.
 *
 *   Math: ((sum_up - sum_down) / (sum_up + sum_down)) * 100, where:
 *      sum_up is the sum of the difference between current close and 
 *      previous close on up days during the period.
 *      sum_down is the sum of the difference between current close and
 *      previous close on down days during the period.
 *
 *   @param close (py::array_t<double>): Array with close prices.
 *   @param period (int): Number of periods.
 */
template <typename T>
py::array_t<T> cmo_calc(const py::array_t<T> close, const int period) {
    py::buffer_info close_buf = close.request();
    const int size = close_buf.shape[0];
    auto *close_ptr = (T *) close_buf.ptr;
    
    auto cmo = py::array_t<T>(close_buf.size);
    auto *cmo_ptr = (T *) cmo.request().ptr;
    init_nan(cmo_ptr, size);

    auto diff_up = py::array_t<T>(close_buf.size);
    auto diff_down = py::array_t<T>(close_buf.size);
    auto *diff_up_ptr = (T *) diff_up.request().ptr;
    auto *diff_down_ptr = (T *) diff_down.request().ptr;

    init_zeros(diff_up_ptr, size);
    init_zeros(diff_down_ptr, size);
    
    T cmo_down = 0.0;
    T cmo_up = 0.0;

    for (int idx = 1; idx < size; ++idx) {
        // Create the diff arrays.
        T diff = close_ptr[idx] - close_ptr[idx-1];
        if (diff > 0.0) {
            diff_up_ptr[idx] = diff;
        }

        else if (diff < 0.0) {
            diff_down_ptr[idx] = diff * -1.0;
        }
        
        // Increment cmo_up/cmo_down witht he differences. In case the stock rose one day,
        // the down diff will be zero, so both variables can be incremented at the same time.
        cmo_up += diff_up_ptr[idx];
        cmo_down += diff_down_ptr[idx];

        // Remove first value in each new period.
        if (idx > period) {
            cmo_down -= diff_down_ptr[idx-period];
            cmo_up -= diff_up_ptr[idx-period];
        }
        
        if (idx >= period) {
            cmo_ptr[idx] = ((cmo_up - cmo_down) / (cmo_up + cmo_down)) * 100;
        }
    }

    return cmo;
}

/*
 *   Implementation of MFI.
 *  
 *   Math: Typical price: (high + low + close) / 3.
 *      Raw money flow: Typical price * volume.
 *      Money flow ratio = x_period positive raw money flow / x_period negative raw money flow.
 *      positive/negative flow is calculated as the sum of the typical prices when today's
 *      typical price is higher/lower that the previous.
 *      Money flow index = 100 - (100 / (1 - money flow ratio)).
 *
 *   @param high (py::array_t<double>): Array with high prices.
 *   @param low (py::array_t<double>): Array with low prices.
 *   @param close (py::array_t<double>): Array with close prices.
 *   @param volume (py::array_t<double>): Array with volume prices.
 *   @param period (int): Number of periods.
 */
template <typename T>
py::array_t<T> mfi_calc(const py::array_t<T> high,
      const py::array_t<T> low, const py::array_t<T> close,
      const py::array_t<T> volume, const int period) {
    
    py::buffer_info close_buf = close.request();
    const int size = close_buf.shape[0];
    auto *close_ptr = (T *) close_buf.ptr;

    auto *high_ptr = (T *) high.request().ptr;
    auto *low_ptr = (T *) low.request().ptr;
    auto *volume_ptr = (T *) volume.request().ptr;

    auto mfi = py::array_t<T>(close_buf.size);
    auto *mfi_ptr = (T *) mfi.request().ptr;
    init_nan(mfi_ptr, size);

    auto raw_down = py::array_t<T>(close_buf.size);
    auto raw_up = py::array_t<T>(close_buf.size);
    auto *raw_down_ptr = (T *) raw_down.request().ptr;
    auto *raw_up_ptr = (T *) raw_up.request().ptr;
    init_zeros(raw_down_ptr, size);
    init_zeros(raw_up_ptr, size);
    
    T raw_up_sum = 0.0;
    T raw_down_sum = 0.0;
    for (int idx = 1; idx < size; ++idx) {
        T tp = (T)(high_ptr[idx] + low_ptr[idx] + close_ptr[idx]) / 3;
        T tp_prior = (T)(high_ptr[idx-1] + low_ptr[idx-1] + close_ptr[idx-1]) / 3;
        
        // Increase the raw money flow. Save raw up/down since we need to remove these values
        // later on, when a new period stats.
        if (tp > tp_prior) {
            raw_up_ptr[idx] = tp * volume_ptr[idx];
            raw_up_sum += raw_up_ptr[idx];
        }

        else if (tp < tp_prior) {
            raw_down_ptr[idx] = tp * volume_ptr[idx];
            raw_down_sum += raw_down_ptr[idx];
        }
        
        // When a new period starts, remove first raw values since it doesn't belong
        // to this periods calculation.
        if (idx > period) {
            raw_up_sum -= raw_up_ptr[idx-period];
            raw_down_sum -= raw_down_ptr[idx-period];
        }

        // Calculate the MFI
        if (idx >= period) {
            T mfr = raw_up_sum / raw_down_sum;
            if (raw_down_sum != 0) {
                mfi_ptr[idx] = 100 - ((T)100 / (1 + mfr));
            }
        }

    }
    
    return mfi;
}

/*
*   Implementation of PPO.
*
*   @param prices (vector<double>): Vector with prices.
*   @param default_size (bool): Specify whether returned vector should be same length
*       filled with NaNs.
*/
template <typename T>
py::array_t<T> ppo_calc(const py::array_t<T> prices, const int period_fast,
        const int period_slow, const std::string ma_type) {
    
    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];
    auto *prices_ptr = (T *) prices_buf.ptr;
    
    auto ppo = py::array_t<T>(prices_buf.size);
    auto *ppo_ptr = (T *) ppo.request().ptr;

    init_nan(ppo_ptr, size);

    py::array_t<T> ma_fast;
    py::array_t<T> ma_slow;
    
    // Check which moving average.
    if (ma_type == "ema") {
        ma_fast = ema_calc(prices, period_fast);
        ma_slow = ema_calc(prices, period_slow);
    }

    else if (ma_type == "sma") {
        ma_fast = sma_calc(prices, period_fast);
        ma_slow = sma_calc(prices, period_slow);
    }

    auto *ma_slow_ptr = (T *) ma_slow.request().ptr;
    auto *ma_fast_ptr = (T *) ma_fast.request().ptr;
    
    for (int idx = 25; idx < size; ++idx) {
        ppo_ptr[idx] = ((ma_fast_ptr[idx] - ma_slow_ptr[idx]) / ma_slow_ptr[idx]) * 100;
    }

    return ppo;
}


/*
 *   True Strength Indixator (TSI)
 *
 *   @param close (vector<double>): Vector with closing prices.
 *   @param period (int): Number of periods for the first ema calculation.
 *   @param period_double (int): Number of periods for the second ema calculation
 *      to get double smoothing.
 *   @return: Vector with tsi values.
 *
 *   Observe that this implementation sets first momentum values to zero, one could
 *   skip these entirely and not include the zeros in the ema calculations, but this
 *   is how this implementation is made.
 */
/*
std::vector<double> tsi_calc(const std::vector<double> close,
        const int period, const int period_double) {
    std::vector<double> tsi(close.size(), std::numeric_limits<double>::quiet_NaN());
    std::vector<double> mom(close.size(), std::numeric_limits<double>::quiet_NaN());
    std::vector<double> mom_abs(close.size(), std::numeric_limits<double>::quiet_NaN());
    mom[0] = 0.0;
    mom_abs[0] = 0.0;
    for (int idx = 1; idx < close.size(); ++idx) {
        mom[idx] = close[idx] - close[idx-1];
        mom_abs[idx] = abs(close[idx] - close[idx-1]);
    }
    
    std::vector<double> ema_first = ema_calc(mom, period, false);
    std::vector<double> ema_second = ema_calc(ema_first, period_double, false);
    std::vector<double> ema_abs_first = ema_calc(mom_abs, period, false);
    std::vector<double> ema_abs_second = ema_calc(ema_abs_first, period_double, false);

    for (int idx = 0; idx < ema_second.size(); ++idx) {
        tsi[idx+period+period_double-2] = 100.0 * (ema_second[idx] / ema_abs_second[idx]);
    }

    return tsi;
}
*/

PYBIND11_MODULE(_momentum, m) {
    m.def("rsi_calc", &rsi_calc<double>, "RSI");
    m.def("rsi_calc", &rsi_calc<float>, "RSI");

    m.def("macd_calc", &macd_calc<double>, "MACD");
    m.def("macd_calc", &macd_calc<float>, "MACD");

    m.def("willr_calc", &willr_calc<double>, "William's R");
    m.def("willr_calc", &willr_calc<float>, "William's R");

    m.def("roc_calc", &roc_calc<double>, "Price Rate-of-Change");
    m.def("roc_calc", &roc_calc<float>, "Price Rate-of-Change");

    m.def("vpt_calc", &vpt_calc<double>, "Volume and Price Trend");
    m.def("vpt_calc", &vpt_calc<float>, "Volume and Price Trend");

    m.def("mi_calc", &mi_calc<double>, "Momentum Indicator");
    m.def("mi_calc", &mi_calc<float>, "Momentum Indicator");

    m.def("cci_calc", &cci_calc<double>, "Commodity Channel Index");
    m.def("cci_calc", &cci_calc<float>, "Commodity Channel Index");

    m.def("aroon_calc", &aroon_calc<double>, "Aroon Indicator");
    m.def("aroon_calc", &aroon_calc<float>, "Aroon Indicator");

    m.def("apo_calc", &apo_calc<double>, "Absolute Price Oscillator");
    m.def("apo_calc", &apo_calc<float>, "Absolute Price Oscillator");

    m.def("bop_calc", &bop_calc<double>, "Balance of Power");
    m.def("bop_calc", &bop_calc<float>, "Balance of Power");

    m.def("cmo_calc", &cmo_calc<double>, "Chande Momentum Indicator");
    m.def("cmo_calc", &cmo_calc<float>, "Chande Momentum Indicator");

    m.def("mfi_calc", &mfi_calc<double>, "Money Flow Index");
    m.def("mfi_calc", &mfi_calc<float>, "Money Flow Index");

    m.def("ppo_calc", &ppo_calc<double>, "Percentage Price Oscillator");
    m.def("ppo_calc", &ppo_calc<float>, "Percentage Price Oscillator");

    //m.def("stochastic_calc", &stochastic_calc, "Stochastic Indicator");
    //m.def("tsi_calc", &tsi_calc, "True Strength Index");
}
