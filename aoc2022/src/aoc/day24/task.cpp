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

    bool operator==(const position& a) const
    {
        return (x == a.x && y == a.y);
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

struct grid_element_state
{
    grid_element g_element;
    int time;

    grid_element_state(grid_element g_element, int time){
        this->g_element = g_element;
        this->time = time;
    }
};


class grid_layout {
    public:
        const static int ROW = 6;//22;
        const static int COL = 8;//152;
        std::shared_ptr<std::array<std::array<int, COL>, ROW>> grid;

        std::shared_ptr<std::vector<grid_element>> blizzards;
        grid_element start;
        grid_element end;

        grid_layout(){
            std::array<std::array<int, COL>, ROW> grid;
            this->grid = std::make_shared<std::array<std::array<int, COL>, ROW>>(grid);
        };
};

std::shared_ptr<grid_layout> parse_input();
int bfs(std::shared_ptr<grid_layout> grid_layout_ptr, grid_element player, std::vector<position>& directions);
bool can_move_on_grid(position& el_position, position& dir, std::shared_ptr<grid_layout> grid_layout_ptr);
void simulate_blizzards(std::shared_ptr<grid_layout> grid_layout_ptr);
int get_result();
bool should_prone_grid_element_state(grid_element_state& ges, position& start);

std::shared_ptr<grid_layout> parse_input(){
    auto input = std::ifstream("/home/michael/git/adventofcode/aoc2022/src/aoc/day24/inn.txt");

    grid_layout grid_l;
    std::vector<grid_element> blizzards;
    grid_element ge;
    int row = 0;
    int col = 0;  

    for( std::string line; getline( input, line ); ){
        col = 0;

        for(auto& c : line){
            //  std::cout << row << std::endl;
            if(c == '.'){
                if(row == 0){
                    ge = grid_element(grid_element_type::start, position(col, row), direction().none);
                    grid_l.start = ge;
                    // std::cout << "start" << std::endl;
                }
                else if(row == grid_l.ROW-1){
                    // std::cout << "end" << std::endl;
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
    std::queue<grid_element_state> q;

    grid_element_state element = grid_element_state(player, 1);
    q.push(element);
    int time = 0;

    std::array<std::array<std::array<bool, 100>, 100>, 100> visited;

    // std::cout << grid_layout_ptr->end.pos.x << " < x y > " << grid_layout_ptr->end.pos.y << std::endl;
    // std::cout << grid_layout_ptr->start.pos.x << " < x y > " << grid_layout_ptr->start.pos.y << std::endl;
    // return -1; 
    // auto a = position(5,0);
    // auto b = position(0,5);
    // if(a==b){
    //     std::cout << "true" << std::endl;
    // }
    // return -1;

    while(!q.empty()){
        auto& current = q.front();
        if(current.g_element.pos == grid_layout_ptr->end.pos){
            return current.time;
        }
        q.pop();
        if(current.time >  9){
            continue;
        }
        else{
            std::cout << "current.time" << current.time << std::endl;
        }
        if(visited[current.g_element.pos.y][current.g_element.pos.x][current.time]){
            continue;
        }
        if(time != current.time){
            time++;
            std::cout << "time:" << time << std::endl;
            std::cout << "size:" << q.size() << std::endl;
            simulate_blizzards(grid_layout_ptr);
        }

        for(auto& dir : directions){
            grid_element ge = grid_element(current.g_element.type, current.g_element.pos + dir, dir);
            grid_element_state ges = grid_element_state(ge, time + 1);
            if(can_move_on_grid(ge.pos, ge.dir, grid_layout_ptr)){
                q.push(ges);
            }
        }
        visited[current.g_element.pos.y][current.g_element.pos.x][current.time] = true;
    }
    return -1;
}

bool should_prone_grid_element_state(grid_element_state& ges, position& start){
    // const int magic_constant = 0;
    // return abs(ges.g_element.pos.x - start.x) + abs(ges.g_element.pos.y - start.y) + magic_constant < ges.time;
    // std::cout << "prone time: " << ges.time << std::endl; 
    return ges.time > 4;
}

bool can_move_on_grid(position& el_position, position& dir, std::shared_ptr<grid_layout> grid_layout_ptr){
    position pos_res = el_position + dir;
    if((*grid_layout_ptr->grid)[pos_res.y][pos_res.x] == 0){
        return true;
    }
    return false;
}

void simulate_blizzards(std::shared_ptr<grid_layout> grid_layout_ptr){
    direction dir = direction();
    for(auto& blizzard : *(grid_layout_ptr->blizzards)){
        position pos = blizzard.pos + blizzard.dir;
        // (*grid_layout_ptr->grid)[blizzard.pos.y][blizzard.pos.x]--;
        
        if((*grid_layout_ptr->grid)[pos.y][pos.x] == -1){
            // entering wall
            blizzard.pos = position(pos.x, pos.y);
            
            if(blizzard.dir == dir.down){
                blizzard.pos = position(pos.x, 1);
            }
            else if(blizzard.dir == dir.up){
                blizzard.pos = position(pos.x, grid_layout_ptr->ROW-1);
            }
            else if(blizzard.dir == dir.left){
                blizzard.pos = position(grid_layout_ptr->COL-1, pos.y);
            }
            else if(blizzard.dir == dir.right) {
                blizzard.pos = position(1, pos.y);
            }
            else {
                throw std::runtime_error("Unexpected blizzard direction!");
            }
        }
        else{
            blizzard.pos = position(pos.x, pos.y);
        }
        // grid_layout_ptr->grid->data()[blizzard.pos.y][blizzard.pos.x] += 1;
    }
}

int get_result(){
    std::shared_ptr<grid_layout> grid_layout_ptr = parse_input();
    grid_element player = grid_layout_ptr.get()->start;

    direction dir = direction();
    std::vector<position> directions = {dir.right, dir.left, dir.up, dir.down, dir.none};


    // std::cout << (*grid_layout_ptr->grid.get())[1][1] << std::endl;
    return bfs(grid_layout_ptr, player, directions);
}

int main(){
    std::cout << get_result() << std::endl;
}