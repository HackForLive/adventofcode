#include "dp_solver.hpp"

DpSolver::DpSolver(vector<vector<vector<vector<vector<vector<vector<int>>>>>>> &vec,
    map<string, vector<int>> &costs_map){
    dp = vec;
    costs = costs_map;
}

int DpSolver::get_max_geodes(int time, int ore, int clay, int obs, int ore_n, int clay_n, int obs_n){
    // time is out
    if ( time <= 0 || dp[0][0][0][0].size() <= ore_n || dp[0][0][0][0][0].size() <= clay_n ||
        dp[0][0][0][0][0][0].size() <= obs_n){
        return 0;
    }
    
    // cached
    if(dp[time][ore][clay][obs][ore_n][clay_n][obs_n] > -1){
        return dp[time][ore][clay][obs][ore_n][clay_n][obs_n];
    }
    
    int maximum = 0;
    // try to build robot

    if(costs["geo"][0] <= ore_n && costs["geo"][1] <= obs_n)
        maximum = max(
            get_max_geodes(time-1, ore, clay, obs, ore_n+ore-costs["geo"][0], clay_n+clay, obs_n+obs-costs["geo"][1]) + time - 1, 
            maximum);
    
    if(dp[0][0][0].size() > obs + 1 and  costs["obs"][0] <= ore_n and costs["obs"][1] <= clay_n)
        maximum = max(
            get_max_geodes(time-1, ore, clay, obs+1, ore_n+ore-costs["obs"][0], clay_n+clay-costs["obs"][1], obs_n+obs), 
            maximum);
    if (dp[0][0].size() > clay + 1 and costs["clay"][0] <= ore_n)
        maximum = max(
            get_max_geodes(time-1, ore, clay+1, obs, ore_n+ore-costs["clay"][0], clay_n+clay, obs_n+obs), maximum);
    
    if (dp[0].size() > ore + 1 and costs["ore"][0] <= ore_n)
        maximum = max(
            get_max_geodes(time-1, ore+1, clay, obs, ore_n+ore-costs["ore"][0], clay_n+clay, obs_n+obs), maximum);
        
    maximum = max(get_max_geodes(time-1, ore, clay, obs, ore_n+ore, clay_n+clay, obs_n+obs), maximum);

    dp[time][ore][clay][obs][ore_n][clay_n][obs_n] = maximum;
    return maximum;
}

int DpSolver::get_max_geodes_test(int time, int ore, int clay, int obs, int ore_n, int clay_n, int obs_n){
    // time is out
    if ( time <= 0 || dp[0][0][0][0].size() <= ore_n || dp[0][0][0][0][0].size() <= clay_n ||
        dp[0][0][0][0][0][0].size() <= obs_n){
        return 0;
    }
    
    // cached
    if(dp[time][ore][clay][obs][ore_n][clay_n][obs_n] > -1){
        return dp[time][ore][clay][obs][ore_n][clay_n][obs_n];
    }
    
    int maximum = 0;
    // try to build robot

    if(costs["geo"][0] <= ore_n && costs["geo"][1] <= obs_n)
        maximum = max(
            get_max_geodes(time-1, ore, clay, obs, ore_n+ore-costs["geo"][0], clay_n+clay, obs_n+obs-costs["geo"][1]) + time - 1, 
            maximum);
    
    if(dp[0][0][0].size() > obs + 1 and  costs["obs"][0] <= ore_n and costs["obs"][1] <= clay_n)
        maximum = max(
            get_max_geodes(time-1, ore, clay, obs+1, ore_n+ore-costs["obs"][0], clay_n+clay-costs["obs"][1], obs_n+obs), 
            maximum);
    if (dp[0][0].size() > clay + 1 and costs["clay"][0] <= ore_n)
        maximum = max(
            get_max_geodes(time-1, ore, clay+1, obs, ore_n+ore-costs["clay"][0], clay_n+clay, obs_n+obs), maximum);
    
    if (dp[0].size() > ore + 1 and costs["ore"][0] <= ore_n)
        maximum = max(
            get_max_geodes(time-1, ore+1, clay, obs, ore_n+ore-costs["ore"][0], clay_n+clay, obs_n+obs), maximum);
        
    maximum = max(get_max_geodes(time-1, ore, clay, obs, ore_n+ore, clay_n+clay, obs_n+obs), maximum);

    dp[time][ore][clay][obs][ore_n][clay_n][obs_n] = maximum;
    return maximum;
}

int get_time_to_get_geo_robot(const int& ore, const int& obs, 
    const int& ore_n, const int& obs_n) {
        
}

int get_time_to_get_geo_robot_r(const int& ore, const int& clay, const int& obs, 
    const int& ore_n, const int& clay_n, const int& obs_n) {
        
}
