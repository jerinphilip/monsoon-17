from engine import Engine
import sys

if __name__ == '__main__':
    _, command = sys.argv
    cursor = Engine("files")
    results = cursor.execute(command)
    print("\n"+"-"*10)
    for table in results:
        print(table)

