HEADER_EXT = '.h'
SOURCE_EXT = '.cpp'
AUTHOR_NAME = 'Thea Bennett'

import argparse
from datetime import datetime
import re
import sys
from pathlib import Path


parser = argparse.ArgumentParser(prog='make_class',
                                 description='Creates a c++ class header/source pair')

parser.add_argument('namespaced_class_name',
                    help='Class name within namespace(s) delimited with \"::\"')
parser.add_argument('filename', help='Filename stem of header/source pair. Path is relative.')

args = parser.parse_args()


if __name__ == '__main__':
    ns_class_name: str = args.namespaced_class_name
    filename: str      = args.filename

    # Check that class name is within some kind of namespace.
    ns_cls_parts = ns_class_name.split('::')
    if len(ns_cls_parts) < 2:
        print("ERROR: Namespaced class name is not within a namespace.")
        sys.exit(1)
    
    for x in ns_cls_parts:
        if len(x.strip()) != len(x):
            print(f"ERROR: Do not include whitespace such as in this token: {x.strip()}")
            sys.exit(2)

        if len(x.strip()) == 0:
            print(f"ERROR: Do not include empty namespaces (even global namespace).")
            sys.exit(3)

        if re.search(r"\W", x.strip()):
            print("ERROR: Non-word character found in tokens.")
            sys.exit(4)


    # Ensure that filenames do not exist.
    header_path = Path(filename + HEADER_EXT)
    source_path = Path(filename + SOURCE_EXT)

    for x in [header_path, source_path]:
        if x.exists():
            print(f"ERROR: \"{x.absolute().as_posix()}\" already exists. Delete and retry.")
            sys.exit(5)

    # Prep.
    current_year = str(datetime.now().year)
    file_heading = \
        "////////////////////////////////////////////////////////////////////////////////////////////////////\n" \
        f"/// @copyright {current_year} {AUTHOR_NAME}\n"                                                         \
        "////////////////////////////////////////////////////////////////////////////////////////////////////\n" \
        "/// @brief @TODO @FIXME Add brief here.\n"                                                              \
        "////////////////////////////////////////////////////////////////////////////////////////////////////"

    # Create header file str.
    header_contents = \
        f'{file_heading}\n' \
        '#pragma once\n\n'

    ns_befores = ''
    ns_afters = ''

    for ns_part in ns_cls_parts[:-1]:
        ns_befores += \
            f'namespace {ns_part}\n' \
            '{\n'
        ns_afters = \
            '}' f'  // namespace {ns_part}\n' \
            + ns_afters

    class_content = \
        f'class {ns_cls_parts[-1]}\n' \
        '{\n' \
        '};\n'

    header_contents += ns_befores + '\n' + class_content + '\n' + ns_afters + '\n'

    # Create source file str.
    source_contents = \
        f'{file_heading}\n' \
        f'#include \"{header_path.name}\"\n\n'

    # Write contents.
    with open(header_path, 'w') as f:
        f.write(header_contents)

    with open(source_path, 'w') as f:
        f.write(source_contents)
