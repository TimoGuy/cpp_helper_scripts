# HEADER_EXT = '.h'
# SOURCE_EXT = '.cpp'

import argparse
from datetime import datetime
import re
import sys
from pathlib import Path


parser = argparse.ArgumentParser(prog='check_fn_defs',
                                 description='Checks for all function declarations and definitions '
                                             'and looks for missing links.')

parser.add_argument('search_recur_dir',
                    help='Directory to recursively search into.')

args = parser.parse_args()


if __name__ == '__main__':
    # ns_class_name: str = args
    pass
