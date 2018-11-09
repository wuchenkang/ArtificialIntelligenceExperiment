#include <iostream>

using namespace std;

class State{
public:
    State(int size, int* state, int pivot, int cost, State* parent);
    ~State();
    State getUp();
    State getDown();
    State getLeft();
    State getRight();
private:
    int size;
    int* state;
    int pivot;
    int cost;
    State* parent;
};


int main(){
    cout << "Hello world!" << endl;
    return 0;
}