#include <memory>
#include <vector>
#include <unordered_map>
#include <queue>
#include <array>
#include <iostream>
#include <fstream>
#include <sstream>

enum grid_element_type {
    wall = 0, blizzard = 1, player = 2, none = 4, start = 8, end = 16
};

struct hash_item {
    int x;
    int y;
    int time;

    hash_item(int x, int y, int time): x(x), y(y), time(time) {};

    bool operator==(const hash_item &other) const
    { return (x == other.x
                && y == other.y
                && time == other.time);
    }
};

template <typename T, typename... Rest>
void hash_combine(std::size_t& seed, const T& v, const Rest&... rest)
{
    seed ^= std::hash<T>{}(v) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
    (hash_combine(seed, rest), ...);
}

template<>
struct std::hash<hash_item>
{
    std::size_t operator()(hash_item const& n) const noexcept
    {
        std::size_t h = 0;
        hash_combine(h, n.time, n.y, n.x);
        return h; // or use boost::hash_combine
    }
};


struct position {
    int x;
    int y;

    position() : x(-1), y(-1) {};
    position(int x, int y) { this->x = x; this->y = y; };

    position operator+(const position& a)        // passing lhs by value helps optimize chained a+b+c // otherwise, both parameters may be const references
    {
        return position(x + a.x, y + a.y);
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

    grid_element_state(grid_element g_element, int time) : g_element(g_element), time(time) {};
};


class grid_layout {
    public:
        std::vector<std::vector<int>> grid;

        std::vector<grid_element> blizzards;
        grid_element start;
        grid_element end;
        int row = -1;
        int col = -1;

