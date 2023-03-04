#ifndef NODE_HPP_
#define NODE_HPP_

//#include <boost/algorithm/cxx17/exclusive_scan.hpp>
//#include <boost/json/detail/hash_combine.hpp>
#include <string>

struct Node {
    uint8_t time;
    uint8_t ore_r;
    uint8_t clay_r;
    uint8_t obs_r;
    uint8_t ore_c;
    uint8_t clay_c;
    uint8_t obs_c;

    Node(uint8_t time, uint8_t ore_r, uint8_t clay_r, uint8_t obs_r, 
    uint8_t ore_c, uint8_t clay_c, uint8_t obs_c);

    bool operator==(const Node &other) const
    { return (time == other.time
                && ore_r == other.ore_r
                && clay_r == other.clay_r
                && obs_r == other.obs_r
                && ore_c == other.ore_c
                && clay_c == other.clay_c
                && obs_c == other.obs_c );
    }
};

template <typename T, typename... Rest>
void hash_combine(std::size_t& seed, const T& v, const Rest&... rest)
{
    seed ^= std::hash<T>{}(v) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
    (hash_combine(seed, rest), ...);
}

template<>
struct std::hash<Node>
{
    std::size_t operator()(Node const& n) const noexcept
    {
        std::size_t h = 0;
        hash_combine(h, n.time, n.ore_r, n.clay_r, n.obs_r, n.ore_c, n.clay_c, n.obs_c);
        return h; // or use boost::hash_combine
    }
};
#endif
