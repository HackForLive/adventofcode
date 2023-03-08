#include "dp_hash_solver.hpp"

DpHashSolver::DpHashSolver(map<string, vector<int>> &costs_map, map<string, int> & max_vals){
    costs = costs_map;
    max_values = max_vals;
}

int DpHashSolver::get_max_geodes(int8_t time, int8_t ore, int8_t clay, int8_t obs, int8_t ore_n, int8_t clay_n, int8_t obs_n){
    // time is out
    if ( time <= 1 || max_values["ore_c"] <= ore_n || max_values["clay_c"] <= clay_n ||
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

    int time_to_build =  get_time_to_get_geo_robot(costs["geo"], ore_n, obs_n, ore, obs);
    if(time_to_build != -1){
        maximum = max(
            get_max_geodes(time-time_to_build, ore, clay, obs, ore_n+ore*time_to_build-costs["geo"][0], clay_n+clay*time_to_build,
            obs_n+obs*time_to_build-costs["geo"][1]) + time - time_to_build, 
            maximum);
    }
    if(max_values["obs_r"] > obs + 1){
        time_to_build = get_time_to_get_obsidian_robot(costs["obs"], ore_n, clay_n, ore, clay);
        if(time_to_build != -1)
            maximum = max(
                get_max_geodes(time-time_to_build, ore, clay, obs+1, ore_n+time_to_build*ore-costs["obs"][0],
                clay_n+clay*time_to_build-costs["obs"][1], obs_n+obs*time_to_build), 
                maximum);
    }
    if (max_values["clay_r"] > clay + 1){
        time_to_build = get_time_to_get_clay_robot(costs["clay"][0], ore_n, ore);
        if(time_to_build != -1)
            maximum = max(
                get_max_geodes(time-time_to_build, ore, clay+1, obs, ore_n+ore*time_to_build-costs["clay"][0], 
                clay_n + clay * time_to_build, obs_n + obs * time_to_build), maximum);
    }
    if (max_values["ore_r"] > ore + 1){
        time_to_build = get_time_to_get_ore_robot(costs["ore"][0], ore_n, ore);
        if(time_to_build != -1)
            maximum = max(get_max_geodes(
                time-time_to_build, ore+1, clay, obs,  ore_n+ore*time_to_build-costs["ore"][0], 
                clay_n + clay * time_to_build, obs_n + obs * time_to_build), maximum);
    }

    dp[node] = maximum;
    return maximum;
}

int DpHashSolver::get_time_to_get_robot(const int& robot_cost, const int& items, const int& items_per_time_unit) {
    if(items_per_time_unit == 0){
        return -1;
    }
    // we have all items needed
    if(robot_cost-items <= 0){
        return 1;
    }
    // robot takes + 1 minute to create 
    return static_cast<int>(ceil((robot_cost-items)/(double)items_per_time_unit)) + 1;
}

int DpHashSolver::get_time_to_get_ore_robot(const int& ore_robot_cost, const int& ore_count, const int& ore_count_per_time_unit) {
    return get_time_to_get_robot(ore_robot_cost, ore_count, ore_count_per_time_unit);
}

int DpHashSolver::get_time_to_get_clay_robot(const int& clay_robot_cost, const int& ore_count, const int& ore_count_per_time_unit) {
    return get_time_to_get_ore_robot(clay_robot_cost, ore_count, ore_count_per_time_unit);
}

int DpHashSolver::get_time_to_get_obsidian_robot(const vector<int>& obs_robot_cost, const int& ore_count, const int& clay_count, 
const int& ore_count_per_time_unit, const int& clay_count_per_time_unit) {
    int time1 = get_time_to_get_robot(obs_robot_cost[0], ore_count, ore_count_per_time_unit);
    int time2 = get_time_to_get_robot(obs_robot_cost[1], clay_count, clay_count_per_time_unit);
    
    return (time1 == -1 || time2 == -1) ? -1: max(time1, time2);
}

int DpHashSolver::get_time_to_get_geo_robot(const vector<int>& geo_robot_cost, const int& ore_count, const int& obs_count, 
const int& ore_count_per_time_unit, const int& obs_count_per_time_unit) {
    return get_time_to_get_obsidian_robot(geo_robot_cost, ore_count, obs_count, ore_count_per_time_unit, obs_count_per_time_unit);
}
