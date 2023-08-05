import sys
from donno import notes 

def main():
    if len(sys.argv) <= 2:
        sys.exit("Add at least one word for search")

    CMD = sys.argv[1]
    PARAM_LIST = sys.argv[2:]

    if CMD == 's':
        path_list = notes.simple_search(PARAM_LIST)
        if len(path_list) == 0:
            sys.exit("No match found")
        else:
            print(notes.note_list(path_list))

