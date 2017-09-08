#include <bits/stdc++.h>
using namespace std;


typedef vector<string> row;

struct info {
    map<string, int> index;
    vector<pair<int, int>> sizes;
    int record_length;
    int expected_size;


   info(string filename){
        int size, offset, count, pos;
        string column, line, size_str;
        char delimiter;
        fstream meta;

        meta.open(filename.c_str(), ios::in);
        record_length = 0;
        offset = 0;
        count = 0;
        delimiter = ',';
        while (getline(meta, line)){
            pos = line.find(delimiter);
            column = line.substr(0, pos);
            size_str = line.substr(pos+1, string::npos);
            size = atoi(size_str.c_str());
            sizes.push_back(make_pair(offset, size));
            offset += size + 2 /* Space character */;
            record_length += size;
            index[column] = count;
            count += 1;
        }
        expected_size = offset-1;
        meta.close();
    }

};


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
        auto compare = [&col](row x, row y){
            return x[col] < y[col];
        };
        sort(T->begin(), T->end(), compare); 
    }

    row at(int x){
        return T->at(x);
    }

    friend ostream & operator << (ostream &out, table &t){
        for(auto &row: *(t.T)){
            int count = 0;
            for(auto &datum: row){
                out << datum; 
                count += 1;
                if ( count < (int)row.size())
                    out << "  ";
            }
            out << "\r\n";
        }
        return out;
    }

    int size(){
        return T->size();
    }

    void clear(){
        T->clear();
    }

    ~table(){
        delete T;
    }

};


