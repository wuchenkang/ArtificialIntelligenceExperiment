#include <iostream>
#include <vector>
#include <climits>

using namespace std;

bool positionAvailable(vector<int>& state, int current, int position){
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

bool nQueensBacktracking(vector<int>& state, int current){
    if(current == state.size()){
        return true;
    }
    for(int i = 0; i < state.size(); i++){
        if(positionAvailable(state, current, i)){
            state[current] = i;
            if(nQueensBacktracking(state, current + 1)){
                return true;
            }
        }
    }
    return false;
}

bool nQueensForwardChecking(vector<int>& state, vector<int> unassigned_list, vector<vector<int> > domain_list){
    if(unassigned_list.empty()){
        return true;
    }

    int min = INT_MAX, min_index = -1, assigned_variable, interval;
    vector<vector<int> > temp;
    for(int i = 0; i < unassigned_list.size(); i++){
        if(domain_list[i].size() < min){
            min = (int)domain_list[i].size();
            min_index = i;
        }
    }

    assigned_variable = unassigned_list[min_index];
    unassigned_list.erase(unassigned_list.begin() + min_index);

    for(int i = 0; i < domain_list[min_index].size(); i++){
        state[assigned_variable] = domain_list[min_index][i];
        temp = domain_list;
        temp.erase(temp.begin() + min_index);

        for(int j = 0; j < unassigned_list.size(); j++){
            interval = abs(assigned_variable - unassigned_list[j]);
            vector<int>::iterator iter = temp[j].begin();
            while(iter != temp[j].end()){
                if(*iter == state[assigned_variable] ||
                    abs(*iter - state[assigned_variable]) == interval){
                    iter = temp[j].erase(iter);
                    continue;
                }
                iter++;
            }
            if(temp[j].empty()){
                break;
            }
        }
        if(nQueensForwardChecking(state, unassigned_list, temp)){
            return true;
        }
    }
    return false;
}

bool validSolution(vector<int> state){
    for(int i = 0; i < state.size()-1; i++){
        for(int j = i + 1; j < state.size(); j++){
            if(state[i] == state[j] || abs(state[i] - state[j]) == abs(i - j)){
                return false;
            }
        }
    }
    return true;
}

int main(){
    int size;
    vector<int> state, unassigned;
    vector<vector<int> > domains;
    cout << "Please enter the size of n queens puzzle:\t" << endl;
    cin >> size;
    for(int i = 0; i < size; i++){
        state.push_back(0);
        unassigned.push_back(i);
        domains.push_back(vector<int>());
        for(int j = 0; j < size; j++){
            domains[i].push_back(j);
        }
    }
//    if(nQueensBacktracking(state, 0)){
    if(nQueensForwardChecking(state, unassigned, domains)){
        if(validSolution(state)){
            for(int i = 0; i < size; i++){
                cout << state[i] << " ";
            }
            cout << endl;
        }else{
            cout << "Algorithm error!" << endl;
        }
    }else{
        cout << "No solution!" << endl;
    }
    return 0;
}