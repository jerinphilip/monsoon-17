#ifndef SORTER_H
#define SORTER_H

#include "buffer.hpp"
#include <vector>
#include <queue>
#include <algorithm>

struct sorter {
    std::vector <std::string> wbfs;
    read_buffer rb;
    write_buffer wb;
    int buffer_size;
    int index;

    sorter(const char *infile, const char *outfile, int buffer_size, int index):
        rb(infile, buffer_size),
        wb(outfile, buffer_size),
        buffer_size(buffer_size),
        index(index){
    }

    void process(){
        split();
        merge();
    }

    write_buffer_hard* new_write_buffer(int count){
        std::string filename = "intermediates/" + std::to_string(count) + ".imd";
        wbfs.push_back(filename);
        write_buffer_hard* wbh = new write_buffer_hard(filename.c_str(), buffer_size);
        return wbh;
    }

    void split(){
        row r;
        std::vector<row> table;
        int count = 0;
        write_buffer_hard *wbh = new_write_buffer(count);
        int current_size = 0;
        while ( rb.advance(r) ){
            if(current_size + utils::row_ssize(r) <= buffer_size){
                current_size += utils::row_ssize(r);
                table.push_back(r);
            }
            else{
                sort(table.begin(), table.end(), utils::comparator(index));
                for(auto &r: table){
                    wbh->write(r);
                }
                wbh->flush();
                count = count + 1;
                wbh = new_write_buffer(count);
                table.clear();
                table.push_back(r);
                current_size = utils::row_ssize(r);
            }
        }
        std::cerr << "Stuck?" << std::endl;
        wbh->flush();
    }

    void merge(){
        std::vector<read_buffer*> rbs;
        int count = wbfs.size();
        int sublist_buffer_size = buffer_size/(count+1);
        for(auto &fn: wbfs){
            read_buffer *rb = new read_buffer(fn.c_str(), sublist_buffer_size);
            rbs.push_back(rb);
        }

        /* Priority queue node */
        typedef std::pair<row, int> node;
        auto compare = [](int index_){
            auto inner_ = [index_](const node a, const node b){
                return a.first[index_] < b.first[index_];
            };
            return inner_;
        };

        auto compare_ = compare(index);
        std::priority_queue<node, std::vector<node>, decltype(compare_)> Q(compare_);
        for(int i=0; i < count; i++){
            row r;
            if (rbs[i]->advance(r)) {
                auto qnode = make_pair(r, i);
                utils::print(std::cerr, r);
                Q.push(qnode);
            }
        }
        while (not Q.empty()){
            auto qnode = Q.top(); Q.pop();
            wb.write(qnode.first);

            row r;
            if(rbs[qnode.second]->advance(r)){
                qnode = make_pair(r, qnode.second);
                Q.push(qnode);
            }
        }

    }

};

#endif
