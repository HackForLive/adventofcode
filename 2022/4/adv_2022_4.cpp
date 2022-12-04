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
bool getResult2(std::string& line);
Range getRange(std::string& line);
bool IsFullyOverlappingIntervals(Range& a, Range& b);
bool IsOverlappingIntervals(Range& a, Range& b);

int main() 
{
    auto input = std::ifstream("input4.txt");

    int res = 0;
    for( std::string line; getline( input, line ); )
        if(getResult2(line)) res++;
    
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


bool getResult2(std::string& line){
    std::vector<std::string> results;

    boost::split(results, line, [](char c){return c == ',';});

    Range a = getRange(results[0]);
    Range b = getRange(results[1]);

    return IsOverlappingIntervals(a,b);
}

Range getRange(std::string& line){
    std::vector<std::string> results;

    boost::split(results, line, [](char c){return c == '-';});
    return Range(stoi(results[0]),stoi(results[1]));
}

bool IsFullyOverlappingIntervals(Range& a, Range& b){

    if(a.getStart() <= b.getStart() && b.getEnd() <= a.getEnd()){
        return true;
    }
    else if(b.getStart() <= a.getStart() && a.getEnd() <= b.getEnd()){
        return true;
    }

    return false;
}

bool IsOverlappingIntervals(Range& a, Range& b){
    // a1 b1 a2 b2
    // b1 a1 a2 b2
    if(a.getStart() < b.getStart() && a.getEnd() < b.getStart()){
        // a1 b1
        return false;
    }
    else if(b.getStart() < a.getStart() && b.getEnd() < a.getStart()){
        return false;
    }

    return true;
}