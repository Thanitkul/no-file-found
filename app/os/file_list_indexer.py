'''
file_list_indexer.py

FileSearcher: 
        This function search for files and their path in the root directory and its subdirectories given the starting path and search string. It can handle regular search and wilecard search(*, ?, [], !, -, #).
        * Matches any number of characters. You can use the asterisk (*) anywhere in a character string.
        ? Matches a single alphabet in a specific position. 
        [] Matches characters within the brackets.
        ! Excludes characters inside the brackets.
        - Matches a range of characters. Remember to specify the characters in ascending order (A to Z, not Z to A).
        # Matches any single numeric character.

        Normal non-wildcard search:
            case insensitive, search for substring in filename

        The output format is in format [{"path": "path", "name": "name"}] .

Created by Phasit Thanitkul (Kane), 26 October 2023

'''

import os
import re
from typing import List, Dict

# function translate (to be called from FileSearcher)
# This function translate the search string to regex pattern.
# parameters:
#   pattern: the search string
#   is_wildcard: boolean to indicate whether the search string is wildcard or not
def translate(pattern: str, is_wildcard: bool) -> str:
    if not is_wildcard:
        return pattern.lower()

    i, n = 0, len(pattern)
    res = ''
    while i < n:
        char = pattern[i]
        i += 1
        if char == '*':
            res = res + '.*'
        elif char == '?':
            res = res + '[a-zA-Z]'
        elif char == '[':
            j = i
            if j < n and pattern[j] == '!':
                j += 1
            if j < n and pattern[j] == ']':
                j += 1
            while j < n and pattern[j] != ']':
                j += 1
            if j >= n:
                res = res + '\\['
            else:
                stuff = pattern[i:j].replace('\\', '\\\\')
                i = j + 1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                res = '%s[%s]' % (res, stuff)
        elif char == '#':
            res = res + '[0-9]'
        else:
            res = res + re.escape(char)
    return f'(?i){res}'

# function FileSearcher (to be called from file_search_engine.py)
# This function search for files and their path in the root directory and its subdirectories given the starting path and search string. 
# It can handle regular search and wilecard search(*, ?, [], !, -, #).
# parameters: 
#   starting_path: the path to start searching
#   search_string: the string to search for (can be wildcard)

def FileSearcher(starting_path: str, search_string: str) -> List[Dict[str, str]]:
    is_wildcard = any(char in search_string for char in '*?[]!-#')
    regex_pattern = translate(search_string, is_wildcard)
    if not is_wildcard:
        regex_pattern = f'.*{regex_pattern}.*'  # Wrap the pattern with .* for substring matching
    regex = re.compile(regex_pattern)
    matches = []
    for root, dirs, files in os.walk(starting_path):
        for filename in files:
            if regex.match(filename):
                matches.append({"path": os.path.join(root, filename), "name": filename})
    return matches


