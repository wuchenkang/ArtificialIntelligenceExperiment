#include "Reversi.h"
#include <vector>

using namespace std;

Board::Board(){
    // 棋盘初始化
    turn = true;
    for(int i = 0; i < 6; i++){
        for(int j = 0; j < 6; j++){
            state[i][j] = '?';
        }
    }
    state[2][2] = state[3][3] = 'W';
    state[2][3] = state[3][2] = 'B';
}

vector<pair<int, int> > Board::judge(int x, int y, char state[6][6]){
    vector<pair<int, int> > influenced_pos;
    // 当前位置已有棋子
    if(state[x][y] != '?'){
        return influenced_pos;
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
    for(int i = x - 1; i > 0; i--){
        if(state[i][y] == enemy){
            hasEnemy = true;
            continue;
        }else if(hasEnemy && state[i][y] == own){
            for(int j = x - 1; j > i; j--){
                influenced_pos.emplace_back(pair<int, int>(j, y));
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
                influenced_pos.emplace_back(pair<int, int>(j, y));
            }
            break;
        }else{
            break;
        }
    }

    // 左
    hasEnemy = false;
    for(int i = y - 1; i > 0; i--){
        if(state[x][i] == enemy){
            hasEnemy = true;
            continue;
        }else if(hasEnemy && state[x][i] == own){
            for(int j = y - 1; j > i; j--){
                influenced_pos.emplace_back(pair<int, int>(x, j));
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
            for(int j = y + 1; j < 6; j++){
                influenced_pos.emplace_back(pair<int, int>(x, j));
            }
            break;
        }else{
            break;
        }
    }

    return influenced_pos;
}