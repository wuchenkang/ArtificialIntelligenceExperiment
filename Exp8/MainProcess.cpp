#include "Reversi.h"
#include <iostream>

using namespace std;

int main(){
    Board board;
    int x, y;
    board.show();
    putchar('\n');
    while(true){
        if(!board.skipped()){
            cout << "Please place your placing choice:\t";
            cin >> x >> y;
            if(!board.move(x, y)){
                cout << "Position not available, please try again!" << endl;
                continue;
            }
            printf("B:\t%d %d\n", x, y);
            putchar('\n');
            board.show();
            putchar('\n');
        }else{
            board.skip();
            printf("# Black skipped!\n");
        }

        if(board.finished()){
            board.finish();
            printf(board.eval() > 0 ? "# Black win!\n" : "# White win!\n");
            break;
        }

        if(!board.skipped()){
            pair<int, int> temp = board.hint(6);
            x = temp.first;
            y = temp.second;
            printf("W:\t%d %d\n", x, y);
            if(!board.move(x, y)){
                cout << "Error!\n" << endl;
                continue;
            }
            putchar('\n');
            board.show();
            putchar('\n');

        }else{
            board.skip();
            printf("# White skipped!\n");
        }

        if(board.finished()){
            board.finish();
            printf(board.eval() > 0 ? "# Black win!\n" : "# White win!\n");
            break;
        }
    }
    return 0;
}
