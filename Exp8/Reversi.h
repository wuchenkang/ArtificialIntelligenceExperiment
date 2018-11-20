#ifndef ARTIFICIALINTELLIGENCEEXPERIMENT_REVERSI_H
#define ARTIFICIALINTELLIGENCEEXPERIMENT_REVERSI_H

#include <vector>

class Board{
public:
    Board();
    std::vector<std::pair<int, int> > judge(char state[6][6], int x, int y);
    void show();
    bool move(int x, int y);
    bool finished();
private:
    bool turn;
    char state[6][6];
};

#endif //ARTIFICIALINTELLIGENCEEXPERIMENT_REVERSI_H
