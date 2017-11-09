#include <iostream>
#include "sort.hpp"

int main(int argc, char *argv[]){
    if ( argc < 3 ){
        std::cerr << "Usage: " << argv[0] << " <infile> <outfile>\n";
        return -1;
    }
    
    sorter *s = new sorter(argv[1], argv[2], 10000, 1);
    s->process();
    return 0;
}
