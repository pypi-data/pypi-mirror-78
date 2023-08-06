

#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <limits>
#include <numeric>
#include <omp.h>
#include <x86intrin.h>
#include <cstdint>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include "_volume.h"
#include "_trend.h"
#include "util.h"

namespace py = pybind11;

/*
 * Implementation of ACDI.
 *
 */
template <typename T>
py::array_t<T> acdi_calc(const py::array_t<T> prices,
        const py::array_t<T> highs, const py::array_t<T> lows,
        const py::array_t<T> volumes) {

    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];
    auto acdi = py::array_t<T>(prices_buf.size);

    auto *prices_ptr = (T *) prices_buf.ptr;
    auto *highs_ptr = (T *) highs.request().ptr;
    auto *lows_ptr = (T *) lows.request().ptr;
    auto *volumes_ptr = (T *) volumes.request().ptr;
    auto *acdi_ptr = (T *) acdi.request().ptr;
    init_nan(acdi_ptr, size);
    
    T ad = 0.0;
    for (int idx = 0; idx < size; ++idx) {
        T nominator = highs_ptr[idx] - lows_ptr[idx];
        // Santiy check, highs should never be higher than low.
        if (nominator > 0.0) {
        ad += (((prices_ptr[idx] - lows_ptr[idx]) - 
                    (highs_ptr[idx] - prices_ptr[idx])) / nominator) * 
                    (T)volumes_ptr[idx];
        }
        
        acdi_ptr[idx] = ad;
    }

    return acdi;
}


/*
 * Implementation of OBV.
 *
    @param (py::array_t<double>) prices: Vector with prices.
    @param (py::array_t<double>) volumes: Vector with volumes.
 */

template <typename T>
py::array_t<T> obv_calc(const py::array_t<T> prices, 
        const py::array_t<T> volumes) {

    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];
    auto obv = py::array_t<T>(prices_buf.size);

    auto *prices_ptr = (T *) prices_buf.ptr;
    auto *volumes_ptr = (T *) volumes.request().ptr;
    auto *obv_ptr = (T *) obv.request().ptr;
    init_nan(obv_ptr, size);
    obv_ptr[0] = volumes_ptr[0];

    for (int idx = 1; idx < size; ++idx) {
        if (prices_ptr[idx] > prices_ptr[idx-1]) {
            obv_ptr[idx] = obv_ptr[idx-1] + volumes_ptr[idx];
        }

        else if (prices_ptr[idx] < prices_ptr[idx-1]) {
            obv_ptr[idx] = obv_ptr[idx-1] - volumes_ptr[idx];
        }
        
        else {
            obv_ptr[idx] = obv_ptr[idx-1];
        }
    }

    return obv;
}


/*
 * Implementation of CMF.
 *
    @param (vector<float>) prices: Vector with closing prices.
    @param (vector<highs>) highs: Vector with high prices.
    @param (vector<lows>) lows: Vector with low prices.
    @param (vector<volumes>) volumes: Vector with volumes.
    @param (int) periods: Number of periods. Standard 21.
 */
template <typename T>
py::array_t<T> cmf_calc(const py::array_t<T> prices,
        const py::array_t<T> highs, const py::array_t<T> lows,
        const py::array_t<T> volumes, const int periods) {

    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];

    auto *prices_ptr = (T *) prices_buf.ptr;
    auto *highs_ptr = (T *) highs.request().ptr;
    auto *lows_ptr = (T *) lows.request().ptr;
    auto *volumes_ptr = (T *) volumes.request().ptr;

    auto cmf = py::array_t<T>(prices_buf.size);
    auto ac = py::array_t<T>(prices_buf.size);
    auto *cmf_ptr = (T *) cmf.request().ptr;
    auto *ac_ptr = (T *) ac.request().ptr;

    init_nan(cmf_ptr, size);
    init_nan(ac_ptr, size);
    
    // Money Flow Multiplier.
    for (int idx = 0; idx < size; ++idx) {
        ac_ptr[idx] = (((prices_ptr[idx] - lows_ptr[idx]) - (highs_ptr[idx] - prices_ptr[idx])) / 
            (highs_ptr[idx] - lows_ptr[idx])) * volumes_ptr[idx];
    }

    for (int idx = periods; idx < size + 1; ++idx) {
        T sum = std::accumulate(ac_ptr + idx - periods, ac_ptr + idx, 0.0);
        T vol = std::accumulate(volumes_ptr + idx - periods, volumes_ptr + idx, 0.0);
        cmf_ptr[idx-1] = sum / vol;
    }
   
    return cmf;
}


/*
 * Implementation of CI.
 *
    @param (py::array_t<double>) prices: Vector with closing prices.
    @param (py::array_t<double>) highs: Vector with high prices.
    @param (py::array_t<double>) lows: Vector with low prices.
    @param (py::array_t<double>) volumes: Vector with volumes.
 */