        grid_layout(std::vector<grid_element>& blizzards, std::vector<std::vector<int>>& grid){
            this->grid = grid;
            this->blizzards = blizzards;
            // grid.fill({});
            // this->grid = std::make_shared<std::array<std::array<int, COL>, ROW>>(grid);
            // this->blizzards = std::make_shared<std::vector<grid_element>>(blizzards);
        };
};

std::shared_ptr<grid_layout> parse_input();
int bfs(std::shared_ptr<grid_layout> grid_layout_ptr, grid_element player, grid_element goal, std::vector<position>& directions);
bool can_move_on_grid(position& el_position, position& dir, std::shared_ptr<grid_layout> grid_layout_ptr);
void simulate_blizzards(std::shared_ptr<grid_layout> grid_layout_ptr);
int get_result();

std::shared_ptr<grid_layout> parse_input(){
    auto input = std::ifstream("/home/michael/git/adventofcode/aoc2022/src/aoc/day24/in.txt");

    
    std::vector<grid_element> blizzards;
    std::vector<std::vector<int>> grid;
    grid_element ge;
    int row = 0;
    int col = 0;

    for( std::string line; getline( input, line ); ){
        col = 0;
        std::vector<int> row_v;
        for(auto& c : line){
            if(c == '.'){
                row_v.push_back(0);
            }
            else if (c == '#') {
                row_v.push_back(-1);
            }
            else if (c == '<'){
                row_v.push_back(1);
                ge = grid_element(grid_element_type::blizzard, position(col, row), direction().left);
                blizzards.push_back(ge);
            }
            else if (c == '>'){
                row_v.push_back(1);
                ge = grid_element(grid_element_type::blizzard, position(col, row), direction().right);
                blizzards.push_back(ge);
            }
            else if (c == '^'){
                row_v.push_back(1);
                ge = grid_element(grid_element_type::blizzard, position(col, row), direction().up);
                blizzards.push_back(ge);
            }
            else if (c == 'v'){
                row_v.push_back(1);
                ge = grid_element(grid_element_type::blizzard, position(col, row), direction().down);
                blizzards.push_back(ge);
            }
            else{
                throw std::runtime_error("unexpected grid element");
            }
            col++;
        }
        grid.push_back(row_v);
        row++;
    }
    grid_layout grid_l{blizzards, grid};
    grid_l.start = grid_element(grid_element_type::start, position(1, 0), direction().none);
    grid_l.end = grid_element(grid_element_type::end, position(col-2, row-1), direction().none);
    grid_l.row = row;
    grid_l.col = col;
    // grid_l.blizzards = std::make_shared<std::vector<grid_element>>(blizzards);
    return std::make_shared<grid_layout>(grid_l);
}

int bfs(std::shared_ptr<grid_layout> grid_layout_ptr, grid_element player, grid_element goal, std::vector<position>& directions){
    std::queue<grid_element_state> q;

    grid_element_state element = grid_element_state(player, 0);
    q.push(element);
    int time = 0;

    std::unordered_map<hash_item, bool> visited;

    while(!q.empty()){
        auto current = q.front();
        if(current.g_element.pos == goal.pos){
            return current.time;
        }
        q.pop();
        hash_item h_i = hash_item(current.g_element.pos.x, current.g_element.pos.y, current.time);
        if(visited.find(h_i) != visited.end()){
            continue;
        }
        if(time != current.time){
            time++;
            simulate_blizzards(grid_layout_ptr);
        }
        for(auto& dir : directions){
            grid_element ge = grid_element(current.g_element.type, current.g_element.pos+dir, direction().none);
            grid_element_state ges = grid_element_state(ge, current.time + 1);
            if(can_move_on_grid(ge.pos, ge.dir, grid_layout_ptr)){
                q.push(ges);
            }
        }
        visited[h_i] = true;
    }
    return -1;
}

bool can_move_on_grid(position& el_position, position& dir, std::shared_ptr<grid_layout> grid_layout_ptr){
    position pos_res = el_position + dir;
    if(pos_res.y < 0 || pos_res.x < 0 || pos_res.y >= grid_layout_ptr->row || pos_res.x >= grid_layout_ptr->col){
        return false;
    }

    if((grid_layout_ptr->grid)[pos_res.y][pos_res.x] == 0){
        return true;
    }
    return false;
}

void simulate_blizzards(std::shared_ptr<grid_layout> grid_layout_ptr){
    direction dir = direction();
    for(auto& blizzard : (grid_layout_ptr->blizzards)){
        position pos = blizzard.pos + blizzard.dir;
        (grid_layout_ptr->grid)[blizzard.pos.y][blizzard.pos.x]--;
        
        if((grid_layout_ptr->grid)[pos.y][pos.x] == -1){
            // entering wall
            
            if(blizzard.dir == dir.down){
                blizzard.pos = position(pos.x, 1);
            }
            else if(blizzard.dir == dir.up){
                blizzard.pos = position(pos.x, grid_layout_ptr->row-2);
            }
            else if(blizzard.dir == dir.left){
                blizzard.pos = position(grid_layout_ptr->col-2, pos.y);
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
        (grid_layout_ptr->grid)[blizzard.pos.y][blizzard.pos.x]++;
    }
}

int get_result(){
    std::shared_ptr<grid_layout> grid_layout_ptr = parse_input();
    grid_element player = grid_layout_ptr.get()->start;
    grid_element goal = grid_layout_ptr.get()->end;

    direction dir = direction();
    std::vector<position> directions = {dir.right, dir.left, dir.up, dir.down, dir.none};

    simulate_blizzards(grid_layout_ptr);
    return bfs(grid_layout_ptr, player, goal, directions);
}

int get_result2(){
    std::shared_ptr<grid_layout> grid_layout_ptr = parse_input();
    grid_element player = grid_layout_ptr.get()->start;

    direction dir = direction();
    std::vector<position> directions = {dir.right, dir.left, dir.up, dir.down, dir.none};

    simulate_blizzards(grid_layout_ptr);
    int a = bfs(grid_layout_ptr, grid_layout_ptr.get()->start, grid_layout_ptr.get()->end, directions);
    int b = bfs(grid_layout_ptr, grid_layout_ptr.get()->end, grid_layout_ptr.get()->start, directions);
    int c = bfs(grid_layout_ptr, grid_layout_ptr.get()->start, grid_layout_ptr.get()->end, directions);

    return a + b + c;
}


int main(){
    std::cout << get_result() << std::endl;
    std::cout << get_result2() << std::endl;
}
