#include <bits/stdc++.h> 
#include "io.h"

using namespace std;

int main(int argc, char *argv[]){
    string metaname(argv[1]);
    info meta(metaname);

    string inputname(argv[2]);
    bufIO b(meta, inputname);

    string mb_size_str(argv[4]);
    int mb = atoi(mb_size_str.c_str());
    string sortorder(argv[5]);
    int unit = 1024*1024;
    int RAM = mb*unit;
    //RAM = 120*94;
    vector<string> intermediates;

    int count = 0;
    vector<int> order;
    string arg;
    for(int i=6; i<argc; i++){
        arg = string(argv[i]);
        order.push_back(meta.index[arg]);
    }
    while (!b.eof()){
        count += 2;
        //cout << count << endl;
        table *t = b.read(RAM);
        t->sort_by_col(order);
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

    if (not sublist_size){
        cerr << "Not sortable. Monster huge." << endl;
    }

    vector<pack> V;
    for(auto &intermediate: intermediates){
        pack v(meta, intermediate, sublist_size);
        V.push_back(v);
    }

    typedef pair<pack*, row> heapnode;
    auto compare = [&order](heapnode x, heapnode y){
        for(auto &col: order){
            if(x.second[col] != y.second[col])
                return x.second[col] > y.second[col];
        }
        return false;
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

        outbuffer.insert(r);
    }

    outbuffer.flush();
    for(auto &p: V){
        remove(p.name.c_str());
    }

    return 0;
}
