#ifndef NODE_HPP_
#define NODE_HPP_

#include <string>

class Node {
    private:
        int time;
        int ore_r;
        int clay_r;
        int obs_r;
        int ore_c;
        int clay_c;
        int obs_c;
    public:
        Node(int time, int ore_r, int clay_r, int obs_r, int ore_c, int clay_c, int obs_c);

        int time_p = time;
        int ore_r_p = ore_r;
        int clay_r_p = clay_r;
        int obs_r_p = obs_r;

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

// custom specialization of std::hash can be injected in namespace std
template<>
struct std::hash<Node>
{
    std::size_t operator()(Node const& s) const noexcept
    {
        std::size_t h1 = std::hash<int>{}(s.time_p);
        std::size_t h2 = std::hash<int>{}(s.ore_r_p);
        std::size_t res = h1 ^ (h2 << 1);
        res = std::hash<int>{}(s.clay_r_p) ^ (res << 1);
        res = std::hash<int>{}(s.obs_r_p) ^ (res << 1);
        return res; // or use boost::hash_combine
    }
};

#endif
