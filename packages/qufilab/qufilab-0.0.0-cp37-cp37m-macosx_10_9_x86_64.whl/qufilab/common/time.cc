/*
 * @ Quant, Anton Normelius, 2020.
 *
 * Storage of date attributes.
 *
 */

#include <iostream>
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "time.h"

//namespace py = boost::python;

/*
    Function to return vector with tm structs.

    @param d (py::list): List containing dates.
    @return dates (vector<struct tm>): List containing tm structs.
 */
std::vector<struct tm> config_time(std::vector<std::string> temp_dates){
    /*
    *  tm struct consists of:
    *      - tm_sec
    *      - tm_min
    *      - tm_hour
    *      - tm_mday
    *      - tm_mon
    *      - tm_year
    *      - tm_wday
    *      - tm_yday
    */
    //std::vector<std::string> temp_dates = to_vector<std::string> (d);
    std::vector<struct tm> dates;
  
    for (auto date : temp_dates){
        struct tm tm;
        memset(&tm, 0, sizeof(struct tm));
        strptime(date.c_str(), "%Y-%m-%d %H:%M:%S", &tm);
        tm.tm_mon += 1; // Need to increase month by 1.
        tm.tm_year += 1900; // Need to increase year by 1900.
        dates.push_back(tm);
    }

    return dates;
}

/*
    Increment days to a tm struct.

    @param tm (struct tm): Struct containing the tm date.
    @param days (int): Number of days to increment.
    @return (struct tm): Returns a tm struct with increment.

 */
struct tm add_days(struct tm tm, int days) {
    time_t epoch = mktime(&tm);
    epoch += (60 * 60 * 24 * days);
    return *localtime(&epoch);

}






