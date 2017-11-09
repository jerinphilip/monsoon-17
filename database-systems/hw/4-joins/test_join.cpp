#include <iostream>
#include "sort.hpp"
#include "join.hpp"
#include <string>

int main(int argc, char *argv[]){
    if ( argc < 3 ){
        std::cerr << "Usage: " << argv[0] << " <R> <S>\n";
        return -1;
    }

    int buffer_size;

    buffer_size = 10000;
    
    std::string output_R, output_S;
    output_R = std::string(argv[1]) + ".sorted";
    output_S = std::string(argv[2]) + ".sorted";
    
    /* Sort and write out */
    sorter *s;
    s = new sorter(argv[1], output_R.c_str(), buffer_size, 1);
    s->process();
    delete s;
    s = new sorter(argv[2], output_S.c_str(), buffer_size, 0);
    s->process();
    delete s;

    SortJoin *S;
    S = new SortJoin(output_R.c_str(), output_S.c_str(), buffer_size);
    S->join(1, 0);

    return 0;
}
