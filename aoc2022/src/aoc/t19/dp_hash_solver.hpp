#ifndef DP_HASH_SOLVER_HPP_
#define DP_HASH_SOLVER_HPP_

#include <vector>
#include <unordered_map>
#include <map>
#include <iostream>
#include <fstream>
#include <sstream>

#include "node.hpp"

using namespace std;

class DpHashSolver {
  private:
    unordered_map<Node, int> dp;
    map<string, vector<int>> costs;
    map<string, int> max_values;

  public:
    DpHashSolver(map<string, vector<int>> &costs, map<string, int> & max_vals);

    int get_max_geodes(int time, int ore, int clay, int obs, int ore_n, int clay_n, int obs_n);
};

#endif