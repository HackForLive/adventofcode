#include <iostream>
#include <fstream>
#include <set>
#include <queue>
#include <vector>
#include <algorithm>

#include <boost/algorithm/string.hpp>

using namespace std;

//
// How to build
//
//  g++ -o adv_2022_10 adv_2022_10.cpp range.cpp -I /path_to/boost_1_80_0
//
void print_queue(std::queue<int> q)
{
  while (!q.empty())
  {
    std::cout << q.front() << " ";
    q.pop();
  }
  std::cout << std::endl;
}

int getResult(std::queue<int>& commands);

int main() 
{
    auto input = std::ifstream("input10.txt");
    
    std::queue<int> commands;
    for( std::string line; getline( input, line ); ){
        std::vector<std::string> results;
        boost::split(results, line, [](char c){return c == ' ';});

        std::string action = results[0];
        if (action == "noop"){
            commands.push(0);
        }
        else{
            int value = stoi(results[1]);
            commands.push(0);
            commands.push(value);
        }
    }
    
    std::cout << getResult(commands) << std::endl;
    return 0;
}

int getResult(std::queue<int>& commands){
    std::set<int> cycles = {20,60,100,140,180,220};

    int cycle = 1;
    int current = 1;
    int result = 0;

    while(!commands.empty()){
        
        int top = commands.front();
        commands.pop();
        
        const bool is_in = cycles.find(cycle) != cycles.end();

        if(is_in){
            result += current * cycle;
            // cout << result << endl;
        }
        cycle++;
        current += top;
    }
    return result;
}

// noop
// 1. start ==> begins execution, during still 1, after the first cycle, noop do nothing

// addx 3
// 1. start ==>  addx 3 begin execution, during X still 1
// 2.       ==> during X still 1, after addx 3 finished execution, X == 4
// 3  start == > begin execution addx/noop, during X == 4