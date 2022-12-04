#include <iostream>
#include <fstream>
#include <set>
#include <vector>
#include <algorithm>

#include <boost/algorithm/string.hpp>

#include "range.hpp"

//
// How to build
//
//  g++ -o adv_2022_4 adv_2022_4.cpp range.cpp -I /path_to/boost_1_80_0
//


bool getResult(std::string& line);
Range getRange(std::string& line);
bool IsFullyOverlappingIntervals(Range a, Range b);

int main() 
{
    auto input = std::ifstream("input4.txt");

    int res = 0;
    for( std::string line; getline( input, line ); )
        if(getResult(line)) res++;
    
    std::cout << res << std::endl;
    return 0;
}

bool getResult(std::string& line){
    std::vector<std::string> results;

    boost::split(results, line, [](char c){return c == ',';});

    Range a = getRange(results[0]);
    Range b = getRange(results[1]);

    return IsFullyOverlappingIntervals(a,b);
}

Range getRange(std::string& line){
    std::vector<std::string> results;

    boost::split(results, line, [](char c){return c == '-';});
    return Range(stoi(results[0]),stoi(results[1]));
}

bool IsFullyOverlappingIntervals(Range a, Range b){

    if(a.getStart() <= b.getStart() && b.getEnd() <= a.getEnd()){
        return true;
    }
    else if(b.getStart() <= a.getStart() && a.getEnd() <= b.getEnd()){
        return true;
    }

    return false;
}