from nbformat import read as nb_read
from nbformat import write as nb_write
import argparse
import os
import glob
from typing import List


def check_file(filename, inplace):
    with open(filename, 'r') as f:
        nb = nb_read(f, as_version=4)

    for cell in reversed(nb['cells']):
        cell['outputs'] = []
        cell['execution_count'] = None
        if cell['source'] == '':
            nb['cells'].remove(cell)

    if inplace is False:
        file_name, ext = os.path.splitext(filename)
        file_name = file_name + "_cleared" + ext
        filename = file_name

    with open(filename, 'w', encoding='utf8') as f:
        nb_write(nb, f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="filename")
    parser.add_argument('--inplace', '-p', action='store_true', help="filename")
    parser.add_argument('--quite', '-q', action='store_true', help="filename")
    args = parser.parse_args()

    verbose = args.quite
    filename = args.filename
    files: List[str] = glob.glob(filename)

    for file in files:
        if not(verbose):
            print(file)
        check_file(file, args.inplace)


if __name__ == "__main__":
    exit(main())
