#include "buffer.hpp"

struct HashJoin {
    read_buffer R_buffer, S_buffer;

    HashJoin(const char *R_fname, 
            const char *S_fname,
            int buffer_size):
        R_buffer(R_fname, buffer_size/2),
        S_buffer(S_fname, buffer_size/2){
    
    }
};

