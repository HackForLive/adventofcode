#include "dp_solver.hpp"

DpSolver::DpSolver(vector<vector<vector<vector<ItemCollector>>>> &vec,
    map<string, vector<int>> &costs_map){
    dp = vec;
    costs = costs_map;
}

// int DpSolver::get_max_geodes_slow(int time, int ore, int clay, int obs, int ore_n, int clay_n, int obs_n){
//     // time is out
//     if ( time <= 0 || dp[0][0][0][0].size() <= ore_n || dp[0][0][0][0][0].size() <= clay_n ||
//         dp[0][0][0][0][0][0].size() <= obs_n){
//         return 0;
//     }
    
//     // cached
//     if(dp[time][ore][clay][obs][ore_n][clay_n][obs_n] > -1){
//         return dp[time][ore][clay][obs][ore_n][clay_n][obs_n];
//     }
    
//     int maximum = 0;
//     // try to build robot

//     if(costs["geo"][0] <= ore_n && costs["geo"][1] <= obs_n)
//         maximum = max(
//             get_max_geodes_slow(time-1, ore, clay, obs, ore_n+ore-costs["geo"][0], clay_n+clay, obs_n+obs-costs["geo"][1]) + time - 1, 
//             maximum);
    
//     if(dp[0][0][0].size() > obs + 1 &&  costs["obs"][0] <= ore_n && costs["obs"][1] <= clay_n)
//         maximum = max(
//             get_max_geodes_slow(time-1, ore, clay, obs+1, ore_n+ore-costs["obs"][0], clay_n+clay-costs["obs"][1], obs_n+obs), 
//             maximum);
//     if (dp[0][0].size() > clay + 1 && costs["clay"][0] <= ore_n)
//         maximum = max(
//             get_max_geodes_slow(time-1, ore, clay+1, obs, ore_n+ore-costs["clay"][0], clay_n+clay, obs_n+obs), maximum);
    
//     if (dp[0].size() > ore + 1 && costs["ore"][0] <= ore_n)
//         maximum = max(
//             get_max_geodes_slow(time-1, ore+1, clay, obs, ore_n+ore-costs["ore"][0], clay_n+clay, obs_n+obs), maximum);
        
//     maximum = max(get_max_geodes_slow(time-1, ore, clay, obs, ore_n+ore, clay_n+clay, obs_n+obs), maximum);

//     dp[time][ore][clay][obs][ore_n][clay_n][obs_n] = maximum;
//     return maximum;
// }

ItemCollector DpSolver::get_max_geodes(short time, short ore, short clay, short obs, ItemCollector ic){
    // time is out
    if ( time <= 0){
        return ic;
    }
    
    // cached
    if(dp[time][ore][clay][obs].clay > 0 || dp[time][ore][clay][obs].ore > 1 || dp[time][ore][clay][obs].obs > 0 ||
    dp[time][ore][clay][obs].geo > 0){
        return dp[time][ore][clay][obs];
    }
    
    ItemCollector maximum(1, 0, 0, 0);
    // try to build robot

    short time_to_build =  get_time_to_get_geo_robot(costs["geo"], ic.ore, ic.obs, ore, obs);
    if(time_to_build != -1){
        ic.ore +=  ore * time_to_build - costs["geo"][0];
        ic.clay += clay * time_to_build;
        ic.obs += obs * time_to_build - costs["geo"][1];
        ItemCollector tmp_ic = get_max_geodes(time-time_to_build, ore, clay, obs, ic);
        short tmp = tmp_ic.geo + time - time_to_build;
        if (tmp > maximum.geo)
           maximum = ItemCollector(tmp_ic.ore, tmp_ic.clay, tmp_ic.obs, tmp);
    }
    if(dp[0][0][0].size() > obs + 1){
        time_to_build = get_time_to_get_obsidian_robot(costs["obs"], ic.ore, ic.clay, ore, clay);
        ic.ore += ore * time_to_build - costs["obs"][0];
        ic.clay += clay * time_to_build - costs["obs"][1];
        ic.obs += obs * time_to_build;
        if(time_to_build != -1){
            ItemCollector tmp_ic = get_max_geodes(time-time_to_build, ore, clay, obs+1, ic);
            short tmp = tmp_ic.geo;
            if (tmp > maximum.geo)
                maximum = ItemCollector(tmp_ic.ore, tmp_ic.clay, tmp_ic.obs, tmp);
        }
    }
    if (dp[0][0].size() > clay + 1){
        time_to_build = get_time_to_get_clay_robot(costs["clay"][0], ic.ore, ore);
        ic.ore += ore * time_to_build - costs["clay"][0];
        ic.clay += clay * time_to_build;
        ic.obs += obs * time_to_build;
        if(time_to_build != -1){
            ItemCollector tmp_ic = get_max_geodes(time-time_to_build, ore, clay+1, obs, ic);
            short tmp = tmp_ic.geo;
            if (tmp > maximum.geo)
                maximum = ItemCollector(tmp_ic.ore, tmp_ic.clay, tmp_ic.obs, tmp);
        }
    }
    if (dp[0].size() > ore + 1){
        time_to_build = get_time_to_get_ore_robot(costs["ore"][0], ic.ore, ore);
        ic.ore += ore * time_to_build - costs["ore"][0];
        ic.clay += clay * time_to_build;
        ic.obs += obs * time_to_build;
        if(time_to_build != -1)
        {
            ItemCollector tmp_ic = get_max_geodes(time-time_to_build, ore+1, clay, obs, ic);
            short tmp = tmp_ic.geo;
            if (tmp > maximum.geo)
                maximum = ItemCollector(tmp_ic.ore, tmp_ic.clay, tmp_ic.obs, tmp);
        }
    }

    dp[time][ore][clay][obs] = maximum;
    return maximum;
}

int DpSolver::get_time_to_get_robot(const int& robot_cost, const int& items, const int& items_per_time_unit) {
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

int DpSolver::get_time_to_get_ore_robot(const int& ore_robot_cost, const int& ore_count, const int& ore_count_per_time_unit) {
    return get_time_to_get_robot(ore_robot_cost, ore_count, ore_count_per_time_unit);
}

int DpSolver::get_time_to_get_clay_robot(const int& clay_robot_cost, const int& ore_count, const int& ore_count_per_time_unit) {
    return get_time_to_get_ore_robot(clay_robot_cost, ore_count, ore_count_per_time_unit);
}

int DpSolver::get_time_to_get_obsidian_robot(const vector<int>& obs_robot_cost, const int& ore_count, const int& clay_count, 
const int& ore_count_per_time_unit, const int& clay_count_per_time_unit) {
    int time1 = get_time_to_get_robot(obs_robot_cost[0], ore_count, ore_count_per_time_unit);
    int time2 = get_time_to_get_robot(obs_robot_cost[1], clay_count, clay_count_per_time_unit);
    
    return (time1 == -1 || time2 == -1) ? -1: max(time1, time2);
}

int DpSolver::get_time_to_get_geo_robot(const vector<int>& geo_robot_cost, const int& ore_count, const int& obs_count, 
const int& ore_count_per_time_unit, const int& obs_count_per_time_unit) {
    return get_time_to_get_obsidian_robot(geo_robot_cost, ore_count, obs_count, ore_count_per_time_unit, obs_count_per_time_unit);
}
