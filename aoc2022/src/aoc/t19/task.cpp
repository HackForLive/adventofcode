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

// #include <boost/algorithm/string.hpp>

using namespace std;

//
// How to build
//
//  g++ -o adv_2022_19 task.cpp dp_solver.cpp -I /path_to/boost_1_80_0
//

int get_result_dp_table(int t, map<string, vector<int>>& costs, map<string, int>& max_values);
int get_result_dp_hash_map(int t, map<string, vector<int>>& costs, map<string, int>& max_values);
void print_how_many_values(vector<vector<vector<vector<vector<vector<vector<int>>>>>>> &f, int value);
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
    auto input = std::ifstream(".\\aoc2022\\src\\aoc\\t19\\inputt.txt");
    const int TIME = 24;
    int result = 0;
    
    for( std::string line; getline( input, line ); ){
        vector<int> vec = getNumberFromString(line);
    
        int id = vec[0];
        int ore_cost = vec[1];
        int clay_cost = vec[2];
        int obs_cost = vec[3];
        int obs2_cost = vec[4];
        int geo_cost = vec[5];
        int geo2_cost = vec[6];

        int os = 1;
        const int mos = 3;
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
        res = get_result_dp_table(TIME, costs, max_values);
        // res = get_result_dp_hash_map(TIME, costs, max_values);
        std::cout << res << endl;
        result = result + id * res;
        // auto k = dp_s.get_dp_table();
        // print_how_many_values(k, -1);
    }
     std::cout << result << endl;
}

int get_result_dp_table(int t, map<string, vector<int>>& costs, map<string, int>& max_values){
    // cout << "ha" << endl;
    vector<vector<vector<vector<vector<vector<vector<int8_t>>>>>>> f;
    f = vector<vector<vector<vector<vector<vector<vector<int8_t>>>>>>>
    (max_values["time"], vector<vector<vector<vector<vector<vector<int8_t>>>>>>
    (max_values["ore_r"], vector<vector<vector<vector<vector<int8_t>>>>>
    (max_values["clay_r"], vector<vector<vector<vector<int8_t>>>>
    (max_values["obs_r"], vector<vector<vector<int8_t>>>
    (max_values["ore_c"], vector<vector<int8_t>>
    (max_values["clay_c"], vector<int8_t>
    (max_values["obs_c"], -1)))))));

    //int dp[max_values["time"]][max_values["ore_r"]][max_values["clay_r"]][max_values["obs_r"]][max_values["ore_c"]][max_values["clay_c"]][max_values["obs_c"]]

    // fill -1
    // std::fill(&dp[0][0][0][0][0][0][0],&dp[0][0][0][0][0][0][0] + sizeof(dp) / sizeof(dp[0][0][0][0][0][0][0]),-1);

    // C style
    // use std::vector
    // int dp[TIME + os][max_ore_r + os][max_clay_r + os][max_obs_r + os][max_ore_r*mos][max_clay_r*mos][max_obs_r*mos];
    
    // int*** pp;
    // int*** dd[t][t][t];

    // pp = ***dd;

    // cout << "ha1" << endl;
    DpSolver dp_s = DpSolver(f, costs);
    int res = 0;
    // res = dp_s.get_max_geodes(t, 1, 0, 0, 0, 0, 0);
    res = dp_s.get_max_geodes_test(t, 1, 0, 0, 0, 0, 0);
    // cout << "ha2" << endl;
    return res;
}

int get_result_dp_hash_map(int t, map<string, vector<int>>& costs, map<string, int>& max_values){
    auto dp_hash_s = DpHashSolver(costs, max_values);
    return dp_hash_s.get_max_geodes(t, 1, 0, 0, 0, 0, 0);
}

void print_how_many_values(vector<vector<vector<vector<vector<vector<vector<int>>>>>>> &f, int val){
    long sum = 0;
    long count = 0;
    for(auto &i : f)
        for(auto &j : i)
            for(auto &k : j)
                for(auto &l : k)
                    for(auto &m : l)
                        for(auto &n : m)
                            for(auto &o : m)
                                for(auto &p : o){
                                    count++;
                                    if(p == val)
                                        sum++;
                                }
    cout << "how many: " << val << " it has: " << sum  << endl;
    cout << "out of: " << count << endl; 
    cout << ((float)(sum/(float)count)) * 100 << "perc" << endl;
}
