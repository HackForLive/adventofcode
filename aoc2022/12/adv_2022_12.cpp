#include <iostream>
#include <fstream>
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

vector<int> getPositionOfCharacter(vector<vector<char>>& map, char character);
vector<int> getStartPosition(vector<vector<char>>& map);
vector<int> getEndPosition(vector<vector<char>>& map);
vector<vector<bool>> getVisitedMap(vector<vector<char>>& map);
vector<vector<int>> getValueMap(vector<vector<char>>& map);
int getResult(vector<vector<char>>& map);
int DFS(vector<vector<char>>& map, vector<int>& start, vector<int>& end);
int DFS2(vector<vector<char>>& map, vector<int>& start, vector<int>& end);

int main() 
{
    auto input = std::ifstream("input.txt");
    
    vector<vector<char>> map;

    for( std::string line; getline( input, line ); ){
        vector<char> row;
        for(char a : line){
            row.push_back(a);
        }
        map.push_back(row);
    }
    
    std::cout << getResult(map) << std::endl;
    return 0;
}

void print2DVector(vector<vector<int>>& values){
    for (int i = 0; i < values.size(); i++){
        for (int j = 0; j < values[i].size(); j++){
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

vector<int> getStartPosition(vector<vector<char>>& map){
    return getPositionOfCharacter(map, 'S');
}

vector<int> getEndPosition(vector<vector<char>>& map){
    return getPositionOfCharacter(map, 'E');
}


int getResult(vector<vector<char>>& map){
    vector<int> end = getEndPosition(map);
    vector<int> start = getStartPosition(map);

    return DFS2(map, end, start);
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

int DFS(vector<vector<char>>& map, vector<int>& start, vector<int>& end){

    int rows = map.size();
    int columns = map[0].size();

    vector<vector<int>> dxy = { {1, 0}, {0, -1}, {-1, 0}, {0, 1} };
    std::queue<vector<int>> nodes;
    vector<vector<bool>> visited = getVisitedMap(map);
    vector<vector<int>> values = getValueMap(map);

    nodes.push(start);
    map[start[0]][start[1]] = 'a';
    map[end[0]][end[1]] = 'z';
    values[start[0]][start[1]] = 0;

    while(!nodes.empty()){
        auto node = nodes.front();
        nodes.pop();
        // visited
        // cout << node[0] << " " << node[1] << endl;
        if(visited[node[0]][node[1]] == true) continue;
        //if(map[node[0]][node[1]] == map[end[0]][end[1]]) break;

        for (auto const & d : dxy){
            vector<int> tmp = {node[0] + d[0], node[1] + d[1]};
            if (tmp[0] >= 0 && tmp[0] < rows && tmp[1] >= 0 && tmp[1] < columns && 
            ((int)map[tmp[0]][tmp[1]] - (int)map[node[0]][node[1]] <= 1)){
                
                nodes.push(tmp);
                if (values[tmp[0]][tmp[1]] == 0 || values[tmp[0]][tmp[1]] > values[node[0]][node[1]] + 1){
                    values[tmp[0]][tmp[1]] = values[node[0]][node[1]] + 1;
                }
            }
        }
        if(map[node[0]][node[1]] == map[end[0]][end[1]]) break;
        visited[node[0]][node[1]] = true;
    }
    print2DVector(values);
    return values[end[0]][end[1]];
    // 6530 too high
}

int DFS2(vector<vector<char>>& map, vector<int>& start, vector<int>& end){

    int rows = map.size();
    int columns = map[0].size();

    vector<vector<int>> dxy = { {1, 0}, {0, -1}, {-1, 0}, {0, 1} };
    std::queue<vector<int>> nodes;
    vector<vector<bool>> visited = getVisitedMap(map);
    vector<vector<int>> values = getValueMap(map);

    nodes.push(start);
    map[start[0]][start[1]] = 'z';
    map[end[0]][end[1]] = 'a';
    values[start[0]][start[1]] = 0;

    while(!nodes.empty()){
        auto node = nodes.front();
        nodes.pop();
        // visited
        // cout << node[0] << " " << node[1] << endl;
        if(visited[node[0]][node[1]] == true) continue;
        //if(map[node[0]][node[1]] == map[end[0]][end[1]]) break;

        for (auto const & d : dxy){
            vector<int> tmp = {node[0] + d[0], node[1] + d[1]};
            if (tmp[0] >= 0 && tmp[0] < rows && tmp[1] >= 0 && tmp[1] < columns && 
            ((int)map[node[0]][node[1]] - (int)map[tmp[0]][tmp[1]] <= 1)){
                
                nodes.push(tmp);
                if (values[tmp[0]][tmp[1]] == 0 || values[tmp[0]][tmp[1]] > values[node[0]][node[1]] + 1){
                    values[tmp[0]][tmp[1]] = values[node[0]][node[1]] + 1;
                }
            }
        }
        if(map[node[0]][node[1]] == 'a') {
            return values[node[0]][node[1]];
        }
        visited[node[0]][node[1]] = true;
    }
    print2DVector(values);
    return values[end[0]][end[1]];
    // 6530 too high
}