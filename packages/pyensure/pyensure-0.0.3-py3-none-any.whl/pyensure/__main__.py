import runpy
import sys

from pyensure import hook

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print ("Provide the script to run as the first argument")
        sys.exit(1)

    file_path = sys.argv[1]
    hook()
    runpy.run_path(file_path, run_name='__main__')