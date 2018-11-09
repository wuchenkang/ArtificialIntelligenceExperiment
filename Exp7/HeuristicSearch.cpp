#include "HeuristicSearch.h"

State::State(int size, int* state, int pivot, int cost, State* parent){
    this->size = size;
    this->state = new int[size * size];
    for(int i = 0; i < size * size; i++){
        this->state[i] = state[i];
    }
    this->pivot = pivot;
    this->cost = cost;
    this->parent = parent
}

State::~State(){
    delete[] this->state;
}