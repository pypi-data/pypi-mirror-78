/*
 * @ Quant, Anton Normelius, 2020.
 *
 * Models calculations.
 *
 * */

#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <sstream>
#include <iomanip>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include "common/time.h"
#include "indicators/_trend.h"
#include "indicators/_volatility.h"


/*
    Position struct to handle every position that is taken in the models.
 */
struct Position {
        float entry_price = 0.0;
        float open_pct = 0.0; // Corresponding actual open percentage drop.
        float exit_price = 0.0;
        float stop_loss = 0.0;
        int index;
        int exit_index;
        bool covered = false;
        std::string type;
        std::string profit_type;
        struct tm entry_date;
        struct tm exit_date;

        float get_profit() const {
            if (type == "long")
                return exit_price - entry_price;

            else 
                return entry_price - exit_price;
        }
        
        std::string get_entry_date(){
            return get_date(entry_date);
        }

        std::string get_exit_date(){
            return get_date(exit_date);
        }

        std::string get_profit_type() const {
            if (get_profit() > 0.0)
                return "Profit";

            else
                return "Loss";
        }

    private:
        std::string get_date(struct tm date){
            std::string year = std::to_string(date.tm_year);
            std::string month = std::to_string(date.tm_mon);
            std::string day = std::to_string(date.tm_mday);
            std::string hour = std::to_string(date.tm_hour);
            std::string min = std::to_string(date.tm_min);
            std::string sec = std::to_string(date.tm_sec);

            if (month.length() == 1)
                month = "0" + month;
            
            if (day.length() == 1)
                day = "0" + day;

            if (hour == "0" && min == "0" && sec == "0") {
                return year + "-" + month + "-" + day;
            }
            
            else {
                return year + "-" + month + "-" + day + " " 
                    + hour + ":" + min + ":" + sec;
            }
        }
};

/*
    Function to handle model performance summary display.
    Observe that this function is for internal use only.

    @param model (string): Specifying the model name, i.e. openChange.
    @param positions (vector<Position>): Vector containg Position objects.
    @param show_positions (bool): Specify whether or not to show positions.
 */
void summary(std::string model, std::vector<Position> positions,
        bool show_positions){

    int num_positions = positions.size();
    int win_trades = 0;
    int loss_trades = 0;
    const int precision = 12;
    
    if (show_positions == true) {
        std::cout << std::left << std::setw(precision) << "Trade" <<
            std::left << std::setw(precision) << "Entry" << 
            std::left << std::setw(precision) << "Price" << 
            std::left << std::setw(precision) << "Exit" << 
            std::left << std::setw(precision) << "Price" << 
            std::left << std::setw(precision) << "Open change" << std::endl;
        std::string out = std::string(6 * precision, '-');
        std::cout << out << std::endl;
    }

    for (auto p : positions) {
        if (p.covered == true){
            if (p.get_profit() > 0.0)
                win_trades++;

            else if (p.get_profit() < 0.0)
                loss_trades++;

            // Extensive summary/all trades.
            if (show_positions == true) {
                std::cout << std::left << std::setw(precision) << p.get_profit_type() 
                    << std::left << std::setw(precision) << p.get_entry_date() 
                    << std::left << std::setw(precision) << p.entry_price
                    << std::left << std::setw(precision) << p.get_exit_date()
                    << std::left << std::setw(precision) << p.exit_price
                    << std::fixed << std::setprecision(2) << p.open_pct * 100 
                    << "%" << std::endl;
            }
        }
    }

    const int ms_prec = 12;
    float win_pct = 0.0;
    if ((win_trades + loss_trades) != 0) {
        win_pct = (float) win_trades / (win_trades + loss_trades) * 100;

        std::cout << std::endl;
        std::cout << std::left << std::setw(ms_prec) << "Model" <<
            std::left << std::setw(ms_prec)<< "Type [-]" << 
            std::left << std::setw(ms_prec) << "Trades [#]" << 
            std::left << std::setw(ms_prec) << "Win [#]" << 
            std::left << std::setw(ms_prec) << "Loss [#]" << 
            std::left << std::setw(ms_prec) << "Win pct [%]" << std::endl;
        std::cout << std::string(6 * precision, '-') << std::endl;


        std::cout << std::left << std::setw(ms_prec) << model <<
            std::left << std::setw(ms_prec) << positions[0].type << 
            std::left << std::setw(ms_prec) << num_positions  << 
            std::left << std::setw(ms_prec) << win_trades << 
            std::left << std::setw(ms_prec) << loss_trades << 
            std::left << std::setw(ms_prec) << std::fixed << 
            std::setprecision(2) << win_pct << std::endl;
    }
}


/**
    Model openChange.

    This model can be used to backtest strategies where an position is taken
    where certain conditions related to opening prices occur, i.e. an initial 
    drop of x percent triggers long/short position, or initial increase of x 
    percent triggers long/short position.

    Observer that when using daily mode, cover of the position will be made
    within x number of data points, not days. Meaning if you have dialy data,
    cover = 1 means cover will be made at closing price tomorrow. If you have
    minute data, cover = 1 means cover will be made at closing price next
    minute.
    
    @param d: List with dates.
    @param c: List with closing prices.
    @param o: List with open prices.
    @param h: List with high prices.
    @param l: List with low prices.
    @param entry: Specifying entry, i.e. 0.02 means position (long/short) 
        is taken if stock opens 2%, where -0.02 means position is taken if stock
        opens negative 2%.
    @param mode: 'daily' / 'percentage'. When position should be covered, based
        on day or based on days or based on when a percentage is met. Observer
        that if percentage is specified, stop_loss has to be included.
    @param direction: In what direction should position be taken if entry is met,
        'long' / 'short'.
    @param cover: Specify what percentage is needed before profit should be taken, 
        i.e. 0.02 means two percent from open price (entry_price). If mode is daily,
        cover needs to be an int, specifying number of days before cover at closing price.
        cover = 0 equals same days closing price.
    @param stop_loss: Specify what percentage is needed before a stop loss should be taken,
        i.e. 0.02 means two percent from open price (entry_price.
    @param show_positions: Specify whether full summary of every positions should be
        displayed.


    TODO:
        - Change implementation of 'daily' mode such that it doesn't go by index,
        but instead by actual days. Will need to figure out how to compare days
        and thus get the last day x days forward. Perhaps this should be changes 
        such that not only days can be specified, but minutes, hours, etc. Depending
        on what data the user has.
 */
