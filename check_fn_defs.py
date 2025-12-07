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


def check_search_dir_exists() -> bool:
    search_dir = args.search_recur_dir

    sdp = Path(search_dir)

    return (sdp.exists() and sdp.is_dir())


def find_existing_files() -> list[Path]:
    SEARCH_EXTENSIONS = ['h',
                         'hpp',
                         'ixx',  # I think this is for modules???
                         'c',
                         'cxx',
                         'cpp']
    search_dir = args.search_recur_dir

    all_found_files = []
    for search_ext in SEARCH_EXTENSIONS:
        # Convert `search_ext` to case-insensitive extension.
        case_insensitive_ext = '*.'
        for ext_char in search_ext:
            case_insensitive_ext += f'[{ext_char.lower()}{ext_char.upper()}]'

        # Search directory for extension.
        files = list(Path(search_dir).rglob(case_insensitive_ext))
        all_found_files.extend(files)

    return all_found_files


def extract_tokens(buf: str) -> list[str]:
    MODE_CODE          = 0
    MODE_LINE_COMMENT  = 1
    MODE_BLOCK_COMMENT = 2
    MODE_SING_QUOT_STR = 3
    MODE_DOUB_QUOT_STR = 4
    MODE_PREPROC       = 5
    mode = MODE_CODE  # See above for cases.

    started_token = False
    tokens = []

    cur = 0
    while cur < len(buf):
        # Code mode.
        if mode == MODE_CODE:
            # Look for mode switch.
            if buf[cur:cur+2] == '//':
                mode = MODE_LINE_COMMENT
                cur += 2
            if buf[cur:cur+2] == '/*':
                mode = MODE_BLOCK_COMMENT
                cur += 2
            elif buf[cur:cur+1] == '\'':
                mode = MODE_SING_QUOT_STR
                cur += 1
            elif buf[cur:cur+1] == '\"':
                mode = MODE_DOUB_QUOT_STR
                cur += 1
            elif buf[cur:cur+1] == '#':
                # Ensure that this is the first in the line.
                line_has_non_ws = False

                back_cur = cur-1
                while back_cur >= 0:
                    if buf[back_cur] == '\n':
                        # Finish search.
                        break
                    elif not buf[back_cur].isspace():
                        # Failed. End.
                        line_has_non_ws = True
                        break
                    else:
                        # Keep searching until get to beginning of line or find a whitespace (bad!!!)
                        back_cur -= 1

                if not line_has_non_ws:
                    mode = MODE_PREPROC
                    cur += 1
                else:
                    print("ERROR: \"#\" token found but token is not first in line after whitespace.")
                    sys.exit(2)
            else:
                # Commit in code mode.
                cur_char = buf[cur:cur+1]
                cur += 1

                if re.search(r"\w", cur_char):
                    # Token!!
                    if not started_token:
                        started_token = True
                        tokens.append('')
                    tokens[-1] += cur_char
                else:
                    started_token = False
                    if len(cur_char.strip()) > 0:
                        tokens.append(cur_char)
        # Line-comment mode.
        elif mode == MODE_LINE_COMMENT:
            # Look for end of line.
            if buf[cur:cur+1] == '\n':
                mode = MODE_CODE
                cur += 1
            elif buf[cur:cur+2] == '\r\n':
                mode = MODE_CODE
                cur += 2
            else:
                cur += 1
        # Block-comment mode.
        elif mode == MODE_BLOCK_COMMENT:
            # Look for end of block.
            if buf[cur:cur+2] == '*/':
                mode = MODE_CODE
                cur += 2
            else:
                cur += 1
        # Single-quote string mode.
        elif mode == MODE_SING_QUOT_STR:
            # Look for single quote without escape.
            if buf[cur:cur+2] == '\\\'':
                # Continue bc is escape.
                cur += 2
            elif buf[cur:cur+1] == '\'':
                mode = MODE_CODE
                cur += 1
            else:
                cur += 1
        # Double-quote string mode.
        elif mode == MODE_DOUB_QUOT_STR:
            # Look for double quote without escape.
            if buf[cur:cur+2] == '\\\"':
                # Continue bc is escape.
                cur += 2
            elif buf[cur:cur+1] == '\"':
                mode = MODE_CODE
                cur += 1
            else:
                cur += 1
        # Preprocessor mode.
        elif mode == MODE_PREPROC:
            # Look for end of line.
            if buf[cur:cur+1] == '\n':
                mode = MODE_CODE
                cur += 1
            elif buf[cur:cur+2] == '\r\n':
                mode = MODE_CODE
                cur += 2
            else:
                cur += 1

    return tokens


class Type_decl:
    candidates: list[str]

class Param_decl:
    param_type: Type_decl
    param_name: str

class Function_decl:
    return_type: Type_decl
    func_name: str
    param_list: list[Param_decl]
    pass  # @TODO: FIGURE THIS OUT!!


def search_file_for_declarations(file: Path) -> list[str]:
    declarations = []

    with open(file, 'r', encoding="utf8") as f:
        f_buf = f.read()
        tokens = extract_tokens(f_buf)

        # Find function declarations and definitions.

        cur = 0
        while cur < len(tokens):
            # Check if is a function.


        ns_nest = []  # What namespace you're in. Empty is global namespace.

        pass

    return declarations


if __name__ == '__main__':
    if not check_search_dir_exists():
        print("ERROR: Search dir does not exist!")
        sys.exit(1)

    # Find all files to search into.
    all_files = find_existing_files()
    for x in all_files:
        file_decls = search_file_for_declarations(x)

    # ns_class_name: str = args
    pass
