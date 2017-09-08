/* Buffered IO Class, to read tables in parts. */

#include <bits/stdc++.h>
#ifndef DTYPE_H
#define DTYPE_H
#include "dtype.h"
#endif
#include "bufio.h"
using namespace std;

struct super {

    super(const char *fmeta, const char *finput):
        meta_file(fmeta), 
        input_file(finput)
    {


    }

    void load_sort_sublists(){

    }



};

int main(int argc, char *argv[]){
    string metaname(argv[1]);
    info meta(metaname);

    string inputname(argv[2]);
    bufIO b(meta, inputname);

    int unit = 1024*1024;
    int RAM = 1*unit;
    RAM = 10*94;
    vector<string> intermediates;

    int count = 0;
    while (!b.eof()){
        count += 1;
        cout << count << endl;
        table t = b.read(RAM);
        t.sort_by_col(2);
        string chunkname = to_string(count) + ".imd";
        fstream f(chunkname, ios::out);
        f << t ;
        f.close();
        intermediates.push_back(chunkname);
    }

    /* Merge files */
    return 0;
}
