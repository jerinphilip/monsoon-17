/* Buffered IO Class, to read tables in parts. */

#include <bits/stdc++.h>
#ifndef DTYPE_H
#define DTYPE_H
#include "dtype.h"
#endif
#include "bufio.h"
using namespace std;

int main(int argc, char *argv[]){
    string metaname(argv[1]);
    info meta(metaname);

    string inputname(argv[2]);
    bufIO b(meta, inputname);

    int RAM = 4096;
    vector<string> intermediates;

    int count = 0;
    while (!b.eof()){
        count += 1;
        table t = b.read(RAM);
        t.sort_by_col(2);
        string chunkname = to_string(count) + ".intermediate";
        fstream f(chunkname, ios::out);
        f << t ;
        intermediates.push_back(chunkname);
    }

    /* Merge files */
    return 0;
}
