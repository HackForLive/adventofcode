#include <iostream>
#include <fstream>
#include <sstream>
#include <set>
#include <queue>
#include <vector>
#include <unordered_map>
#include <algorithm>

#include <boost/algorithm/string.hpp>

using namespace std;

//
// How to build
//
//  g++ -o adv_2022_15 adv_2022_15.cpp -I /path_to/boost_1_80_0
//

void printChamber(std::vector<char>& chamber, int& chamberWidth);
void moveRight(vector<vector<int>>& pattern, std::vector<char>& chamber, vector<int>& position, int& chamberWidth);
void moveLeft(vector<vector<int>>& pattern, std::vector<char>& chamber, vector<int>& position, int& chamberWidth);
void moveDown(vector<vector<int>>& pattern, std::vector<char>& chamber, vector<int>& position, int& chamberWidth);
bool canMoveRight(vector<vector<int>>& pattern, std::vector<char>& chamber, vector<int>& position, int& chamberWidth);
bool canMoveLeft(vector<vector<int>>& pattern, std::vector<char>& chamber, vector<int>& position, int& chamberWidth);
bool canMoveDown(vector<vector<int>>& pattern, std::vector<char>& chamber, vector<int>& position, int& chamberWidth);
int simulationRound(std::vector<char>& chamber, std::unordered_map<int, vector<vector<int>>>& order, 
                    std::vector<char>& jetPattern, int& jetIndex, int& round, int& maxH);
void fallPattern(vector<vector<int>>& pattern, std::vector<char>& chamber, char& jet, vector<int>& position, int& chamberWidth);
int simulation(std::vector<char>& chamber, std::vector<char>& jetPattern, int& rounds);
int getResult(vector<char>& jetPattern);

int main() 
{
    auto input = std::ifstream("input.txt");
    
    vector<int> mins = {INT_MAX, INT_MAX};
    vector<int> maxs = {INT_MIN, INT_MIN};

    vector<char> jetPattern;

    for( std::string line; getline( input, line ); ){
        for(const auto &c : line){
            jetPattern.push_back(c);
        }
    }

    cout << getResult(jetPattern) << endl;
    return 0;
}

// The tall, vertical chamber is exactly seven units wide. Each rock appears so
// that its left edge is two units away from the left wall and its bottom edge is 
// three units above the highest rock in the room (or the floor, if there isn't one).

// After a rock appears, it alternates between being pushed by a jet of hot gas one unit 
// (in the direction indicated by the next symbol in the jet pattern) and then falling one unit down.

// ####

// .#.
// ###
// .#.

// ..#
// ..#
// ###

// #
// #
// #
// #

// ##
// ##
int getResult(vector<char>& jetPattern){

    int chamberWidth = 7;
    // int rounds = 2022;
    int rounds = 2022;
    int row = rounds*10;
    
    std::vector<char> chamber(chamberWidth * row, '.');
    for(int j = 0; j < chamberWidth; j++){
        chamber[j] = '#';
    }

    int res = simulation(chamber, jetPattern, rounds);

    return res;
}

bool canMoveRight(vector<vector<int>>& pattern, std::vector<char>& chamber, vector<int>& position, int& chamberWidth){
    for( const auto &point : pattern){
        int y = position[0] - point[0];
        int x = point[1] + position[1];
        // bad <<< check only others
        if(x + 1 < chamberWidth && 
          (chamber[y*chamberWidth + x + 1] == '.' || chamber[y*chamberWidth + x + 1] == '@')){
            continue;
        }
        else{
            return false;
        }
    }
    return true;
}

bool canMoveLeft(vector<vector<int>>& pattern, std::vector<char>& chamber, vector<int>& position, int& chamberWidth){
    for( const auto &point : pattern){
        int y = position[0] - point[0];
        int x = point[1] + position[1];
        if(x - 1 >= 0 && 
           (chamber[y*chamberWidth + x - 1] == '.' || chamber[y*chamberWidth + x - 1] == '@')){
            continue;
        }
        else{
            return false;
        }
    }
    return true;
}

bool canMoveDown(vector<vector<int>>& pattern, std::vector<char>& chamber, vector<int>& position, int& chamberWidth){
    for( const auto &point : pattern){
        int y = position[0] - point[0];
        int x = point[1] + position[1];
        if(y - 1 >= 0 &&
           (chamber[(y-1)*chamberWidth + x] == '.' || chamber[(y-1)*chamberWidth + x] == '@')){
            continue;
        }
        else{
            return false;
        }
    }
    return true;
}

void moveRight(vector<vector<int>>& pattern, std::vector<char>& chamber, vector<int>& position, int& chamberWidth){
    for( const auto &point : pattern){
        int y = position[0] - point[0];
        int x = point[1] + position[1];
        chamber[y*chamberWidth + x] = '.';
        chamber[y*chamberWidth + x + 1] = '@';
    }
    position[1] = position[1] + 1;
}
void moveLeft(vector<vector<int>>& pattern, std::vector<char>& chamber, vector<int>& position, int& chamberWidth){
    for( const auto &point : pattern){
        int y = position[0] - point[0];
        int x = point[1] + position[1];
        chamber[y*chamberWidth + x] = '.';
        chamber[y*chamberWidth + x - 1] = '@';
    }
    position[1] = position[1] - 1;
}
void moveDown(vector<vector<int>>& pattern, std::vector<char>& chamber, vector<int>& position, int& chamberWidth){
    for( const auto &point : pattern){
        int y = position[0] - point[0];
        int x = point[1] + position[1];
        chamber[y*chamberWidth + x] = '.';
        chamber[(y-1)*chamberWidth + x] = '@';
    }
    position[0] = position[0] - 1;
}

