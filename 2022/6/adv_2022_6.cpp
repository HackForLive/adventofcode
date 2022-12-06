#include <iostream>
#include <fstream>
#include <set>
#include <vector>

int main() 
{
    int counter = 1;
    char ch;
    std::set<char> f;
    std::vector<char> vec;
    std::fstream fin("input6.txt", std::fstream::in);
    while (fin >> std::noskipws >> ch) {
         if(f.find(ch) != f.end()){
              
            f.clear();
            f.insert(ch);
            for (auto it = vec.rbegin(); it != vec.rend(); ++it)
            {
                if(*it == ch) break;
                f.insert(*it);

            }
         }
         else{
            f.insert(ch);
         }
         vec.push_back(ch);
         if(f.size() == 14)
            break;
         counter++;
    }
    std::cout << counter << std::endl;
    return 0;
}
