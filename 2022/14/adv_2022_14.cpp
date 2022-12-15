#include <iostream>
#include <fstream>
#include <sstream>
#include <set>
#include <queue>
#include <vector>
#include <algorithm>

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

vector<vector<char>> createMap(int n);
vector<int> getNumbersFromString(string s);
void drawRockPath(vector<vector<char>>& map, vector<int>& start, vector<int>& end);
void drawRockPath(vector<vector<char>>& map, string line);
void print2DVector(vector<vector<char>>& values);
vector<string> split (string s, string delimiter);

vector<vector<char>> createMap(int n){
    
    vector<vector<char>> map;
    for (int i = 0; i < n; i++){
        vector<char> row;
        for (int j = 0; j < n; j++){
            row.push_back('.');
        }
        map.push_back(row);
    }
    return map;
}

void drawRockPath(vector<vector<char>>& map, vector<int>& start, vector<int>& end){
    cout << start[0] << ' ' << start[1] << endl;
    cout << end[0] << ' ' << end[1] << endl;

    if (start[0] == end[0]){
        for(int j = min(start[1], end[1]); j <= max(start[1], end[1]); j++){
            map[start[0]][j] = '#';
        }
    }
    else if (start[1] == end[1]){
        for(int i = min(start[0], end[0]); i <= max(start[0], end[0]); i++){
            map[i][start[1]] = '#';
        }
    }
    else{
        throw std::invalid_argument("Only vertical or horizontal paths are expected!");
    }
}

void drawRockPath(vector<vector<char>>& map, string line){
    vector<int> numbers = getNumbersFromString(line);

    vector<int> start = {numbers[1], numbers[0]};
    for(int i = 2; i < numbers.size(); i += 2){
        if(i + 1 < numbers.size()){
            vector<int> end = {numbers[i+1], numbers[i]};
            drawRockPath(map, start, end);
            start = end;
        }
    }
}

vector<int> getNumbersFromString(string s) {
    vector<int> numbers;
   
    vector<string> numParts = split(s, " -> ");
    for(const auto &part : numParts){
        vector<string> numPart = split(part, ",");
        numbers.push_back(stoi(numPart[0]));
        numbers.push_back(stoi(numPart[1]));
   }
   return numbers;
}

vector<string> split (string s, string delimiter) {
    size_t pos_start = 0, pos_end, delim_len = delimiter.length();
    string token;
    vector<string> res;

    while ((pos_end = s.find (delimiter, pos_start)) != string::npos) {
        token = s.substr (pos_start, pos_end - pos_start);
        pos_start = pos_end + delim_len;
        res.push_back (token);
    }

    res.push_back (s.substr (pos_start));
    return res;
}


int main() 
{
    auto input = std::ifstream("inputt.txt");
    
    vector<vector<char>> map = createMap(1000);

    for( std::string line; getline( input, line ); ){
        drawRockPath(map, line);
    }
    print2DVector(map);
    // std::cout << getResult(map) << std::endl;
    return 0;
}


void print2DVector(vector<vector<char>>& values){
    for (int i = 0; i < 10; i++){
        for (int j = 480; j < 508; j++){
            cout << values[i][j] << ' ';
        }
        cout << endl;
    }
}

vector<int> getPositionOfCharacter(vector<vector<char>>& map, char character){
    for (int i = 0; i < map.size(); i++)
        for (int j = 0; j < map[i].size(); j++)
            if(map[i][j] == character)
                return vector<int> {i , j};

    throw std::invalid_argument("Start character was not found.");
}

vector<vector<bool>> getVisitedMap(vector<vector<char>>& map){
    
    vector<vector<bool>> visited;
    for (int i = 0; i < map.size(); i++){
        vector<bool> row;
        for (int j = 0; j < map[i].size(); j++){
            row.push_back(false);
        }
        visited.push_back(row);
    }
    return visited;
}

vector<vector<int>> getValueMap(vector<vector<char>>& map){
    
    vector<vector<int>> visited;
    for (int i = 0; i < map.size(); i++){
        vector<int> row;
        for (int j = 0; j < map[i].size(); j++){
            row.push_back(0);
        }
        visited.push_back(row);
    }
    return visited;
}
