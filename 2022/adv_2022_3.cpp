#include <iostream>
#include <fstream>
#include <set>
#include <vector>
#include <algorithm>

// Lowercase item types a through z have priorities 1 through 26.
// Uppercase item types A through Z have priorities 27 through 52.

bool isLowerCase(char &a);
int main() 
{
    auto input = std::ifstream("input3.txt");

    int res = 0;
    for( std::string line; getline( input, line ); )
    {
        std::set<char> f;
        std::set<char> s;

        //std::cout << (int)'a' << (int)'z' << (int)'A' << (int)'Z'<< std::endl;
        // 97 122 65 90
        for(int i = 0; i < line.length()/2; i++){
            f.insert(line[i]);
        }
        for(int i = line.length()/2; i < line.length(); i++){
            s.insert(line[i]);
        }

        std::set<char> intersect;
        std::set_intersection(f.begin(), f.end(), s.begin(),s.end(), std::inserter(intersect, intersect.begin()));

        auto oneMove = *(intersect.begin());
        if(isLowerCase(oneMove)){
            res = res + (int)oneMove - (int)'a' + 1;
        }
        else{
            res = res + (int)oneMove - (int)'A' + 27;
        }
    }
    std::cout << res << std::endl;
    return 0;
}

bool isLowerCase(char &a){
    if((int)a - (int)'a' >= 0){
        return true;
    }
    return false;
}
