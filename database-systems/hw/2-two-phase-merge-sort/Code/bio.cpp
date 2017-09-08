/* Buffered IO Class, to read tables in parts. */
#include <bits/stdc++.h> 
#ifndef DTYPE_H 
#define DTYPE_H
#include "dtype.h"
#endif
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

int main(int argc, char *argv[]){
    string metaname(argv[1]);
    info meta(metaname);

    string inputname(argv[2]);
    bufIO b(meta, inputname);

    int unit = 1024*1024;
    int RAM = 1*unit;
    RAM = 120*94;
    vector<string> intermediates;

    int count = 0;
    int column = 2;
    while (!b.eof()){
        count += 2;
        //cout << count << endl;
        table *t = b.read(RAM);
        t->sort_by_col(column);
        string chunkname = to_string(count) + ".imd";
        fstream f(chunkname, ios::out);
        f << (*t) ;
        f.close();
        delete t;
        intermediates.push_back(chunkname);
    }

    /* Merge files */

    int N = intermediates.size();
    int sublist_size = RAM/(N + 1);

    vector<pack> V;
    for(auto &intermediate: intermediates){
        pack v(meta, intermediate, sublist_size);
        V.push_back(v);
    }

    typedef pair<pack*, row> heapnode;
    auto compare = [&column](heapnode x, heapnode y){
        return x.second[column] > y.second[column];
    };


    priority_queue<heapnode, 
        vector<heapnode>, 
        decltype(compare)> Q(compare);

    /* Initialize */
    for(auto &p: V){
        if(not p.complete()){
            heapnode h = make_pair(&p, p.next());
            Q.push(h);
        }
    }

    string outname(argv[3]);
    output outbuffer(meta, outname, sublist_size);

    while (not Q.empty()){
        auto ph = Q.top();
        Q.pop();
        pack *p = ph.first; 
        row r = ph.second;
        if(not p->complete()){
            heapnode h = make_pair(p, p->next());
            Q.push(h);
        }

        for(auto &d: r){
            cout << d << " ";
        }
        cout << endl;

        outbuffer.insert(r);
    }

    outbuffer.flush();
    for(auto &p: V){
        remove(p.name.c_str());
    }

    return 0;
}
