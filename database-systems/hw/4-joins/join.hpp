#include "buffer.hpp"
#include <vector>
#include <string>

/* Joins two relations by the indices, assuming they're sorted already? */
enum {
    C_FIRST,
    C_SECOND
};

struct join_struct {
    bool used, done;
    std::vector<row> vr;
    row representative;
    bool empty;
    int index;

    join_struct(int i){
        used = true;
        done = false;
        empty = true;
        index = i;
    }

    std::string key(){
        return representative[index];
    }
};

struct SortJoin {
    std::string R_fname, S_fname;
    read_buffer R_buffer, S_buffer;

    SortJoin(const char *R_fname, const char *S_fname, int buffer_size):
        R_fname(R_fname), S_fname(S_fname),
        R_buffer(R_fname, buffer_size/2), S_buffer(S_fname, buffer_size/2)
    {
        // ^ Evil hack - assuming buffers are half.
    }

    void join(int i=C_SECOND, int j=C_FIRST){
        join_struct r_state(i), s_state(j);
        while (not (r_state.done and s_state.done)){
            // Check if used.
            if (r_state.used){
                get_same(R_buffer, r_state);
            }
            if (s_state.used){
                get_same(S_buffer, s_state);
            }

            // There's something in R, S now. Compare if reps are same.
            if ( r_state.key() == s_state.key() ){
                // Cross product the two.
                cross_product(r_state.vr, s_state.vr);
                r_state.used = true;
                s_state.used = true;
            }

            else {
                // Pad with null?
            }
            
        }

    }

    void cross_product(std::vector<row> &vr, std::vector<row> &vs){
        for(auto &r: vr){
            for(auto &s: vs){
                row t;
                t.insert(t.end(), r.begin(), r.end());
                t.insert(t.end(), s.begin(), s.end());
                utils::print(std::cerr, t);
            }

        }
        vr.clear();
        vs.clear();
    }

    void get_same(read_buffer &rb, join_struct &js){
        bool initialized = false;
        bool done = false;
        row previous, current; 
        while (not done){
            if (not initialized){
                rb.advance(current);
                previous = current;
                js.vr.push_back(current);
                js.representative = current;
                initialized = true;
            }
            else{
                if(rb.get(current)){
                    if(current[js.index] == previous[js.index]){
                        js.vr.push_back(current);
                        previous = current;
                        rb.pop();
                    }
                    else{
                        done = true;
                    }
                }
                else {
                    js.done = true;
                }
            }
        }
        js.used = false;
    }
};
