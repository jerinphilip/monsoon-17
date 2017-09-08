#include <bits/stdc++.h>
#include "bufio.h"
using namespace std;

struct pack{
    string name;
    bufIO *b;
    table *t;
    int current, size, nRecords;

    pack(info meta, string filename, int sz){
        current = 0;
        name = filename;
        b = new bufIO(meta, name);
        size = sz;
        read();
    }

    bool complete(){
        return b->eof() and current == nRecords;
    }

    row next(){
        assert(not complete());
        row r = t->at(current);
        current = current + 1;
        if (current == nRecords){
            /* Possible segfault */
            delete t;
            read();
            current = 0;
        }
        return r;
    }

    void read(){
        t = b->read(size);
        nRecords = t->size();
    }

};

struct output{
    string name;
    info meta;
    fstream out;
    int size;
    int maxRecords;
    table t;

    output(info meta, string name, int size): 
        meta(meta), name(name),
        size(size){
        out.open(name, ios::out);

        maxRecords = size/meta.record_length;
    }

    void insert(row r){
        t.insert(r);
        if(t.size() == maxRecords){
            flush();
        }
    }

    void flush(){
        out << t;
        t.clear();
    }

};

