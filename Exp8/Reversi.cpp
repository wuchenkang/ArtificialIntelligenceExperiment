#include "Reversi.h"

using namespace std;

int Board::evalMap[6][6] = {
    {8, 1, 4, 4, 1, 8},
    {1, 1, 2, 2, 1, 1},
    {4, 2, 2, 2, 2, 4},
    {4, 2, 2, 2, 2, 4},
    {1, 1, 2, 2, 2, 1},
    {8, 1, 4, 4, 1, 8}
//    {2, 2, 2, 2, 2, 2},
//    {2, 2, 2, 2, 2, 2},
//    {2, 2, 2, 2, 2, 2},
//    {2, 2, 2, 2, 2, 2},
//    {2, 2, 2, 2, 2, 2},
//    {2, 2, 2, 2, 2, 2}
};

Board::Board(){
    // 棋盘初始化
    turn = true;
    for (auto &i : state) {
        for (char &j : i) {
            j = ' ';
        }
    }
    state[2][2] = state[3][3] = 'W';
    state[2][3] = state[3][2] = 'B';
}

Board::Board(const Board& other) {
    for(int i = 0; i < 6; i++){
        for(int j = 0; j < 6; j++){
            state[i][j] = other.state[i][j];
        }
    }
    turn = other.turn;
}

vector<pair<int, int> > Board::judge(int x, int y){
    vector<pair<int, int> > influenced_list;    // 记录被翻转的棋子
    // 当前位置已有棋子 ，返回空表1
    if(state[x][y] != ' '){
        return influenced_list;
    }

    // 判断己方和敌方棋子
    char own, enemy;
    if(turn){
        own = 'B';
        enemy = 'W';
    }else{
        own = 'W';
        enemy = 'B';
    }

    bool hasEnemy;

    // 对棋子上方的影响
    hasEnemy = false;
    for(int i = x - 1; i >= 0; i--){
        if(state[i][y] == enemy){
            hasEnemy = true;
            continue;
        }else if(hasEnemy && state[i][y] == own){
            for(int j = x - 1; j > i; j--){
                influenced_list.emplace_back(pair<int, int>(j, y));
            }
            break;
        }else{
            break;
        }
    }

    // 对棋子下方的影响
    hasEnemy = false;
    for(int i = x + 1; i < 6; i++){
        if(state[i][y] == enemy){
            hasEnemy = true;
            continue;
        }else if(hasEnemy && state[i][y] == own){
            for(int j = x + 1; j < i; j++){
                influenced_list.emplace_back(pair<int, int>(j, y));
            }
            break;
        }else{
            break;
        }
    }

    // 对棋子左方的影响
    hasEnemy = false;
    for(int i = y - 1; i >= 0; i--){
        if(state[x][i] == enemy){
            hasEnemy = true;
            continue;
        }else if(hasEnemy && state[x][i] == own){
            for(int j = y - 1; j > i; j--){
                influenced_list.emplace_back(pair<int, int>(x, j));
            }
            break;
        }else{
            break;
        }
    }

    // 对棋子右方的影响
    hasEnemy = false;
    for(int i = y + 1; i < 6; i++){
        if(state[x][i] == enemy){
            hasEnemy = true;
            continue;
        }else if(hasEnemy && state[x][i] == own){
            for(int j = y + 1; j < i; j++){
                influenced_list.emplace_back(pair<int, int>(x, j));
            }
            break;
        }else{
            break;
        }
    }

    // 对棋子左上方的影响
        hasEnemy = false;
        for(int i = x - 1, j = y - 1; i >= 0 && j >= 0; i--, j--){
            if(state[i][j] == enemy){
                hasEnemy = true;
                continue;
            }else if(hasEnemy && state[i][j] == own){
                for(int k = x - 1, l = y - 1; k > i && l > j; k--, l--){
                    influenced_list.emplace_back(pair<int, int>(k, l));
                }
                break;
            }else{
                break;
            }
    }

    // 对棋子左下方的影响
    hasEnemy = false;
    for(int i = x + 1, j = y - 1; i < 6 && j >= 0; i++, j--){
        if(state[i][j] == enemy){
            hasEnemy = true;
            continue;
        }else if(hasEnemy && state[i][j] == own){
            for(int k = x + 1, l = y - 1; k < i && l > j; k++, l--){
                influenced_list.emplace_back(pair<int, int>(k, l));
            }
            break;
        }else{
            break;
        }
    }

    // 对棋子右上方的影响
    hasEnemy = false;
    for(int i = x - 1, j = y + 1; i >= 0 && j < 6; i--, j++){
        if(state[i][j] == enemy){
            hasEnemy = true;
            continue;
        }else if(hasEnemy && state[i][j] == own){
            for(int k = x - 1, l = y + 1; k > i && l < j; k--, l++){
                influenced_list.emplace_back(pair<int, int>(k, l));
            }
            break;
        }else{
            break;
        }
    }

    // 对棋子右下方的影响
    hasEnemy = false;
    for(int i = x + 1, j = y + 1; i < 6 && j < 6; i++, j++){
        if(state[i][j] == enemy){
            hasEnemy = true;
            continue;
        }else if(hasEnemy && state[i][j] == own){
            for(int k = x + 1, l = y + 1; k < i && l < j; k++, l++){
                influenced_list.emplace_back(pair<int, int>(k, l));
            }
            break;
        }else{
            break;
        }
    }

    return influenced_list;
}

