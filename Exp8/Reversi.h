#ifndef ARTIFICIALINTELLIGENCEEXPERIMENT_REVERSI_H
#define ARTIFICIALINTELLIGENCEEXPERIMENT_REVERSI_H

#include <vector>
#include <cstdio>
#include <cstdlib>
#include <climits>

class Board{
public:
    Board();
    Board(const Board& other);
    std::vector<std::pair<int, int> > judge(int x, int y);
    int eval();
    bool move(int x, int y);
    bool skipped();
    void skip();
    bool finished();
    void finish();
    void show();
    std::pair<int, int> hint(int depth);
private:
    int search(int currentDepth, int maxDepth);

    bool turn;
    char state[6][6];
};

#endif //ARTIFICIALINTELLIGENCEEXPERIMENT_REVERSI_H