template <typename T>
py::array_t<T> ci_calc(const py::array_t<T> prices,
        const py::array_t<T> highs, const py::array_t<T> lows,
        const py::array_t<T> volumes) {

    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];
    auto *prices_ptr = (T *) prices_buf.ptr;

    auto ci = py::array_t<T>(prices_buf.size);
    auto *ci_ptr = (T *) ci.request().ptr;
    init_nan(ci_ptr, size);

    py::array_t<T> acdi = acdi_calc(prices, highs, lows, volumes);
    auto *acdi_ptr = (T *) acdi.request().ptr;

    py::array_t<T> ema10 = ema_calc(acdi, 10);
    auto *ema10_ptr = (T *) ema10.request().ptr;

    py::array_t<T> ema3 = ema_calc(acdi, 3);
    auto *ema3_ptr = (T *) ema3.request().ptr;

    for (int idx = 9; idx < size; idx++) {
        ci_ptr[idx] = ema3_ptr[idx] - ema10_ptr[idx];
    }
    
    return ci;
}

/*
 * Implementation of PVI.
 *
 *  Math: If volume_today > volume_yesterday:
 *              PVI = PVI_yesterday + ((Close - Close_yesterday) / Close_yesterday) * PVI_yesterday
 *      
 *  @param (vector<float>) prices: Vector with closing prices.
 *  @param (vector<volumes>) volumes: Vector with volumes.
 *
 */
template <typename T>
py::array_t<T> pvi_calc(const py::array_t<T> prices,
        const py::array_t<T> volumes) {

    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];
    auto pvi = py::array_t<T>(prices_buf.size);

    auto *prices_ptr = (T *) prices_buf.ptr;
    auto *volumes_ptr = (T *) volumes.request().ptr;
    auto *pvi_ptr = (T *) pvi.request().ptr;

    init_nan(pvi_ptr, size);
    pvi_ptr[0] = 100.0;

    for (int idx = 1; idx < size; ++idx) {
        if (volumes_ptr[idx] > volumes_ptr[idx-1]) {
            pvi_ptr[idx] = pvi_ptr[idx-1] + ((prices_ptr[idx] - prices_ptr[idx-1]) 
                    / prices_ptr[idx-1]) * pvi_ptr[idx-1];
        }

        else {
            pvi_ptr[idx] = pvi_ptr[idx-1];
        }
    }
    
    return pvi;
}

/*
 *  Implementation of NVI.
 *
 *  Negative Volume Index
 *
 *  Math: If volume_today > volume_yesterday:
 *              NVI = NVI_yesterday + ((Close - Close_yesterday) / Close_yesterday) * NVI_yesterday
 *      
 *  @param (vector<float>) prices: Vector with closing prices.
 *  @param (vector<volumes>) volumes: Vector with volumes.
 *
 */
template <typename T>
py::array_t<T> nvi_calc(const py::array_t<T> prices,
        const py::array_t<T> volumes) {

    py::buffer_info prices_buf = prices.request();
    const int size = prices_buf.shape[0];
    auto nvi = py::array_t<T>(prices_buf.size);

    auto *prices_ptr = (T *) prices_buf.ptr;
    auto *volumes_ptr = (T *) volumes.request().ptr;
    auto *nvi_ptr = (T *) nvi.request().ptr;

    init_nan(nvi_ptr, size);
    nvi_ptr[0] = 100.0;

    for (int idx = 1; idx < size; ++idx) {
        if (volumes_ptr[idx] < volumes_ptr[idx-1]) {
            nvi_ptr[idx] = nvi_ptr[idx-1] + ((prices_ptr[idx] - prices_ptr[idx-1]) 
                    / prices_ptr[idx-1]) * nvi_ptr[idx-1];
        }

        else {
            nvi_ptr[idx] = nvi_ptr[idx-1];
        }
    }
    
    return nvi;
}


PYBIND11_MODULE(_volume, m) {
    m.def("acdi_calc", &acdi_calc<double>, "Accumulation Distribution");
    m.def("acdi_calc", &acdi_calc<float>, "Accumulation Distribution");

    m.def("obv_calc", &obv_calc<double>, "On Balance Volume");
    m.def("obv_calc", &obv_calc<float>, "On Balance Volume");

    m.def("cmf_calc", &cmf_calc<double>, "Chaikin Money Flow");
    m.def("cmf_calc", &cmf_calc<float>, "Chaikin Money Flow");

    m.def("ci_calc", &ci_calc<double>, "Chaikin Indicator");
    m.def("ci_calc", &ci_calc<float>, "Chaikin Indicator");

    m.def("pvi_calc", &pvi_calc<double>, "Positive Volume Index");
    m.def("pvi_calc", &pvi_calc<float>, "Positive Volume Index");

    m.def("nvi_calc", &nvi_calc<double>, "Negative Volume Index");
    m.def("nvi_calc", &nvi_calc<float>, "Negative Volume Index");
}


