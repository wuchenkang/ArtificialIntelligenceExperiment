#include <iostream>

using namespace std;

bool positionAvailable(const int* state, int current, int position){
    if(current == 0){
        return true;
    }
    for(int i = 0; i < current; i++){
        int temp = state[i] - position;
        if(temp == 0 || temp == current - i || temp == i - current){
            return false;
        }
    }
    return true;
}

bool nQueensBacktracking(int size, int* state, int current){
    if(current == size){
        return true;
    }
    for(int i = 0; i < size; i++){
        if(positionAvailable(state, current, i)){
            state[current] = i;
            if(nQueensBacktracking(size, state, current + 1)){
                return true;
            }
        }
    }
    return false;
}



int main(){
    int size;
    int* state;
    cout << "Please enter the size of n queens puzzle:\t" << endl;
    cin >> size;
    state = new int[size];
    if(nQueensBacktracking(size, state, 0)){
        for(int i = 0; i < size; i++){
            cout << state[i] << " ";
        }
        cout << endl;
    }else{
        cout << "No solution!" << endl;
    }
    return 0;
}