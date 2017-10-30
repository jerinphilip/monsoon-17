#include <iostream>
#include "buffer.hpp"


int main(int argc, char *argv[]){
    if (argc < 2 ){
        std::cerr << "Usage: " << argv[0] << " <filename> " ;
        std::cerr << std::endl;
        return 1;
    }
    read_buffer *rb;
    write_buffer *wb;
    rb = new read_buffer(argv[1], 1000);
    wb = new write_buffer(argv[2], 1000);
    row r;
    while (rb->advance(r)) {
        utils::print(std::cout, r);
        wb->write(r);
    }
    wb->flush();
    delete rb;
    delete wb;
    return 0;
}
