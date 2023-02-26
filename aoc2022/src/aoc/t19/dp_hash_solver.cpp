#include "dp_hash_solver.hpp"

DpHashSolver::DpHashSolver(map<string, vector<int>> &costs_map, map<string, int> & max_vals){
    costs = costs_map;
    max_values = max_vals;
}

int DpHashSolver::get_max_geodes(int time, int ore, int clay, int obs, int ore_n, int clay_n, int obs_n){
    // time is out
    if ( time <= 0 || max_values["ore_c"] <= ore_n || max_values["clay_c"] <= clay_n ||
        max_values["obs_c"] <= obs_n){
        return 0;
    }

    auto node = Node(time, ore, clay, obs, ore_n, clay_n, obs_n);
    
    // cached
    if (dp.find(node) != dp.end()){
      return dp[node];
    }
    
    int maximum = 0;
    // try to build robot

    if(costs["geo"][0] <= ore_n && costs["geo"][1] <= obs_n)
        maximum = max(
            get_max_geodes(time-1, ore, clay, obs, ore_n+ore-costs["geo"][0], clay_n+clay, obs_n+obs-costs["geo"][1]) + time - 1, 
            maximum);
    
    if(max_values["obs_r"] > obs + 1 and  costs["obs"][0] <= ore_n and costs["obs"][1] <= clay_n)
        maximum = max(
            get_max_geodes(time-1, ore, clay, obs+1, ore_n+ore-costs["obs"][0], clay_n+clay-costs["obs"][1], obs_n+obs), 
            maximum);
    if (max_values["clay_r"] > clay + 1 and costs["clay"][0] <= ore_n)
        maximum = max(
            get_max_geodes(time-1, ore, clay+1, obs, ore_n+ore-costs["clay"][0], clay_n+clay, obs_n+obs), maximum);
    
    if (max_values["ore_r"] > ore + 1 and costs["ore"][0] <= ore_n)
        maximum = max(
            get_max_geodes(time-1, ore+1, clay, obs, ore_n+ore-costs["ore"][0], clay_n+clay, obs_n+obs), maximum);
        
    maximum = max(get_max_geodes(time-1, ore, clay, obs, ore_n+ore, clay_n+clay, obs_n+obs), maximum);

    dp[node] = maximum;
    return maximum;
}
