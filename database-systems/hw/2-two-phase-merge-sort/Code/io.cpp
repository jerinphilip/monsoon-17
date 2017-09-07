#include <bits/stdc++.h>
#include "dtype.h"
using namespace std;


int main(int argc, char *argv[]){
    fstream meta(argv[1], ios::in);
    fstream input(argv[2], ios::in);
    int size;
    int offset = 0;

    vector<pair<int, int>> S;
    while ( meta >> size ){
        S.push_back(make_pair(offset, size));
        offset += size + 2 /* Space character */;
    }

    table t;
    string line, datum;
    //vector<vector<string>> table;
    int count = 0;
    while (!input.eof()){
        getline(input, line);
        cout << line.size() << " " << offset << endl;
        if((int)line.size() == offset - 1){
            vector<string> tuple;
            count += 1;
            for (auto p: S){
                //cout << p.first << " " << p.second << " ";
                datum = line.substr(p.first, p.second);
                //cout << "[" << datum << "]"<< endl;
                tuple.push_back(datum);
            }
            t.insert(tuple);
        }
    }

    cout << count << " records."<<endl;
    t.sort_by_col(2);
    cout << t;
    return 0;
}
