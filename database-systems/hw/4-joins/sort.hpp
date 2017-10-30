#ifndef SORTER_H
#define SORTER_H

#include "buffer.h"
#include "util.h"
#include <vector>

struct sorter {
    std::vector <std::string> wbfs;
    read_buffer rb;
    write_buffer wb;
    int buffer_size;

    sorter(const char *filename, const char *outfile, int buffer_size):
        rb(filename, buffer_size), 
        wb(filename, buffer_size)
        buffer_size(buffer_size){
    }

    void process(){
        split();
        merge();
    }

    void new_write_buffer(int count){
        string filename = std::to_string(count) + ".imd";
        wbfs.push_back(filename);
        return write_buffer_hard(filename.c_str(), buffer_size);
    }

    void split(){
        row r;
        int count = 0;
        write_buffer_hard wbh = new_write_buffer(count);
        while ( rb.advance(r) ){
            if (not wbh.write(r)){
                wbh.flush();
                count = count + 1;
                wbh = new_write_buffer(count);
            }
        }
        wbf.flush();
    }

    void merge(){
        vector<read_buffer> rbs;
        int count = wbfs.size();
        int sublist_buffer_size = buffer_size/(count+1);
        for(auto &fn: wbfs){
            read_buffer rb(fn.c_str(), sublist_buffer_size);
            rbs.push_back(rb);
        }
        bool complete = false;
        row min, current;
        int min_index = -1;
        while (not complete){
            bool first = true;
            for ( auto &rb: rbs ){
                if ( first ) {
                    min = rb.get(current);
                    min_index = 0;
                    first = false;
                }
                else {
                    if(less_than(current, min)){

                    }
                }
                rb.get(current);
            }
        }
    }

};

#endif
