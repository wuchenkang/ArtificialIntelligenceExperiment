#include "Reversi.h"
#include <iostream>
#include <ctime>

using namespace std;

int main(){
    int win = 0, total  = 1;
    unsigned int start = static_cast<unsigned int>(time(nullptr));
    srand((unsigned int)time(nullptr));
    printf("AI vs Player\n");
    for(int i = 0; i < total; i++){
        Board board;
        int x, y;
        board.show();
        putchar('\n');
        while(true){
            if(!board.skipped()){
                pair<int, int> temp = board.hint(6);
//                pair<int, int> temp = board.random();
                x = temp.first;
                y = temp.second;
                printf("B:\t%d %d\n", x, y);
                if(!board.move(x, y)){
                    cout << "Error!\n" << endl;
                    exit(-1);
                }
                board.show();
                putchar('\n');
            }else{
                board.skip();
                printf("# Black skipped!\n");
            }

            if(board.finished()){
                board.finish();
                printf(board.win() > 0 ? "# Black win!\n" : "# White win!\n");
                if(board.win() > 0){
                    win++;
                }
                break;
            }

            if(!board.skipped()){
//                pair<int, int> temp = board.hint(i+1);
//                pair<int, int> temp = board.random();
//                x = temp.first;
//                y = temp.second;
                printf("Please enter your choise:\t");
                scanf("%d%d", &x, &y);
//                if(!board.move(x, y)){
//                    cout << "Error!\n" << endl;
//                    exit(-1);
//                }
                while(!board.move(x, y)){
                    printf("Please try again:\t");
                    scanf("%d%d", &x, &y);
                }
                printf("W:\t%d %d\n", x, y);
                board.show();
                putchar('\n');
            }else{
                board.skip();
                printf("# White skipped!\n");
            }

            if(board.finished()){
                board.finish();
                printf(board.win() > 0 ? "# Black win!\n" : "# White win!\n");
                if(board.win() > 0){
                    win++;
                }
                break;
            }
        }
    }
    unsigned int end = static_cast<unsigned int>(time(nullptr));
//    printf("Win rate:\t%f%%\n", win * 100.0 / total < 50 ? 100.0 - win * 100.0 / total : win * 100.0 / total);
    printf("Time:\t%us\n", end - start);
    return 0;
}
