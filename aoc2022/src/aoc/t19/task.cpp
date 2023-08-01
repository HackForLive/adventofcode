#include <iostream>
#include <fstream>
#include <sstream>
#include <set>
#include <queue>
#include <vector>
#include <array>
#include <algorithm>
#include <memory>
#include <map>

#include "dp_solver.hpp"
#include "dp_hash_solver.hpp"
#include "item_collector.hpp"

// #include <boost/algorithm/string.hpp>

using namespace std;

//
// How to build
//
//  g++ -o test aoc2022/src/aoc/t19/task.cpp aoc2022/src/aoc/t19/dp_solver.cpp 
//  aoc2022/src/aoc/t19/dp_hash_solver.cpp aoc2022/src/aoc/t19/node.cpp -I /home/michael/Downloads/boost-1.82.0/libs/
//

int get_result_dp_table(int t, map<string, vector<int>>& costs, map<string, int>& max_values);
int get_result_dp_hash_map(int t, map<string, vector<int>>& costs, map<string, int>& max_values);
void print_how_many_values(vector<vector<vector<vector<ItemCollector>>>> &f, int value);
vector<int> getNumberFromString(string s);

vector<int> getNumberFromString(string s) {
   stringstream str_strm;
   str_strm << s; //convert the string s into stringstream
   string temp_str;
   int temp_int;
   vector<int> nums;
   while(!str_strm.eof()) {
      str_strm >> temp_str; //take words into temp_str one by one
      if(stringstream(temp_str) >> temp_int) { //try to convert string to int
        //  cout << temp_int << " ";
         nums.push_back(temp_int);
      }
      temp_str = ""; //clear temp string
   }
//    cout << endl << endl;
   return nums;
}

int main() 
{
    auto input = std::ifstream("aoc2022/src/aoc/t19/input.txt");
    const int TIME = 32;
    int result = 1;
    
    for( std::string line; getline( input, line ); ){
        vector<int> vec = getNumberFromString(line);
    
        int id = vec[0];
        if (id == 4) break;
        int ore_cost = vec[1];
        int clay_cost = vec[2];
        int obs_cost = vec[3];
        int obs2_cost = vec[4];
        int geo_cost = vec[5];
        int geo2_cost = vec[6];

        int os = 1;
        const int mos = 4;
        int max_ore_r = max(clay_cost, max(obs_cost, geo_cost));
        int max_clay_r = obs2_cost;
        const int max_obs_r = geo2_cost;

        map<string, vector<int>> costs = {
            { "ore", {ore_cost} },
            { "clay", {clay_cost} },
            { "obs", {obs_cost, obs2_cost} },
            { "geo", {geo_cost, geo2_cost} }
        };

        map<string, int> max_values = {
            { "time", TIME + os },
            { "ore_r", max_ore_r + os },
            { "clay_r", max_clay_r + os },
            { "obs_r", max_obs_r + os },
            { "ore_c", max_ore_r*mos },
            { "clay_c", max_clay_r*mos },
            { "obs_c", max_obs_r*mos },
        };

        int res = 0;
        // res = get_result_dp_table(TIME, costs, max_values);
        res = get_result_dp_hash_map(TIME, costs, max_values);
        std::cout << res << endl;
        result *= res;
    }
     std::cout << result << endl;
}

int get_result_dp_table(int t, map<string, vector<int>>& costs, map<string, int>& max_values){
    DpSolver dp_s = DpSolver(costs, max_values, 2);
    int res = 0;
    // ItemCollector ic;
    // res = dp_s.get_max_geodes(t, 1, 0, 0, ic).geo;

    res = dp_s.get_max_geodes_faster(t, 1, 0, 0, 0, 0, 0);
    // auto k = dp_s.get_dp_table();
    // print_how_many_values(k, -1);
    return res;
}

int get_result_dp_hash_map(int t, map<string, vector<int>>& costs, map<string, int>& max_values){
    auto dp_hash_s = DpHashSolver(costs, max_values);
    return dp_hash_s.get_max_geodes(t, 1, 0, 0, 0, 0, 0);
}

void print_how_many_values(vector<vector<vector<vector<ItemCollector>>>> &f, int val){
    unsigned long long sum = 0;
    unsigned long long count = 0;
    // for(auto &i : f)
    //     for(auto &j : i)
    //         for(auto &k : j)
                for(auto &l : f)
                    for(auto &m : l)
                        for(auto &n : m)
                            for(auto &o : m)
                                for(auto &p : o){
                                    count++;
                                    if(p.ore == 1 && p.clay == 0 && p.obs == 0 && p.geo == 0 )
                                        sum++;
                                }
    cout << "how many: " << val << " it has: " << sum  << endl;
    cout << "out of: " << count << endl; 
    cout << ((float)(sum/(float)count)) * 100 << "perc" << endl;
}
