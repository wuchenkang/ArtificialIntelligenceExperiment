#include "Reversi.h"
#include <iostream>

using namespace std;

int main(){
    Board board;
    int x, y;
    board.show();
    putchar('\n');
    while(!board.finished()){
        cout << "Please place your placing choice:\t";
        cin >> x >> y;
        if(!board.move(x, y)){
            cout << "Position not available, please try again!" << endl;
            continue;
        }
        putchar('\n');
        board.show();
        putchar('\n');
    }
    return 0;
}
