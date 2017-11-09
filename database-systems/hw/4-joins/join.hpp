#include "buffer.hpp"
#include <vector>

/* Joins two relations by the indices, assuming they're sorted already? */
enum {
    C_FIRST,
    C_SECOND
};

class SortJoin {
    string R_fname, S_fname;
    read_buffer R_buffer, S_buffer;

    SortJoin(const char *R_fname, const char *S_fname, int buffer_size):
        R_fname(R_fname), S_fname(S_fname),
        R_buffer(R_fname, buffer_size/2), S_buffer(S_fname, buffer_size/2)
    {

    }

    void join(int i=C_SECOND, int j=C_FIRST){
        bool done = false;
        row r, s;

        // Scan into vector until content equal.

    }

    bool get_same(read_buffer &rb, int i, std::vector<row> &rs){
        bool initialized = false;
        bool done = false;
        row previous, current; 
        while (not done){
            if(not initialized){
                initialized = true;
                if(not rb.advance(current)){
                    return false;
                }
                rs.push_back(current);
                previous = current;
            }

            else{

                if(not rb.get(current)){
                    return false;
                }

                if ( current[i] != previous[i]){
                    done = true;
                }
                else{
                    rb.pop();
                    rs.push_back(current);
                }
            }
        }
        return true;
    }
};
