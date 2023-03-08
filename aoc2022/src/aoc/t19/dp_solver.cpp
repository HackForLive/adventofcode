#include "dp_solver.hpp"

DpSolver::DpSolver(map<string, vector<int>> &costs_map, map<string, int>& max_val, int dp_num){
    //int dp[max_values["time"]][max_values["ore_r"]][max_values["clay_r"]][max_values["obs_r"]][max_values["ore_c"]][max_values["clay_c"]][max_values["obs_c"]]

    // fill -1
    // std::fill(&dp[0][0][0][0][0][0][0],&dp[0][0][0][0][0][0][0] + sizeof(dp) / sizeof(dp[0][0][0][0][0][0][0]),-1);

    // C style
    // use std::vector
    // int dp[TIME + os][max_ore_r + os][max_clay_r + os][max_obs_r + os][max_ore_r*mos][max_clay_r*mos][max_obs_r*mos];
    
    // int*** pp;
    // int*** dd[t][t][t];

    // pp = ***dd;
    costs = costs_map;
    max_values = max_val; 

    switch (dp_num){
        case 1:
            dp1 = vector<vector<vector<vector<ItemCollector>>>>
            (max_values["time"], vector<vector<vector<ItemCollector>>>
            (max_values["ore_r"], vector<vector<ItemCollector>>
            (max_values["clay_r"], vector<ItemCollector>
            (max_values["obs_r"], ItemCollector(1,0,0,0)))));
            break;
        case 2:
            dp2 = vector<vector<vector<vector<vector<vector<vector<int>>>>>>>
            (max_values["time"], vector<vector<vector<vector<vector<vector<int>>>>>>
            (max_values["ore_r"], vector<vector<vector<vector<vector<int>>>>>
            (max_values["clay_r"], vector<vector<vector<vector<int>>>>
            (max_values["obs_r"], vector<vector<vector<int>>>
            (max_values["ore_c"], vector<vector<int>>
            (max_values["clay_c"], vector<int>
            (max_values["obs_c"], -1)))))));
            break;
        default:
            throw std::logic_error("Function not yet implemented");

    }
}

int DpSolver::get_max_geodes_slow(int time, int ore, int clay, int obs, int ore_n, int clay_n, int obs_n){
    // time is out
    if ( time <= 1 || max_values["ore_c"] <= ore_n || max_values["clay_c"] <= clay_n ||
        max_values["obs_c"] <= obs_n){
        return 0;
    }
    
    // cached
    if(dp2[time][ore][clay][obs][ore_n][clay_n][obs_n] > -1){
        return dp2[time][ore][clay][obs][ore_n][clay_n][obs_n];
    }
    
    int maximum = 0;
    // try to build robot

    if(costs["geo"][0] <= ore_n && costs["geo"][1] <= obs_n)
        maximum = max(
            get_max_geodes_slow(time-1, ore, clay, obs, ore_n+ore-costs["geo"][0], clay_n+clay, obs_n+obs-costs["geo"][1]) + time - 1, 
            maximum);
    
    if(max_values["obs_r"] > obs + 1 &&  costs["obs"][0] <= ore_n && costs["obs"][1] <= clay_n)
        maximum = max(
            get_max_geodes_slow(time-1, ore, clay, obs+1, ore_n+ore-costs["obs"][0], clay_n+clay-costs["obs"][1], obs_n+obs), 
            maximum);
    if (max_values["clay_r"] > clay + 1 && costs["clay"][0] <= ore_n)
        maximum = max(
            get_max_geodes_slow(time-1, ore, clay+1, obs, ore_n+ore-costs["clay"][0], clay_n+clay, obs_n+obs), maximum);
    
    if (max_values["ore_r"] > ore + 1 && costs["ore"][0] <= ore_n)
        maximum = max(
            get_max_geodes_slow(time-1, ore+1, clay, obs, ore_n+ore-costs["ore"][0], clay_n+clay, obs_n+obs), maximum);
        
    maximum = max(get_max_geodes_slow(time-1, ore, clay, obs, ore_n+ore, clay_n+clay, obs_n+obs), maximum);

    dp2[time][ore][clay][obs][ore_n][clay_n][obs_n] = maximum;
    return maximum;
}