// by jet, then down
void fallPattern(vector<vector<int>>& pattern, std::vector<char>& chamber, char& jet, vector<int>& position, int& chamberWidth){

    if(jet == '>' && canMoveRight(pattern, chamber, position, chamberWidth)){
        moveRight(pattern, chamber, position, chamberWidth);
    }
    else if(jet == '<' && canMoveLeft(pattern, chamber, position, chamberWidth)){
        moveLeft(pattern, chamber, position, chamberWidth);
    }
    // else{
    //     throw std::invalid_argument("Jet character was not recognized." + jet);
    // }

    if(canMoveDown(pattern, chamber, position, chamberWidth)){
        moveDown(pattern, chamber, position, chamberWidth);
    }
}

int simulation(std::vector<char>& chamber, std::vector<char>& jetPattern, int& rounds){
    vector<vector<int>> first = {{0,0},{0,1},{0,2},{0,3}};
    vector<vector<int>> second = {{0,1},{1,0},{1,1},{1,2},{2,1}};
    vector<vector<int>> third = {{0,2},{1,2},{2,2},{2,1},{2,0}};
    vector<vector<int>> fourth = {{0,0},{1,0},{2,0},{3,0}};
    vector<vector<int>> fifth = {{0,0},{1,0},{0,1},{1,1}};

    std::unordered_map<int, vector<vector<int>>> order;

    order[0] = first;
    order[1] = second;
    order[2] = third;
    order[3] = fourth;
    order[4] = fifth;

    int maxH = 0;
    int round = 0;
    int jetIndex = 0;
    int currentH = maxH;

    while ( round < rounds ){
        currentH  = simulationRound(chamber, order, jetPattern, jetIndex, round, maxH);
        if(currentH > maxH){
            maxH = currentH;
        }
        round++;
    }

    return maxH;
}

///
/// top left position
///
vector<int> getPosition(vector<vector<int>> &pattern, int& maxH){
    int height = 3;
    
    int minY = INT_MAX;
    int maxY = INT_MIN;
    for(const auto& point : pattern){
        if(point[0] > maxY){
            maxY = point[0];
        }
        if(point[0] < minY){
            minY = point[0];
        }
    }

    return {maxY-minY+height+maxH+1,2};
}

void setupPattern(vector<int>& position, vector<vector<int>> &pattern, std::vector<char>& chamber, int& chamberWidth){
    for(const auto& point : pattern){
        // int x = point[1] + position[1];
        // int y = point[0] + position[0];
        int x = position[1] + point[1];
        int y = position[0] - point[0];
        chamber[y*chamberWidth + x] = '@';
    }
}

void finishPattern(vector<int>& position, vector<vector<int>> &pattern, std::vector<char>& chamber, int& chamberWidth){
    for(const auto& point : pattern){
        // int x = point[1] + position[1];
        // int y = point[0] + position[0];
        int x = position[1] + point[1];
        int y = position[0] - point[0];
        chamber[y*chamberWidth + x] = '#';
    }
}

int simulationRound(std::vector<char>& chamber, std::unordered_map<int, vector<vector<int>>>& order, 
                    std::vector<char>& jetPattern, int& jetIndex, int& round, int& maxH){

    int currentH = 0;
    int jetLen = jetPattern.size();
    int orderLen = order.size();
    int chamberWidth = 7;

    vector<int> position = getPosition(order[round%orderLen], maxH);
    setupPattern(position, order[round%orderLen], chamber, chamberWidth);
    while (true) {
        printChamber(chamber, chamberWidth);
        cout << position[1] << ":x, " << position[0] << ":y" << endl;
        currentH = position[0];
        fallPattern(order[round%orderLen], chamber, jetPattern[jetIndex%jetLen], position, chamberWidth);
        
        cout << "--------------" << endl;
        // cout << position[1] << ":x, " << position[0] << ":y" << endl;
        cout << currentH << endl;
        
        // cout << jetPattern[jetIndex%jetLen] << endl;
        cout << "--------------" << endl;
        jetIndex++;
        if(currentH == position[0]){
            finishPattern(position, order[round%orderLen], chamber, chamberWidth);
            printChamber(chamber, chamberWidth);

            break;
        }
    }
    if(currentH > maxH){
        maxH = currentH;
    }

    return currentH;
}

void printChamber(std::vector<char>& chamber, int& chamberWidth){

    // int height = 15;
    // for(int i = 0; i < height*chamberWidth; i+= chamberWidth){
    //     for(int j = i; j < i+chamberWidth; j++){
    //         cout << chamber[j];
    //     }
    //     cout << endl;
    // }

    int height = 15;
    for(int i = height*chamberWidth-1; i >=0; i-= chamberWidth){
        for(int j = i-chamberWidth+1; j <= i; j++){
            cout << chamber[j];
        }
        cout << endl;
    }
}