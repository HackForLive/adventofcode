#include <iostream>
#include <fstream>
#include <set>
#include <stack>

int main() 
{
    int counter = 1;
    char ch;
    std::set<char> f;
    std::stack<char> st;
    std::fstream fin("input6.txt", std::fstream::in);
    while (fin >> std::noskipws >> ch) {
        st.push(ch);
         if(f.find(ch) != f.end()){
            f.clear();
            while(!st.empty()) {
                char curr = st.top();
                f.insert(curr);
                st.pop();
                if(curr == ch)
                    break;
            }
         }
         else{
            f.insert(ch);
         }
         if(f.size() == 4)
            break;
         counter++;
    }
    std::cout << counter << std::endl;
    return 0;
}
