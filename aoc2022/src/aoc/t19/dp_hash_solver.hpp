#ifndef DP_HASH_SOLVER_HPP_
#define DP_HASH_SOLVER_HPP_

#include <vector>
#include <array>
#include <unordered_map>
#include <map>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>

#include "node.hpp"

using namespace std;

class DpHashSolver {
  private:
    unordered_map<Node, int8_t> dp;
    map<string, vector<int>> costs;
    map<string, int> max_values;

  public:
    DpHashSolver(map<string, vector<int>> &costs, map<string, int> & max_vals);

    int get_max_geodes(int8_t time, int8_t ore, int8_t clay, int8_t obs, int8_t ore_n, int8_t clay_n, int8_t obs_n);
    int get_time_to_get_robot(const int& robot_cost, const int& items, const int& items_per_time_unit);
    int get_time_to_get_ore_robot(const int& ore_robot_cost, const int& ore_count, const int& ore_count_per_time_unit);
    int get_time_to_get_clay_robot(const int& clay_robot_cost, const int& ore_count, const int& ore_count_per_time_unit);
    int get_time_to_get_obsidian_robot(const vector<int>& obsidian_robot_cost, const int& ore_count, const int& clay_count, 
                                       const int& ore_count_per_time_unit, const int& clay_count_per_time_unit);
    int get_time_to_get_geo_robot(const vector<int>& geo_robot_cost, const int& ore_count, const int& obs_count, 
                                  const int& ore_count_per_time_unit, const int& obs_count_per_time_unit);
};

#endif