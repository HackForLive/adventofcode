#ifndef DP_SOLVER_HPP_
#define DP_SOLVER_HPP_

#include <vector>
#include <map>
#include <iostream>
#include <fstream>
#include <sstream>

using namespace std;

class DpSolver {
  private:
    vector<vector<vector<vector<vector<vector<vector<int>>>>>>> dp;
    map<string, vector<int>> costs;

  public:
    DpSolver(vector<vector<vector<vector<vector<vector<vector<int>>>>>>> &dp,
      map<string, vector<int>> &costs);
    
    vector<vector<vector<vector<vector<vector<vector<int>>>>>>> get_dp_table() { return dp; }

    int get_max_geodes(int time, int ore, int clay, int obs, int ore_n, int clay_n, int obs_n);
    int DpSolver::get_max_geodes_test(int time, int ore, int clay, int obs, int ore_n, int clay_n, int obs_n);
};

// inline Range::Range(int s, int e) 
// { 
//     start = s;
//     end = e;
// }

#endif