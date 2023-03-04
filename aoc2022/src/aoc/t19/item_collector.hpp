#pragma once

#include <string>

struct ItemCollector
{
    // three-bit unsigned field, allowed values are 0...255
    short ore;
    short clay;
    short obs;
    short geo;

    ItemCollector() : ore(1), clay(0), obs(0), geo(0) {};

    ItemCollector(short ore, short clay, short obs, short geo) : ore(ore), clay(clay), obs(obs), geo(geo) {};
};
