#include <iostream>
#include <fstream>
#include <set>
#include <vector>
#include <algorithm>

// Lowercase item types a through z have priorities 1 through 26.
// Uppercase item types A through Z have priorities 27 through 52.
int getPoints(char &a);
bool isLowerCase(char &a);
char getBadge(std::string group1, std::string group2, std::string group3);
int main() 
{
    auto input = std::ifstream("input3.txt");

    int result = 0;
    std::string group1, group2, group3; 
    while(getline(input, group1) && getline(input, group2) && getline(input, group3))
    {  
        char badge = getBadge(group1, group2, group3);
        result = result + getPoints(badge);
    }
    std::cout << result << std::endl;
    return 0;
}

char getBadge(std::string group1, std::string group2, std::string group3){
    // 'z' => 122
    const int LEN = 123;
    int g1[LEN] = { 0 };
    int g2[LEN] = { 0 };
    int g3[LEN] = { 0 };

    for(char c : group1) {
        if(g1[(int)c] == 0) g1[(int)c] = 1;
    }
    for(char c : group2) {
        if(g2[(int)c] == 0) g2[(int)c] = 1;
    }
    for(char c : group3) {
        if(g3[(int)c] == 0) g3[(int)c] = 1;
    }

    for(int i = 0; i < LEN; i++){
        if(g1[i] == 1 && g2[i] == 1 && g3[i] == 1){
            return (char)i;
        }
    }

    throw std::invalid_argument( "no badge found" );
}

int getPoints(char &a){
     return isLowerCase(a) ? (int)a - (int)'a' + 1: (int)a - (int)'A' + 27;
}

bool isLowerCase(char &a){
    if((int)a - (int)'a' >= 0){
        return true;
    }
    return false;
}
