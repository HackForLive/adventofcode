#ifndef RANGE_HPP_
#define RANGE_HPP_


class Range {
  private:
    int start;
    int end;

  public:
    Range(int start, int end);
    
    int getStart() { return start; }
    int getEnd()  { return end; }

};

// inline Range::Range(int s, int e) 
// { 
//     start = s;
//     end = e;
// }

#endif