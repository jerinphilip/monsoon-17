#ifndef BUFFER_H
#define BUFFER_H

#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <queue>

typedef std::vector<std::string> row;
typedef std::queue<row> table;

namespace utils {

    int print(std::ostream &out, row &r){
        int size = 0;
        bool first = true;
        for(auto &c: r){
            if (not first){
                out << " "; size += 1;
            }

            first = false;
            out << c; size += c.size();
        }
        out << "\n"; size += 1;
        return size;
    }

    auto comparator = [](int index){
        auto comp_ = [&index](const row &r, const row &s){
            return r[index] < s[index];
        };
        return comp_;
    };

    int row_size(row &r){
        int size_ = 0;
        for (auto &c: r){
            size_ += c.size();
        }
        return size_;
    }

    int row_ssize(row &r){
        int size = 0;
        bool first = true;
        for(auto &c: r){
            if (not first){
                size += 1;
            }

            first = false;
            size += c.size();
        }
        size += 1;
        return size;
    }

}

struct read_buffer {
    int max_buffer_size;
    std::fstream fp;
    table t;

    read_buffer(const char *filename, int max_buffer_size):
        max_buffer_size(max_buffer_size),
        fp(filename, std::ios::in){
    }

    bool advance(row &r){
        bool status = get(r);
        pop();
        return status;
    }

    bool get(row &r){
        if (t.empty()){
            if (not buffer_in()){
                return false;
            }
        } 
        r = t.front();
        return true;
    }

    void pop(){
        if (not t.empty())
            t.pop();
    }

    bool buffer_in(){
        int current_size = 0;
        std::string line_buffer;
        while ( current_size < max_buffer_size ){
            if(getline(fp, line_buffer)){
                row r;
                std::stringstream stream;
                std::string cell;

                stream << line_buffer;

                while ( stream >> cell ){
                    r.push_back(cell);
                    current_size += cell.size();
                }

                t.push(r);
            } else {
                return (not t.empty());
            }
        }
        return true;
    }
};

struct write_buffer {
    int max_buffer_size;
    std::fstream fp;
    std::stringstream out_buffer;
    int current_size;

    write_buffer(const char *filename, int max_buffer_size):
        max_buffer_size(max_buffer_size),
        fp(filename, std::ios::out), current_size(0){
    }

    bool write(row &r){
        current_size += utils::print(out_buffer, r);
        if (current_size > max_buffer_size) {
            return flush();
        }
        return true;
    }

    bool flush(){
        if(fp << out_buffer.rdbuf()){
            out_buffer.str(std::string());
            current_size = 0;
            return true;
        }
        return false;
    }

    ~write_buffer(){
        flush();
    }
};

struct write_buffer_hard: write_buffer {
    write_buffer_hard(const char *filename, int max_buffer_size):
        write_buffer(filename, max_buffer_size){}

    bool write (row & r){
        current_size += utils::print(out_buffer, r);
        if ( current_size > max_buffer_size ){
            flush();
            return false;
        }
        return true;
    }
};

#endif
