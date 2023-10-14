// Model growth of Lantern Fish
#include <iostream>
#include <fstream>
#include <vector>
#include <array>
#include <sstream>
#include <ctime>
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
    auto input = std::ifstream("test.txt");

    for( std::string line; getline( input, line ); ){
        return take_int(line);
    }
}

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
    return inputs.size();
}

long get_result_using_2d(std::vector<int> & start_lanternfish_numbers, int days = 80){

    const int states_n = 9;
    long  matrix[states_n][300];
    for(int i = 0; i < states_n; i++){
        // sub optimal
        matrix[i][0] = 1;
    }

    for(int i = 1; i < days; i++){
        for(int j = states_n -1; j >= 0; j--){
            if (j == 0) {
                matrix[j][i] = matrix[6][i-1] + matrix[8][i-1];
            }else{
                matrix[j][i] = matrix[j-1][i-1];
            }
        }
    }

    long res = 0;
    for(const auto& num : start_lanternfish_numbers){
        res = res + matrix[0][days-num];
    }

    return res;
}


long get_result_using_1d(std::vector<int> & start_lanternfish_numbers, int days = 80){

    // shift array
    const int start_index = 9;
    // precompute first entries
    long matrix[300] = {1, 2, 2, 2, 2, 2, 2, 2, 3};

    for(int i = start_index; i < days; i++)
        matrix[i] = matrix[i-start_index+2] + matrix[i-start_index];

    long res = 0;
    for(const auto& num : start_lanternfish_numbers){
        res = res + matrix[days-num];
    }

    return res;
}

int main(int argc, char* argv[]){
    if (argc < 2){
        std::cout << "Missing days parameter!" << std::endl;
        return 1;
    }

    int days = std::stoi(argv[1]);
    
    std::vector<int> numbers = read_test_input();\
    auto res_2d = make_decorator(get_result_using_2d)(numbers, days);
    auto res_1d = make_decorator(get_result_using_1d)(numbers, days);
    std::cout << "Using 1D array:" << res_1d << std::endl;
    std::cout << "Using 2D array:" << res_1d << std::endl;
    
    return 0;
}

