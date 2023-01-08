#include <iostream>
#include <fstream>
#include <queue>
#include <vector>

int main() 
{
    auto input = std::ifstream("input1.txt");

    std::priority_queue<int> p;
    int cal = 0;
    for( std::string line; getline( input, line ); )
    {
        if (line == ""){
            p.push(cal);
            cal = 0;
        }else{
            cal = cal + stoi(line);
        }
    }
    int res = p.top();
    p.pop();res += p.top();p.pop();res += p.top();

    std::cout << res << std::endl;
    return 0;
}
