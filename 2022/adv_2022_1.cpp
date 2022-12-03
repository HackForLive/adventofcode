#include <iostream>
#include <fstream>

int main() 
{
    auto input = std::ifstream("input1.txt");

    int cal = 0;
    int max = 0;
    for( std::string line; getline( input, line ); )
    {
        cal = (line == "") ? 0 : cal + stoi(line);
        max = cal > max ? cal : max;
    }
    std::cout << max << std::endl;
    return 0;
}
