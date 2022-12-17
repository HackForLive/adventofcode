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
int getResult(vector<vector<char>>& map);
int getResult2(vector<vector<char>>& map, int n);
vector<int> getPositionOfCharacter(vector<vector<char>>& map, char character);
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
    // cout << start[0] << ' ' << start[1] << endl;
    // cout << end[0] << ' ' << end[1] << endl;

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
    auto input = std::ifstream("input.txt");
    int n = 1000;
    
    vector<vector<char>> map = createMap(n);

    for( std::string line; getline( input, line ); ){
        drawRockPath(map, line);
    }
    
    std::cout << getResult2(map, n) << std::endl;
    print2DVector(map);
    return 0;
}

bool checkIfFree(vector<vector<char>>& map, const vector<int>& spot){
    // cout << spot[0] << ' ' << spot[1] << endl;
    if(map.size() <= spot[0] || map[0].size() <= spot[1])return false;

    if(map[spot[0]][spot[1]] == '.') return true;
    return false;
}

bool dropSand(vector<vector<char>>& map, vector<int>& start){
    int infTime = 400;
    int time = 0;
    vector<vector<int>> dxy = {{1,0},{1,-1},{1,1}};
    vector<int> last = {start[0], start[1]};
    bool changed = false;
    while(time < infTime){
        time++;
        changed = false;
        for(const auto &d : dxy){
            vector<int> tmp = {last[0] + d[0],last[1] + d[1]};
            if(checkIfFree(map, tmp)){
                last = tmp;
                changed = true;
                break;
            }
        }
        if(!changed){
            if (map[last[0]][last[1]] == 'o'){
                return false;
            }
            map[last[0]][last[1]] = 'o';    
            // print2DVector(map);
            return true;
        }
    }
    return false;
}

int getResult(vector<vector<char>>& map){
    vector<int> start = {0, 500};
    map[start[0]][start[1]] = '+';
    int rest = 0;
    while(dropSand(map, start))rest++;
    return rest;
}

int getResult2(vector<vector<char>>& map, int n){
    vector<int> start = {0, 500};
    int lastY = getPositionOfCharacter(map, '#')[0];
    int inftyLineY = lastY + 2;
    drawRockPath(map, "0," + to_string(inftyLineY)+ " -> " + to_string(n) + "," + to_string(inftyLineY));
    map[start[0]][start[1]] = '+';
    int rest = 0;
    while(dropSand(map, start))rest++;
    return rest;
}



void print2DVector(vector<vector<char>>& values){
    for (int i = 0; i < 13; i++){
        for (int j = 485; j < 520; j++){
            cout << values[i][j] << ' ';
        }
        cout << endl;
    }
}

vector<int> getPositionOfCharacter(vector<vector<char>>& map, char character){
    vector<int> last = {-1,-1};
    for (int i = 0; i < map.size(); i++)
        for (int j = 0; j < map[i].size(); j++)
            if(map[i][j] == character)
                last = vector<int> {i , j};

    if( last[0] == -1 ){
        throw std::invalid_argument("Start character was not found.");
    }
    return last;
}
