#ifndef ARTIFICIALINTELLIGENCEEXPERIMENT_REVERSI_H
#define ARTIFICIALINTELLIGENCEEXPERIMENT_REVERSI_H

#include <vector>

class Board{
public:
    Board();
    std::vector<std::pair<int, int> > judge(int x, int y, char state[6][6]);
    void show();
private:
    bool turn;
    char state[6][6];
};

#endif //ARTIFICIALINTELLIGENCEEXPERIMENT_REVERSI_H
