#ifndef ARTIFICIALINTELLIGENCEEXPERIMENT_REVERSI_H
#define ARTIFICIALINTELLIGENCEEXPERIMENT_REVERSI_H

#include <vector>
#include <cstdio>
#include <cstdlib>
#include <climits>
#include <ctime>

class Board{
public:
    Board();        // 默认构造函数
    Board(const Board& other);  // 拷贝构造函数
    std::vector<std::pair<int, int> > judge(int x, int y);  // 找出被当前下法翻转的所有棋子
    int eval();     // 评估函数
    bool move(int x, int y);    // 落子并更新被翻转的棋子
    bool skipped();     // 判断当前玩家是否无棋可下
    void skip();        // 跳过当前玩家的回合
    bool finished();    // 判断棋局是否结束（双方都无棋可下）
    void finish();      // 结束棋局
    void show();        // 打印出当前棋局
    std::pair<int, int> hint(int depth);    // 根据当前棋面给出提示
    std::pair<int, int> random();           // 随机选择可下的棋步
private:
    // 带Alpha-Beta剪枝的MinMax搜索
    int search(int currentDepth, int maxDepth, int alpha, int beta);

    bool turn;                  // 记录当前回合
    char state[6][6];           // 记录棋面
    static int evalMap[6][6];   // 静态评估函数的评估权值表
};

#endif //ARTIFICIALINTELLIGENCEEXPERIMENT_REVERSI_H
