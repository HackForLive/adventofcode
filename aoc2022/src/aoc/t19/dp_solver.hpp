#ifndef DP_SOLVER_HPP_
#define DP_SOLVER_HPP_

#include <vector>
#include <map>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>

#include "item_collector.hpp"

using namespace std;

class DpSolver {
  private:
    vector<vector<vector<vector<ItemCollector>>>> dp1;
    vector<vector<vector<vector<vector<vector<vector<int>>>>>>> dp2;
    map<string, vector<int>> costs;
    map<string, int> max_values;

  public:
    DpSolver(map<string, vector<int>> &costs, map<string, int>& max_values, int dp_num);
    
    vector<vector<vector<vector<ItemCollector>>>> get_dp_table1() { return dp1; }
    vector<vector<vector<vector<vector<vector<vector<int>>>>>>> get_dp_table2() { return dp2; }

    int get_max_geodes_slow(int time, int ore, int clay, int obs, int ore_n, int clay_n, int obs_n);
    short get_max_geodes_faster(short time, short ore, short clay, short obs, short ore_n, short clay_n, short obs_n);
    ItemCollector get_max_geodes(short time, short ore, short clay, short obs, ItemCollector ic);
    int get_time_to_get_robot(const int& robot_cost, const int& items, const int& items_per_time_unit);
    int get_time_to_get_ore_robot(const int& ore_robot_cost, const int& ore_count, const int& ore_count_per_time_unit);
    int get_time_to_get_clay_robot(const int& clay_robot_cost, const int& ore_count, const int& ore_count_per_time_unit);
    int get_time_to_get_obsidian_robot(const vector<int>& obsidian_robot_cost, const int& ore_count, const int& clay_count, 
                                       const int& ore_count_per_time_unit, const int& clay_count_per_time_unit);
    int get_time_to_get_geo_robot(const vector<int>& geo_robot_cost, const int& ore_count, const int& obs_count, 
                                  const int& ore_count_per_time_unit, const int& obs_count_per_time_unit);
};

#endif