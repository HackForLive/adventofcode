#include <iostream>
#include <fstream>
#include <sstream>
#include <set>
#include <queue>
#include <vector>
#include <algorithm>

#include <boost/algorithm/string.hpp>

using namespace std;

//
// How to build
//
//  g++ -o adv_2022_15 adv_2022_15.cpp -I /path_to/boost_1_80_0
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

void print2DVector(vector<vector<char>>& values);
int readHashes(vector<vector<int>>& intervals,vector<vector<int>>& s, vector<vector<int>>& b, int& y);
vector<vector<int>> getUpdatedIntervals(vector<vector<int>> actual);
bool isIntervalOverlapping(vector<int>& A, vector<int>& B);
vector<int> mergeIntervals(vector<int>& A, vector<int>& B);
vector<int> expandS(vector<int>& S, vector<int>& B, int& y);
int getManhattonDistance(vector<int>& s, vector<int>& b);
vector<int> getNumbersFromInputLine(const string& line);
int getResult(vector<vector<int>>& s, vector<vector<int>>& b);

vector<int> getNumbersFromInputLine(const string& line) {
    vector<int> numbers;

    std::vector<std::string> results;
    boost::split(results, line, [](char c){return c == '=';});

    std::vector<std::string> resultsV;
    // Sx
    boost::split(resultsV, results[1], [](char c){return c == ',';});
    numbers.push_back(stoi(resultsV[0]));
    // Bclosestx
    boost::split(resultsV, results[3], [](char c){return c == ',';});
    numbers.push_back(stoi(resultsV[0]));

    // Sy
    boost::split(resultsV, results[2], [](char c){return c == ':';});
    numbers.push_back(stoi(resultsV[0]));
    numbers.push_back(stoi(results[4]));
    // Bclosesty
    return numbers;
}

int main() 
{
    auto input = std::ifstream("input.txt");
    
    // y,x
    vector<int> mins = {INT_MAX, INT_MAX};
    vector<int> maxs = {INT_MIN, INT_MIN};

    vector<int> vec;
    vector<int> vecS;
    vector<int> vecB;
    vector<vector<int>> vecBs;
    vector<vector<int>> vecSs;

    for( std::string line; getline( input, line ); ){
        vec = getNumbersFromInputLine(line);
        vecS = {vec[2],vec[0]};
        vecB = {vec[3],vec[1]};
        vecBs.push_back(vecB);
        vecSs.push_back(vecS);
    }

    // cout << mins[0] << ' ' << mins[1] << endl;
    // cout << maxs[0] << ' ' << maxs[1] << endl;

    cout << getResult(vecSs, vecBs) << endl;
    return 0;
}

int getManhattonDistance(vector<int>& s, vector<int>& b){
    return abs(s[0]-b[0]) + abs(s[1]-b[1]);
}

int getResult(vector<vector<int>>& s, vector<vector<int>>& b){
    int y = 2000000;
    vector<int> S,B;
    vector<vector<int>> intervals = {};
    for(int i = 0; i < s.size(); i++){
        S = {s[i][0], s[i][1]};
        B = {b[i][0], b[i][1]};
        
        vector<int> interTmp = expandS(S, B, y);
        if(interTmp.size() > 0){
            intervals.push_back(interTmp);
            intervals = getUpdatedIntervals(intervals);
        }
    }
    intervals = getUpdatedIntervals(intervals);
    return readHashes(intervals, s,b,y);
}

int readHashes(vector<vector<int>>& intervals,vector<vector<int>>& s, vector<vector<int>>& b, int& y){
    int res = 0;
    set<vector<int>> set_of_b_vector;

    for(int i = 0; i < b.size(); i++){
        set_of_b_vector.insert(b[i]);
    }

    for(int i = 0; i < intervals.size(); i++){
        res += intervals[i][1] - intervals[i][0] + 1;
        for(int j = 0; j < s.size(); j++){
            if(s[j][0] == y && s[j][1] >= intervals[i][0] && s[j][1] <= intervals[i][1]) res--;
        }
        for(const auto b_v : set_of_b_vector){
            if(b_v[0] == y && b_v[1] >= intervals[i][0] && b_v[1] <= intervals[i][1]) res--;
        }
    }
    return res;
}

vector<vector<int>> getUpdatedIntervals(vector<vector<int>> actual){
    if(actual.size()==1){return actual;}

    vector<vector<int>> updated;
    for(int i = 0; i < actual.size(); i++){
        vector<int> merged = {};
        for(int j = i + 1; j < actual.size(); j++){

            auto l = actual[i];
            auto r = actual[j];
            if(isIntervalOverlapping(l, r)){
                merged = mergeIntervals(l, r);
                actual[i] = merged;
                actual[j] = merged;
            }
        }
        if(i == actual.size() - 2 && merged.size() > 0){
            updated.push_back(merged);
            break;
        }
        if(merged.size() == 0){
            updated.push_back(actual[i]);
        }
    }
    return updated;
}

bool isIntervalOverlapping(vector<int>& A, vector<int>& B){
    if(A[0] > B[1]) return false;
    if(B[0] > A[1]) return false;
    return true;
}

vector<int> mergeIntervals(vector<int>& A, vector<int>& B){
    return {min(A[0],B[0]), max(A[1],B[1])};
}

vector<int> expandS(vector<int>& S, vector<int>& B, int& y){
    int manD = getManhattonDistance(S,B);
    int diff = manD - abs(S[0] - y);

    if (diff < 0){
        return {};
    }
    else if (diff == 0){
        return {S[1],S[1]};
    }
    else{
        return {S[1] - diff, S[1] + diff};
    }
}
