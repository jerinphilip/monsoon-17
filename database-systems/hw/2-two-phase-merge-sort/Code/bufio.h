#include "bits/stdc++.h"
#ifndef DTYPE_H
#define DTYPE_H
#include "dtype.h"
#endif
class bufIO {
    string inputname, metaname;
    fstream input;
    info meta;
    vector<pair<int, int>> S;
    int expected_size;
    int record_size;

    public:
        bufIO(info _meta, string in): meta(_meta){
            inputname = in;
            input.open(inputname.c_str(), ios::in);
        }

        table read(int max_size){
            int nrecords = max_size/meta.record_length;
            table t;
            string line, datum;
            int count = 0;
            while ( count < nrecords ){
                if(input.eof()){
                    break;
                }
                else{
                    getline(input, line);
                    if((int)line.size() == meta.expected_size){
                        vector<string> tuple;
                        count += 1;
                        for (auto p: meta.sizes){
                            datum = line.substr(p.first, p.second);
                            tuple.push_back(datum);
                        }
                        t.insert(tuple);
                    }
                }
            }
            cout<<"Loaded "<<count<<" records.\n";
            return t;
        }


        ~bufIO(){
            input.close();
        }

        bool eof(){
            return input.eof();
        }
};

