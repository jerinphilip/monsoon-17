/* Buffered IO Class, to read tables in parts. */

#include <bits/stdc++.h>
#include "dtype.h"
using namespace std;

class bufIO {
    string inputname, metaname;
    fstream meta, input;
    vector<pair<int, int>> S;
    int expected_size;
    int record_size;

    public:
        bufIO(string meta_in, string in){
            metaname = meta_in;
            inputname = in;
            input.open(inputname.c_str(), ios::in);
        }

        void load_meta(){
            int size;
            meta.open(metaname.c_str(), ios::in);
            int offset;
            record_size = 0;
            while ( meta >> size ){
                S.push_back(make_pair(offset, size));
                offset += size + 2 /* Space character */;
                record_size += size;
            }
            expected_size = offset-1;
            meta.close();
        }

        table read(int max_size){
            int nrecords = max_size/record_size;
            table t;
            string line, datum;
            //vector<vector<string>> table;
            int count = 0;
            while ( count < nrecords ){
                if(input.eof()){
                    break;
                }
                else{
                    getline(input, line);
                    //cout << line << endl;
                    //cout << line.size() << " " << expected_size << endl;
                    if((int)line.size() == expected_size){
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
            }
            return t;
        }


        ~bufIO(){
            input.close();
        }
};

int main(int argc, char *argv[]){
    string metaname(argv[1]);
    string inputname(argv[2]);
    bufIO b(metaname, inputname);
    b.load_meta();
    table t = b.read(10*94);
    cout << t << endl;
    return 0;
}