void openChange(std::vector<std::string>d, std::vector<float> close_prices, 
        std::vector<float> open_prices, std::vector<float> high_prices, 
        std::vector<float> low_prices, float entry, std::string mode, 
        std::string direction, float cover, 
        float stop_loss, bool show_positions){
    
    std::string model = "openChange";

    // Initialize data
    std::vector<struct tm> dates = config_time(d);
    //std::vector<float> close_prices = to_vector<float> (c);
    //std::vector<float> open_prices = to_vector<float> (o);
    //std::vector<float> high_prices = to_vector<float> (h);
    //std::vector<float> low_prices = to_vector<float> (l);
    int len_data = close_prices.size();

    // Save positions objects into vector.
    std::vector<Position> positions;
    
    for (int idx = 1; idx < len_data; idx++){
        float open = open_prices[idx];
        float close = close_prices[idx];
        float close_before = close_prices[idx-1];
        float high = high_prices[idx];
        float low = low_prices[idx];
        float pct_chg = (open - close_before) / close_before;
        struct tm date = dates[idx];
        
        // Check if positive or negative open.
        if ((pct_chg <= entry && entry < 0.0) || (pct_chg >= entry && entry > 0.0)){
            Position position;
            position.index = idx;
            position.entry_date = date;
            position.entry_price = open;
            position.open_pct = pct_chg;
            position.type = direction;
            
            // Going long with negative open.
            if (direction == "long"){
                position.stop_loss = (open * (1 - stop_loss));
                if (mode == "percentage")
                    position.exit_price = (open * (1 + cover));
            }

            // Going short with neagtive open.
            else if (direction == "short"){
                position.stop_loss = (open * (1 + stop_loss));
                if (mode == "percentage")
                    position.exit_price = (open * (1 - cover));
            }

            if (mode == "daily")
                position.exit_index = (position.index + cover);
            
            positions.push_back(position);
        }
    
        // Loop over all of the positions to see if update is needed.
        for (auto &position : positions){
            if (position.covered  == false){
                if (mode == "daily"){
                    if (position.exit_index == idx){
                        position.covered = true;
                        position.exit_price = close;
                        position.exit_date = date;
                    }
                }

                else if (mode == "percentage"){
                    // Handle long positions.
                    if (position.type == "long"){
                        if (low < position.stop_loss){
                            position.covered = true;
                            position.exit_date = date;
                            position.exit_price = position.stop_loss;
                        }

                        else if (high > position.exit_price){
                            position.covered = true;
                            position.exit_date = date;
                        }
                    }

                    // Handle short positions.
                    if (position.type == "short"){
                        if (high > position.stop_loss){
                            position.covered = true;
                            position.exit_date = date;
                            position.exit_price = position.stop_loss;
                        }

                        else if (low < position.exit_price){
                            position.covered = true;
                            position.exit_date = date;
                        }
                    }
                }
            }
        }
    }

    summary(model, positions, show_positions);
}


void trendCrossover(std::vector<std::string> d, std::vector<float> close_prices, 
        std::vector<float> open_prices, std::vector<float> high_prices, 
        std::vector<float> low_prices, std::string indicator, int periods, 
        int deviations) {
    
    std::string model = "trendCrossover";

    std::vector<struct tm> dates = config_time(d);
    int len_data = close_prices.size();

    // TEST PRICES
    /*
    std::vector<float> prices = {22.273, 22.194, 22.085, 22.174, 22.184, 
        22.134, 22.234, 22.432, 22.244, 22.293, 22.154, 22.393, 22.382, 
        22.611, 23.356, 24.052, 23.753, 23.832, 23.952, 23.634,
        23.823, 23.872, 23.654, 23.187, 23.098, 23.326, 22.681, 
        23.098, 22.403, 22.173};

    if (indicator == "sma")
        std::vector<float> indicator = sma_calc(close_prices, periods);    
    
    else if (indicator == "ema")
        std::vector<float> indicator = ema_calc(close_prices, periods);    

    else if (indicator == "smma")
        std::vector<float> indicator = smma_calc(close_prices, periods);    

    else if (indicator == "lwma")
        std::vector<float> indicator = lwma_calc(close_prices, periods);    
    
    else if (indicator == "bollinger_bands") {
        std::vector<float> bottom_band, top_band;
        tie(bottom_band, top_band) = bollinger_bands_calc(prices, 10, 2);
    }
    */

    
    // Save positions objects into vector.
    std::vector<Position> positions;
         
}

// Declaratio of "models" package and reachable functions.
PYBIND11_MODULE(models, m) {
    m.def("openChange", &openChange, "");
    m.def("trendCrossover", &trendCrossover, "");
}
