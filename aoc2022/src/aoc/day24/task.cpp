#include <memory>
#include <vector>
#include <array>
#include <iostream>
#include <fstream>
#include <sstream>

enum grid_element_type {
    wall = 0, blizzard = 1, player = 2, free = 4, start = 8, end = 16
};


struct position {
    int x;
    int y;

    position() : x(-1), y(-1) {};
    position(int x, int y) { this->x = x; this->y = y; };
};

struct direction
{
    static position up;
    static position down;
    static position right;
    static position left;
    static position none;

    direction() {
        this->up = position(0,-1);
        this->down = position(0,1);
        this->right = position(1,0);
        this->left = position(-1,0);
        this->none = position(0,0);
    };
};

struct grid_element {
    grid_element_type type = grid_element_type::free;
    position pos;
    position dir;

    grid_element() {
        this->type = type;
        this->pos = position();
        this->dir = direction::none;
    };

    grid_element(grid_element_type type, position pos, position dir) {
        this->type = type;
        this->pos = pos;
        this->dir = dir;
    };
};

class grid_layout {
    public:
        const static int ROW = 22;
        const static int COL = 152;
        std::shared_ptr<std::array<std::array<int, COL>, ROW>> grid;

        std::shared_ptr<std::vector<grid_element>> blizzards;
        grid_element player;

        grid_layout(){};
};

int main(){

    // list of blizzards

    

    std::shared_ptr<grid_layout> grid_layout_ptr = parse_input();



    // row/col 22/152

    return 0;
}

std::shared_ptr<grid_layout> parse_input(){
    auto input = std::ifstream("adventofcode/aoc2022/src/aoc/day24/in.txt");

    grid_layout grid_l;

    for( std::string line; getline( input, line ); ){

        for(auto& c : line){
            if(c == '.'){

            }
            else if (c == '#') {

            }
            else if (c == '<'){

            }
            else if (c == '>'){

            }
            else if (c == '^'){
                
            }
            else if (c == 'v'){
                
            }
            else{
                throw std::runtime_error("unexpected grid element");
            }
        }
    }
}

int bfs(){

}

void get_map(){

}

int get_result(){

}