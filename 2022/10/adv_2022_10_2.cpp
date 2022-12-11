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

void printResult(std::queue<int>& commands);

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
    printResult(commands);
    // std::cout << getResult(commands) << std::endl;
    return 0;
}

void printResult(std::queue<int>& commands){
    std::set<int> cycles = {40,80,120,160,200,240};
    int position = 1;
    char CRT[6][40];
    // 1-40
    // 41-80
    //
    // 201 - 240

    int cycle = 1;

    while(!commands.empty()){
        
        //start
        int top = commands.front();
        commands.pop();

        // during
        if(cycle%40 == position || cycle%40 == position + 1 || cycle%40 == position + 2){
            CRT[(int)(cycle/40)][cycle%40] = 'X';
        }
        else{
            CRT[(int)(cycle/40)][cycle%40] = '.';
        }

        //end
        cycle++;
        position += top;
    }
    for(int i = 0; i < 6; i++){
        for(int j = 0; j < 40; j++){
            cout << CRT[i][j];
        }

        cout << endl;

    }
}

// noop
// 1. start ==> begins execution, during still 1, after the first cycle, noop do nothing

// addx 3
// 1. start ==>  addx 3 begin execution, during X still 1
// 2.       ==> during X still 1, after addx 3 finished execution, X == 4
// 3  start == > begin execution addx/noop, during X == 4
