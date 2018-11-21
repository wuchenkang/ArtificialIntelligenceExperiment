#include "Reversi.h"

using namespace std;

int Board::evalMap[6][6] = {
    {8, 4, 2, 2, 4, 8},
    {4, 1, 2, 2, 1, 4},
    {2, 2, 2, 2, 2, 2},
    {2, 2, 2, 2, 2, 2},
    {4, 1, 2, 2, 1, 4},
    {8, 4, 2, 2, 4, 8}
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
    vector<pair<int, int> > influenced_list;
    // 当前位置已有棋子
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

    // 上
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

    // 下
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

    // 左
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

    // 右
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

    // 左上
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

    // 左下
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

    // 右上
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

    // 右下
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
                chessDiff+= evalMap[i][j];
            }else if(state[i][j] == 'W'){
                chessDiff-= evalMap[i][j];
            }
        }
    }

    if(finished()){
        chessDiff *= 10;
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
    printf("    0   1   2   3   4   5\n");
    for(int i = 0; i < 6; i++){
        printf("  +---+---+---+---+---+---+\n%d ", i);
        for(int j = 0; j < 6; j++){
            if(state[i][j] == 'B') {
                printf("| %s ", "●\0");
            }else if(state[i][j] == 'W'){
                printf("| %s ", "○\0");
            }else{
                printf("|   ");
            }

        }
        printf("|\n");
    }
    printf("  +---+---+---+---+---+---+\n");
}

bool Board::move(int x, int y){
    vector<pair<int, int> > influenced_list = judge(x, y);
    if(influenced_list.empty()){
        return false;
    }else{
        char own = turn ? 'B' : 'W';
        state[x][y] = own;
        for (auto &i : influenced_list) {
            state[i.first][i.second] = own;
        }
        turn = !turn;
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

// TODO
int Board::search(int currentDepth, int maxDepth, int alpha, int beta){
    if(currentDepth >= maxDepth || finished()){
        return eval();
    }

    int value, temp;
    Board next;

    if(skipped()){
        next = *this;
        next.skip();
        return next.search(currentDepth+1, maxDepth, alpha, beta);
    }

    if(turn){
        value = INT_MIN;
    }else{
        value = INT_MAX;
    }

    for(int i = 0; i < 6; i++){
        for(int j = 0; j < 6; j++){
            if(alpha > beta){
//                printf("Purge!\n");
                return value;
            }
            if(state[i][j] == ' ' && !judge(i, j).empty()){
                next = *this;
                next.move(i, j);
                temp = next.search(currentDepth+1, maxDepth, alpha, beta);
                if(turn){
                    if(temp > alpha){
                        alpha = temp;
                    }
                    value = temp > value ? temp : value;
                }else{
                    if(temp < beta){
                        beta = temp;
                    }
                    value = temp < value ? temp : value;
                }
            }
        }
    }

    return value;
}