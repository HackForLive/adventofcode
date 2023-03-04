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
    vector<vector<vector<vector<ItemCollector>>>> dp;
    map<string, vector<int>> costs;

  public:
    DpSolver(vector<vector<vector<vector<ItemCollector>>>> &dp,
      map<string, vector<int>> &costs);
    
    vector<vector<vector<vector<ItemCollector>>>> get_dp_table() { return dp; }

    int get_max_geodes_slow(int time, int ore, int clay, int obs, int ore_n, int clay_n, int obs_n);
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