#include <iostream>
#include <vector>
#include <climits>
#include <ctime>

using namespace std;

// 判断皇后放置位置的有效性
bool positionAvailable(vector<int>& state, int current, int position){
    for(int i = 0; i < current; i++){   // 遍历每个已赋值的行
        int temp = state[i] - position;
        // 若当前位置(position, i)处在已赋值行位置的同一列或对角线上
        // 则不满足约束，不是一个有效的位置
        if(temp == 0 || temp == current - i || temp == i - current){
            return false;
        }
    }
    // 当前位置与所有已赋值行都不冲突，满足约束，是一个有效位置
    return true;
}

// 回溯算法
bool nQueensBacktracking(vector<int>& state, int current){
    // 所有行都放置有一个皇后，得到完整的解
    if(current == state.size()){
        return true;
    }

    // 遍历当前行所有位置
    for(int i = 0; i < state.size(); i++){
        // 如果该位置有效
        if(positionAvailable(state, current, i)){
            // 在该位置放下一个皇后，递归搜索下一行
            state[current] = i;
            if(nQueensBacktracking(state, current + 1)){
                return true;
            }
        }
    }

    // 当前行所有位置的放法都得不到一个完整的解
    return false;
}

// 前向检测算法（不使用MRV）
bool nQueensForwardChecking(vector<int> &state,
        vector<int> unassigned_list, vector<vector<int> > domain_list){
    // 所有变量都被赋值，找到完整解
    if(unassigned_list.empty()){
        return true;
    }

    int assigned_index = 0, assigned_variable, interval;
    vector<vector<int> > temp;

    assigned_variable = unassigned_list[assigned_index];
    unassigned_list.erase(unassigned_list.begin() + assigned_index);

    // 尝试为第一个未赋值的变量赋值
    for(int i = 0; i < domain_list[assigned_index].size(); i++){
        state[assigned_variable] = domain_list[assigned_index][i];
        temp = domain_list;
        temp.erase(temp.begin() + assigned_index);

        bool no_empty = true;
        // 遍历其他所有未赋值的变量
        for(int j = 0; j < unassigned_list.size(); j++){
            // 找出并去除值域中违反约束的值
            interval = abs(assigned_variable - unassigned_list[j]);
            auto iter = temp[j].begin();
            while(iter != temp[j].end()){
                if(*iter == state[assigned_variable] ||
                   abs(*iter - state[assigned_variable]) == interval){
                    iter = temp[j].erase(iter);
                    continue;
                }
                iter++;
            }

            // 存在未赋值变量的值域为空，当前赋值不可行
            if(temp[j].empty()){
                no_empty = false;
                break;
            }
        }

        // 递归对下一行进行赋值
        if(no_empty && nQueensForwardChecking(state, unassigned_list, temp)){
            return true;
        }
    }

    // 当前变量没有可行的赋值
    return false;
}

// 前向检测算法（使用MRV）
bool nQueensForwardCheckingWithMRV(vector<int> &state,
        vector<int> unassigned_list, vector<vector<int> > domain_list){
    // 找到完整解就返回
    if(unassigned_list.empty()){
        return true;
    }

    // 找出具有最小剩余值的变量
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

    // 尝试对该变量进行赋值
    for(int i = 0; i < domain_list[min_index].size(); i++){
        state[assigned_variable] = domain_list[min_index][i];
        temp = domain_list;
        temp.erase(temp.begin() + min_index);

        // 遍历其他所有未赋值的变量
        bool no_empty = true;
        for(int j = 0; j < unassigned_list.size(); j++){
            // 找出并去除值域中违反约束的值
            interval = abs(assigned_variable - unassigned_list[j]);
            auto iter = temp[j].begin();
            while(iter != temp[j].end()){
                if(*iter == state[assigned_variable] ||
                    abs(*iter - state[assigned_variable]) == interval){
                    iter = temp[j].erase(iter);
                    continue;
                }
                iter++;
            }

            // 存在未赋值变量的值域为空，当前赋值不可行
            if(temp[j].empty()){
                no_empty = false;
                break;
            }
        }

        // 递归对下一行进行赋值
        if(no_empty && nQueensForwardCheckingWithMRV(state, unassigned_list, temp)){
            return true;
        }
    }

    // 当前变量没有可行的赋值
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

void printState(vector<int>& state){
    for(int i = 0; i < state.size(); i++){
        cout << "+---";
    }
    cout << "+" << endl;
    for(int i = 0; i < state.size(); i++){
        cout << "+";
        for(int j = 0; j < state.size(); j++){
            if(j == state[i]){
                cout << " ● +";
            }else{
                cout << "   +";
            }
        }
        cout << endl;\
                for(int j = 0; j < state.size(); j++){
            cout << "+---";
        }
        cout << "+" << endl;
    }
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
    double start, end;

    cout << "BackTracking" << endl;
    start = clock() * 1000.0 / CLOCKS_PER_SEC;
    if(nQueensBacktracking(state, 0)){
        end = clock() * 1000.0 / CLOCKS_PER_SEC;
        if(validSolution(state)){
            cout << "[";
            for(int i = 0; i < size; i++){
                if(i == 0){
                    cout << state[i];
                }else{
                    cout << ", " << state[i];
                }
            }
            cout << "]" << endl;
//            printState(state);
        }else{
            cout << "Algorithm error!" << endl;
        }
    }else{
        end = clock() * 1000.0 / CLOCKS_PER_SEC;
        cout << "No solution!" << endl;
    }
    cout << "Total time:\t" << end - start << " ms" << endl << endl;

    cout << "ForwardChecking without MRV" << endl;
    start = clock() * 1000.0 / CLOCKS_PER_SEC;
    if(nQueensForwardChecking(state, unassigned, domains)){
        end = clock() * 1000.0 / CLOCKS_PER_SEC;
        if(validSolution(state)){
            cout << "[";
            for(int i = 0; i < size; i++){
                if(i == 0){
                    cout << state[i];
                }else{
                    cout << ", " << state[i];
                }
            }
            cout << "]" << endl;
//            printState(state);
        }else{
            cout << "Algorithm error!" << endl;
        }
    }else{
        end = clock() * 1000.0 / CLOCKS_PER_SEC;
        cout << "No solution!" << endl;
    }
    cout << "Total time:\t" << end - start << " ms" << endl << endl;

    cout << "ForwardChecking with MRV" << endl;
    start = clock() * 1000.0 / CLOCKS_PER_SEC;
    if(nQueensForwardCheckingWithMRV(state, unassigned, domains)){
        end = clock() * 1000.0 / CLOCKS_PER_SEC;
        if(validSolution(state)){
            cout << "[";
            for(int i = 0; i < size; i++){
                if(i == 0){
                    cout << state[i];
                }else{
                    cout << ", " << state[i];
                }
            }
            cout << "]" << endl;
//            printState(state);
        }else{
            cout << "Algorithm error!" << endl;
        }
    }else{
        end = clock() * 1000.0 / CLOCKS_PER_SEC;
        cout << "No solution!" << endl;
    }
    cout << "Total time:\t" << end - start << " ms" << endl << endl;
    return 0;
}