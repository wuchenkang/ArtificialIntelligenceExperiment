#include "Reversi.h"
#include <iostream>

using namespace std;

int main(){
    Board board;
    int x, y;
    board.show();
    putchar('\n');
    while(scanf("%d%d", &x, &y)){
        board.move(x, y);
        board.show();
        putchar('\n');
    }
    return 0;
}