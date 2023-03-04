#include "node.hpp"

Node::Node(uint8_t time_l, uint8_t ore_r_l, uint8_t clay_r_l, uint8_t obs_r_l, 
uint8_t ore_c_l, uint8_t clay_c_l, uint8_t obs_c_l){
    time = time_l;
    ore_r = ore_r_l;
    clay_r = clay_r_l;
    obs_r = obs_r_l;
    ore_c = ore_c_l;
    clay_c = clay_c_l;
    obs_c = obs_c_l;
}
