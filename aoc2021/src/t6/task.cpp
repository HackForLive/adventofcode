// Model growth of Lantern Fish
// first part: how many fish after 80 days
// second part: how many fish after 256 days

// $ ./task 256
// Using 2D memo array:1695929023803
// 0.00010114 seconds
// Using 1D memo array:1695929023803
// 2.4143e-05 seconds
// Using 1D memo array:1695929023803
// 2.4489e-05 seconds
// Using recurse:1695929023803
// 114.802 seconds

#include <iostream>
#include <fstream>
#include <vector>
#include <array>
#include <map>
#include <sstream>
#include <ctime>
#include <filesystem>
#include "decorator.hpp"

//
// How to build
//
//  g++ -o adv_2022_10 task.cpp decorator.cpp
//
std::vector<int> take_int(std::string str) {
    std::stringstream ss(str);
    std::vector<int> result;
    char ch;
    int tmp;
    while(ss >> tmp) {
        result.push_back(tmp);
        ss >> ch;
    }
    return result;
}

std::vector<int> read_test_input(){
    // std::cout << std::filesystem::current_path();
    auto input = std::ifstream("test.txt");
    std::string line; getline( input, line );
    return take_int(line);
}

// Exponential
long naive_recurse(int days, int number){
    if (days - number < 1) {
        return 1;
    }

    return naive_recurse(days-number - 1, 8) + naive_recurse(days-number - 1, 6); 
}

long get_naive_recurse_result(std::vector<int>& start_lanternfish_numbers, int days = 80){
    
    long res = 0;
    std::map<int, long> memo;
    for(const auto& num : start_lanternfish_numbers){
        
        long tmp;
        if (memo.find( num ) != memo.end()){
            tmp = memo[num];
        }
        else{
            tmp = naive_recurse(days, num);
            memo[num] = tmp;
        }
        
        res += tmp;
    }

    std::cout << "Using recurse:" << res << std::endl;
    return res;
}

// Exponential time, // Exponential memory
int get_naive_simulation_result(std::vector<int> inputs, int days = 80){
    for(int i = 0; i < days; i++){
        int k = inputs.size();
        for(int j = 0; j < k; j++){
            if(inputs[j] > 0) inputs[j]--;
            else{
                inputs[j] = 6;
                inputs.push_back(8);
            }
        }
    }
    std::cout << "Using naive method:" << inputs.size() << std::endl;
    return inputs.size();
}

// O(days) - time, O(days*cycle_count) - memory
long get_result_using_2d(std::vector<int> & start_lanternfish_numbers, int days = 80){

    const int states_n = 9;
    long  matrix[300][states_n];
    for(int i = 0; i < states_n; i++){
        // sub optimal
        matrix[0][i] = 1;
    }

    for(int i = 1; i < days; i++){
        for(int j = states_n -1; j >= 0; j--){
            if (j == 0) {
                matrix[i][j] = matrix[i-1][6] + matrix[i-1][8];
            }else{
                matrix[i][j] = matrix[i-1][j-1];
            }
        }
    }

    long res = 0;
    for(const auto& num : start_lanternfish_numbers){
        res = res + matrix[(std::max(days-num, 0))][0];
    }

    std::cout << "Using 2D memo array:" << res << std::endl;
    return res;
}

// O(days) - time, O(days) - memory
long get_result_using_1d(std::vector<int> & start_lanternfish_numbers, int days = 80){

    // shift array
    const int start_index = 9;
    // precompute first entries
    long matrix[300] = {1, 2, 2, 2, 2, 2, 2, 2, 3};

    for(int i = start_index; i < days; i++)
        matrix[i] = matrix[i-start_index+2] + matrix[i-start_index];

    long res = 0;
    for(const auto& num : start_lanternfish_numbers){
        res = res + matrix[(std::max(days-num, 0))];
    }

    std::cout << "Using 1D memo array:" << res << std::endl;
    return res;
}

// O(days) - time, O(1) - memory
long get_result_using_1d_memory_improved(std::vector<int> & start_lanternfish_numbers, int days = 80){

    long res = 0;
    const int n = 9; // 0-8 cycle states
    long matrix[n];
    std::fill(std::begin(matrix), std::end(matrix), 1);

    for(int i = 1; i < days; i++)
        matrix[i%n] += matrix[(i+2)%n];

    for(const auto& num : start_lanternfish_numbers)
        res = res + matrix[(std::max(days-num, 0))%n];

    std::cout << "Using 1D memo array:" << res << std::endl;
    return res;
}

int main(int argc, char* argv[]){
    if (argc < 2){
        std::cout << "Missing days parameter!" << std::endl;
        return 1;
    }

    int days = std::stoi(argv[1]);
    const int naive_day_limit = 140;
    const int naive_recurse_day_limit = 257;
    
    std::vector<int> numbers = read_test_input();
    auto res_2d = make_decorator(get_result_using_2d)(numbers, days);
    auto res_1d = make_decorator(get_result_using_1d)(numbers, days);
    auto res_1d_impr = make_decorator(get_result_using_1d_memory_improved)(numbers, days);

    if (days < naive_day_limit){
        auto res_naive_iteration = make_decorator(get_naive_simulation_result)(numbers, days);
    }
    if (days < naive_recurse_day_limit){
        auto res_recurse = make_decorator(get_naive_recurse_result)(numbers, days);
    }
    
    return 0;
}
