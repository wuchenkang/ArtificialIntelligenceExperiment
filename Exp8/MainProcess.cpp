#include "Reversi.h"
#include <iostream>

using namespace std;

int main(){
    int win = 0, total  = 20;
    srand((unsigned int)time(nullptr));
    for(int i = 0; i < total; i++){
        Board board;
        int x, y;
        board.show();
        putchar('\n');
        while(true){
            if(!board.skipped()){
                pair<int, int> temp = board.random();
                x = temp.first;
                y = temp.second;
                printf("B:\t%d %d\n", x, y);
                if(!board.move(x, y)){
                    cout << "Error!\n" << endl;
                    continue;
                }
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
                if(board.eval() < 0){
                    win++;
                }
                break;
            }

            if(!board.skipped()){
                pair<int, int> temp = board.hint(8);
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
                if(board.eval() < 0){
                    win++;
                }
                break;
            }
        }
    }
    printf("Win rate:\t%f%%\n", win * 100.0 / total);
    return 0;
}