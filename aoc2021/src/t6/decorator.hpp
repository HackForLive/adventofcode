#ifndef DECORATOR_
#define DECORATOR_

#include <functional>
#include <chrono>
#include <iostream>

template <typename> 
struct ExeTime;

// Execution time decorator
template <typename R, typename... Args>
struct ExeTime<R(Args ...)> {
public:
    ExeTime(std::function<R(Args...)> func): f_(func) { } 

    R operator ()(Args ... args) {
        std::chrono::time_point<std::chrono::system_clock> start, end;
        std::chrono::duration<double> elapsed;

        start = std::chrono::system_clock::now();
        R result = f_(args...);    
        end = std::chrono::system_clock::now();
        elapsed = end - start;
        std::cout << elapsed.count() << " seconds" << std::endl;

        return result;   
    }   

private:
    std::function<R(Args ...)> f_;
};


template <typename R, typename... Args>
ExeTime<R(Args ...)> make_decorator(R (*f)(Args ...)) {
    return ExeTime<R(Args...)>(std::function<R(Args...)>(f));
}

#endif