int Board::eval(){
    int chessDiff = 0;

    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 6; j++) {
            if(state[i][j] == 'B'){
                chessDiff+= evalMap[i][j];  // 黑方棋子使评估函数加上对应权重
            }else if(state[i][j] == 'W'){
                chessDiff-= evalMap[i][j];  // 白方棋子使评估函数减去对应权重
            }
        }
    }

    // 对于结束的棋局选择
    if(finished()){
        chessDiff *= 64;
    }

    return chessDiff;
}

bool Board::skipped(){
    for(int i = 0; i < 6; i++){
        for(int j = 0; j < 6; j++){
            if((state[i][j] == ' ' && !judge(i, j).empty())){
                return false;
            }
        }
    }
    return true;
}

void Board::skip(){
    turn = !turn;
//    printf(turn ? "# Black skipped!\n" : "# White skipped!\n");
}

bool Board::finished(){
    if(!skipped()){
        return false;
    }
    turn = !turn;
    if(!skipped()){
        turn = !turn;
        return false;
    }
    return true;
}

void Board::finish(){
//    printf(eval() > 0 ? "# Black win!\n" : "# White win!\n");
}

void Board::show(){
    int black_count = 0, white_count = 0;
    printf("    0   1   2   3   4   5\n");
    for(int i = 0; i < 6; i++){
        printf("  +---+---+---+---+---+---+\n%d ", i);
        for(int j = 0; j < 6; j++){
            if(state[i][j] == 'B') {
                black_count++;
                printf("| %s ", "●\0");
            }else if(state[i][j] == 'W'){
                white_count++;
                printf("| %s ", "○\0");
            }else{
                printf("|   ");
            }

        }
        printf("|\n");
    }
    printf("  +---+---+---+---+---+---+\n");
    printf("Black:\t%d pieces\n", black_count);
    printf("White:\t%d pieces\n", white_count);
    printf("Eval func:\t%d\n", eval());
}

bool Board::move(int x, int y){
    vector<pair<int, int> > influenced_list = judge(x, y);
    if(influenced_list.empty()){    // 无可被翻转的棋子·
        return false;
    }else{                          // 有可被翻转的棋子
        char own = turn ? 'B' : 'W';
        // 翻转所有可被翻转的棋子
        state[x][y] = own;
        for (auto &i : influenced_list) {
            state[i.first][i.second] = own;
        }
        turn = !turn;               // 进入敌方回合
        return true;
    }
}

pair<int, int> Board::hint(int depth){
    pair<int, int> result;
    int value, temp;
    Board next;

    if(turn){
        value = INT_MIN;
    }else{
        value = INT_MAX;
    }

    // 搜索当前所有可能的下法，选择对自己最有利的那种
    for(int i = 0; i < 6; i++) {
        for (int j = 0; j < 6; j++) {
            if (state[i][j] == ' ' && !judge(i, j).empty()) {
                next = *this;
                next.move(i, j);
                temp = next.search(1, depth, INT_MIN, INT_MAX);
                if(turn){
                    if(temp > value){
                        value = temp;
                        result.first = i;
                        result.second = j;
                    }
                }else{
                    if(temp < value){
                        value = temp;
                        result.first = i;
                        result.second = j;
                    }
                }
            }
        }
    }

    return result;
}

pair<int, int> Board::random(){
    vector<pair<int, int> > temp;

    for(int i = 0; i < 6; i++) {
        for (int j = 0; j < 6; j++) {
            if (state[i][j] == ' ' && !judge(i, j).empty()) {
                temp.emplace_back(i, j);
            }
        }
    }

    return temp[rand() % temp.size()];
}

int Board::search(int currentDepth, int maxDepth, int alpha, int beta){
    // 若达到最大搜索深度或棋局结束，则直接返回评估值
    if(currentDepth >= maxDepth || finished()){
        return eval();
    }

    int value, temp;
    Board next;

    // 若当前无子可下，则跳过己方回合，取敌方回合的评估值
    if(skipped()){
        next = *this;
        next.skip();
        return next.search(currentDepth+1, maxDepth, alpha, beta);
    }

    // 初始化
    if(turn){
        value = INT_MIN;
    }else{
        value = INT_MAX;
    }

    // 带alpha-beta剪枝的MinMax搜索
    for(int i = 0; i < 6; i++){
        for(int j = 0; j < 6; j++){
            // 若alpha > beta，则剪去当前分支
            if(alpha > beta){
//                printf("Purge!\n");
                return value;
            }
            // 对于所有可下的棋步进行递归搜索
            if(state[i][j] == ' ' && !judge(i, j).empty()){
                next = *this;
                next.move(i, j);
                temp = next.search(currentDepth+1, maxDepth, alpha, beta);
                if(turn){
                    // 更新alpha值
                    if(temp > alpha){
                        alpha = temp;
                    }
                    // 最小值节点
                    value = temp > value ? temp : value;
                }else{
                    // 更新beta值
                    if(temp < beta){
                        beta = temp;
                    }
                    // 最大值节点
                    value = temp < value ? temp : value;
                }
            }
        }
    }

    return value;
}