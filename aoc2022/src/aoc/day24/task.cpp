#include <memory>
#include <vector>
#include <queue>
#include <array>
#include <iostream>
#include <fstream>
#include <sstream>

enum grid_element_type {
    wall = 0, blizzard = 1, player = 2, none = 4, start = 8, end = 16
};


struct position {
    int x;
    int y;

    position() : x(-1), y(-1) {};
    position(int x, int y) { this->x = x; this->y = y; };

    position& operator +(const position& a)
    {
        this->x += a.x;
        this->y += a.y;
        return *this;
    }
};

struct direction
{
    position up;
    position down;
    position right;
    position left;
    position none;

    direction() {
        this->up = position(0,-1);
        this->down = position(0,1);
        this->right = position(1,0);
        this->left = position(-1,0);
        this->none = position(0,0);
    };
};

struct grid_element {
    grid_element_type type = grid_element_type::none;
    position pos;
    position dir;

    grid_element() {
        this->type = type;
        this->pos = position();
        this->dir = direction().none;
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
        grid_element start;
        grid_element end;

        grid_layout(){
            std::array<std::array<short, COL>, ROW> grid;
            this->grid = std::make_shared<std::array<std::array<int, COL>, ROW>>(grid);
        };
};

std::shared_ptr<grid_layout> parse_input();

int main(){
    return 0;
}

std::shared_ptr<grid_layout> parse_input(){
    auto input = std::ifstream("/home/michael/git/adventofcode/aoc2022/src/aoc/day24/in.txt");

    grid_layout grid_l;
    std::vector<grid_element> blizzards;
    grid_element ge;
    int row = 0;
    int col = 0;  

    for( std::string line; getline( input, line ); ){
        col = 0;

        for(auto& c : line){
            if(c == '.'){
                if(row == 0){
                    ge = grid_element(grid_element_type::start, position(col, row), direction().none);
                    grid_l.start = ge;
                }
                else if(row == grid_l.ROW-1){
                    ge = grid_element(grid_element_type::end, position(col, row), direction().none);
                    grid_l.end = ge;
                }
                (*grid_l.grid)[row][col] = 0;
                ge = grid_element(grid_element_type::none, position(col, row), direction().none);
            }
            else if (c == '#') {
                (*grid_l.grid)[row][col]=-1;
                ge = grid_element(grid_element_type::wall, position(col, row), direction().none);
            }
            else if (c == '<'){
                (*grid_l.grid)[row][col]+=1;
                ge = grid_element(grid_element_type::blizzard, position(col, row), direction().left);
                blizzards.push_back(ge);
            }
            else if (c == '>'){
                (*grid_l.grid)[row][col]+= 1;
                ge = grid_element(grid_element_type::blizzard, position(col, row), direction().right);
                blizzards.push_back(ge);
            }
            else if (c == '^'){
                (*grid_l.grid)[row][col]+=1;
                ge = grid_element(grid_element_type::blizzard, position(col, row), direction().up);
                blizzards.push_back(ge);
            }
            else if (c == 'v'){
                (*grid_l.grid)[row][col]+=1;
                ge = grid_element(grid_element_type::blizzard, position(col, row), direction().down);
                blizzards.push_back(ge);
            }
            else{
                throw std::runtime_error("unexpected grid element");
            }
            col++;
        }
        row++;
    }
    grid_l.blizzards = std::make_shared<std::vector<grid_element>>(blizzards);
    return std::make_shared<grid_layout>(grid_l);
}

int bfs(std::shared_ptr<grid_layout> grid_layout_ptr, grid_element player, std::vector<position>& directions){
    std::queue<grid_element> q;
    q.push(player);

    while(!q.empty()){
        auto& current = q.front();
        q.pop();

        for(auto& dir : directions){
            grid_element ge = grid_element(current.type, current.pos + dir, dir);
        }

    }
    return 0;
}

void simulate_blizzards(std::shared_ptr<grid_layout> grid_layout_ptr){
    for(auto& blizzard : *(grid_layout_ptr->blizzards)){
        position pos = blizzard.pos + blizzard.dir;
        if(grid_layout_ptr.grid[pos.y][pos.x].type == -1){

        }
    }
}

int get_result(){
    std::shared_ptr<grid_layout> grid_layout_ptr = parse_input();
    grid_element player = grid_layout_ptr.get()->start;

    direction dir = direction();
    std::vector<position> directions = {dir.right, dir.left, dir.up, dir.down, dir.none};

    // std::cout << (*grid_layout_ptr->grid.get())[1][1] << std::endl;
    return 0;
}