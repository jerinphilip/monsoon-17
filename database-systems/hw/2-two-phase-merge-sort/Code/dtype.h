#include <bits/stdc++.h>
using namespace std;


typedef vector<string> row;

class table {
    vector<row> *T;

    public:

    table(){
        T = new vector<row>;
    }
    void insert(row x){
        T->push_back(x);
    }

    void sort_by_col(int col){
        auto comparator = [&col](row x, row y){
            return x[col] < y[col];
        };
        sort(T->begin(), T->end(), comparator); 
    }

    friend ostream & operator << (ostream &out, table &t){
        for(auto &row: *(t.T)){
            for(auto &datum: row){
                out << datum << "<>";
            }
            out << "\n";
        }
        return out;
    }
};

