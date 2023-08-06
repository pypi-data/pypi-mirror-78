
/*
 * Implementation of candlestick methods.
 * This implementation handles all calculations
 * regarding a single candlestick.
 *
 */

#include <cstdint>
#include "candlestick.h"

template <typename T>
Candlestick<T>::Candlestick(T high, T low, T open, T close, T body_avg, T ma) {
    this -> high = high;
    this -> low = low;
    this -> open = open;
    this -> close = close;
    body_high = std::max(close, open);
    body_low = std::min(close, open);
    body_mid = (body_low + body_high) / 2.0;
    this -> ma = ma;

    body = body_high - body_low;
    this -> body_avg = body_avg;
    upper_shadow = high - body_high;
    lower_shadow = body_low - low;
    range = high - low;
}

// Checks if upper shadow exists. It is achieved by comparing the upper
// shadow size with a percentage of the body. 
template <typename T>
bool Candlestick<T>::has_upper_shadow(const float shadow_margin) {
    return upper_shadow > (shadow_margin / 100 * body) ? true : false;
}

// Checks if lower shadow exists. It is achieved by comparing the lower
// shadow size with a percentage of the body.
template <typename T>
bool Candlestick<T>::has_lower_shadow(const float shadow_margin) {
    return lower_shadow > (shadow_margin / 100 * body) ? true : false;
}

// Checks if candlestick has a short body. Short is defined to be
// smaller than an 14 period ema of body sizes.
template <typename T>
bool Candlestick<T>::has_short_body() {
    return body < body_avg ? true : false;
}

// Checks if candlestick has a long body. Long is defined to be
// greater than or equal to a 14 period ema of body sizes.
template <typename T>
bool Candlestick<T>::has_long_body() {
    return body >= body_avg ? true : false;
}

// If close is greater than open, then the candlestick is positive, i.e. green.
template <typename T>
bool Candlestick<T>::is_green() {
    return close > open ? true : false;
}

// If open is greater than close, then the candlestick is negative, i.e. red.
template <typename T>
bool Candlestick<T>::is_red() {
    return open > close ? true : false;
}


// A doji body is here defined to be less than or equal to 
// a percentage of the candlestick range. This will ensure that
// the body is very short.
template <typename T>
bool Candlestick<T>::has_doji_body(const float doji_pct) {
    return body <= (doji_pct / 100 * range) ? true : false;
}

// Shadows are considered equal if the percentage difference between
// their sizes are less than a specified shadow percentage. By default,
// 66.7% are used, indicating that one shadow can be twice as big as the
// other.
template <typename T>
bool Candlestick<T>::has_equal_shadows(const float equal_shadow_pct) {
    T diff = abs(upper_shadow - lower_shadow);
    T average = (upper_shadow + lower_shadow) / 2;

    return (upper_shadow == lower_shadow) ? true :
        diff / average < equal_shadow_pct ? true :
                                            false;
}

// A marubozu candle is defined as a candlestick without any shadows.
// In this implementation, shadow margins can be specified, indicating
// how much shadow one can tolerate and still be considered a marubozu.
template <typename T>
bool Candlestick<T>::is_marubozu(const float shadow_margin) {
    return (!has_lower_shadow(shadow_margin) &&
            !has_upper_shadow(shadow_margin)) ? true : false;
}

// An uptrend is defined as a candlestick close price above 
// moving average of previous body sizes.
template <typename T>
bool Candlestick<T>::has_up_trend() {return close >= ma ? true : false;}



// Explicit instantiations for the types that will be available.
// This is needed to resolve linking issues.
template struct Candlestick<double>;
template struct Candlestick<float>;