short DpSolver::get_max_geodes_faster(short time, short ore, short clay, short obs, short ore_n, short clay_n, short obs_n){
    // time is out
    if ( time <= 1 || max_values["ore_c"] <= ore_n || max_values["clay_c"] <= clay_n ||
        max_values["obs_c"] <= obs_n){
        return 0;
    }
    
    // cached
    if(dp2[time][ore][clay][obs][ore_n][clay_n][obs_n] > -1){
        return dp2[time][ore][clay][obs][ore_n][clay_n][obs_n];
    }

    short maximum = 0;
    // try to build robot
    short time_to_build =  get_time_to_get_geo_robot(costs["geo"], ore_n, obs_n, ore, obs);
    if(time_to_build != -1){
        short oret =  ore_n + ore * time_to_build - costs["geo"][0];
        short clayt = clay_n + clay * time_to_build;
        short obst = obs_n + obs * time_to_build - costs["geo"][1];
        short tmp_ic = get_max_geodes_faster(time-time_to_build, ore, clay, obs, oret, clayt, obst) + max(0, time - time_to_build);
        maximum = max(maximum, tmp_ic);
    }
    if(max_values["obs_r"] > obs + 1){
        time_to_build = get_time_to_get_obsidian_robot(costs["obs"], ore_n, clay_n, ore, clay);
        if(time_to_build != -1){
            short oret =  ore_n + ore * time_to_build - costs["obs"][0];
            short clayt = clay_n + clay * time_to_build - costs["obs"][1];
            short obst = obs_n + obs * time_to_build;
            short tmp_ic = get_max_geodes_faster(time-time_to_build, ore, clay, obs+1, oret, clayt, obst);
            maximum = max(maximum, tmp_ic);
        }
    }
    if (max_values["clay_r"] > clay + 1){
        time_to_build = get_time_to_get_clay_robot(costs["clay"][0], ore_n, ore);
        if(time_to_build != -1){
            short oret =  ore_n + ore * time_to_build - costs["clay"][0];
            short clayt = clay_n + clay * time_to_build;
            short obst = obs_n + obs * time_to_build;
            short tmp_ic = get_max_geodes_faster(time-time_to_build, ore, clay+1, obs, oret, clayt, obst);
            maximum = max(maximum, tmp_ic);
        }
    }
    if (max_values["ore_r"] > ore + 1){
        time_to_build = get_time_to_get_ore_robot(costs["ore"][0], ore_n, ore);
        if(time_to_build != -1)
        {
            short oret =  ore_n + ore * time_to_build - costs["ore"][0];
            short clayt = clay_n + clay * time_to_build;
            short obst = obs_n + obs * time_to_build;
            short tmp_ic = get_max_geodes_faster(time-time_to_build, ore+1, clay, obs, oret, clayt, obst);
            maximum = max(maximum, tmp_ic);
        }
    }

    dp2[time][ore][clay][obs][ore_n][clay_n][obs_n] = maximum;
    return maximum;
}

ItemCollector DpSolver::get_max_geodes(short time, short ore, short clay, short obs, ItemCollector ic){
    // time is out
    if ( time <= 1){
        return ic;
    }
    
    // cached
    if(dp1[time][ore][clay][obs].clay == ic.clay && dp1[time][ore][clay][obs].ore == ic.ore && dp1[time][ore][clay][obs].obs == ic.obs &&
    dp1[time][ore][clay][obs].geo && ic.ore > 1 ){
        return dp1[time][ore][clay][obs];
    }
    
    ItemCollector maximum(ic.ore, ic.clay, ic.obs, ic.geo);
    // try to build robot

    short time_to_build =  get_time_to_get_geo_robot(costs["geo"], ic.ore, ic.obs, ore, obs);
    if(time_to_build != -1){
        ic.ore +=  ore * time_to_build - costs["geo"][0];
        ic.clay += clay * time_to_build;
        ic.obs += obs * time_to_build - costs["geo"][1];
        ic.geo += max(0, time - time_to_build);
        ItemCollector tmp_ic = get_max_geodes(time-time_to_build, ore, clay, obs, ic);
        if (tmp_ic.geo > maximum.geo)
           maximum = ItemCollector(tmp_ic.ore, tmp_ic.clay, tmp_ic.obs, tmp_ic.geo);
    }
    if(max_values["obs_r"] > obs + 1){
        time_to_build = get_time_to_get_obsidian_robot(costs["obs"], ic.ore, ic.clay, ore, clay);
        if(time_to_build != -1){
            ic.ore += ore * time_to_build - costs["obs"][0];
            ic.clay += clay * time_to_build - costs["obs"][1];
            ic.obs += obs * time_to_build;
            ItemCollector tmp_ic = get_max_geodes(time-time_to_build, ore, clay, obs+1, ic);
            if (tmp_ic.geo > maximum.geo)
                maximum = ItemCollector(tmp_ic.ore, tmp_ic.clay, tmp_ic.obs, tmp_ic.geo);
        }
    }
    if (max_values["clay_r"] > clay + 1){
        time_to_build = get_time_to_get_clay_robot(costs["clay"][0], ic.ore, ore);
        if(time_to_build != -1){
            ic.ore += ore * time_to_build - costs["clay"][0];
            ic.clay += clay * time_to_build;
            ic.obs += obs * time_to_build;
            ItemCollector tmp_ic = get_max_geodes(time-time_to_build, ore, clay+1, obs, ic);
            if (tmp_ic.geo > maximum.geo)
                maximum = ItemCollector(tmp_ic.ore, tmp_ic.clay, tmp_ic.obs, tmp_ic.geo);
        }
    }
    if (max_values["ore_r"] > ore + 1){
        time_to_build = get_time_to_get_ore_robot(costs["ore"][0], ic.ore, ore);
        if(time_to_build != -1)
        {
            ic.ore += ore * time_to_build - costs["ore"][0];
            ic.clay += clay * time_to_build;
            ic.obs += obs * time_to_build;
            ItemCollector tmp_ic = get_max_geodes(time-time_to_build, ore+1, clay, obs, ic);
            if (tmp_ic.geo > maximum.geo)
                maximum = ItemCollector(tmp_ic.ore, tmp_ic.clay, tmp_ic.obs, tmp_ic.geo);
        }
    }

    dp1[time][ore][clay][obs] = maximum;
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
