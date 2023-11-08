'''
file_searcher.py

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
        # For non-wildcard, escape the pattern and return it for case-insensitive search
        return re.escape(pattern)
    else:
        # If the search string is wildcard, translate the search string to regex pattern
        i, n = 0, len(pattern)
        res = ''
        # Loop through the search string
        while i < n:
            # Get the current character
            char = pattern[i]
            # Increment the index
            i += 1
            # If the current character is *, add .* to the pattern
            if char == '*':
                res = res + '.*'
            # If the current character is ?, add [a-zA-Z] to the pattern
            elif char == '?':
                res = res + '[a-zA-Z]'
            # If the current character is [, add [ to the pattern
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
            # If the current character is !, add [^a-zA-Z] to the pattern
            elif char == '#':
                res = res + '[0-9]'
            # If the current character is -, add - to the pattern
            else:
                res = res + re.escape(char)
        return f'(?i){res}', True

# function FileSearcher (to be called from file_search_engine.py)
# This function search for files and their path in the root directory and its subdirectories given the starting path and search string. 
# It can handle regular search and wilecard search(*, ?, [], !, -, #).
# parameters: 
#   starting_path: the path to start searching
#   search_string: the string to search for (can be wildcard)
def FileSearcher(starting_path: str, search_string: str) -> List[Dict[str, str]]:
    is_wildcard = any(char in search_string for char in '*?[]!-#')
    regex_pattern = translate(search_string, is_wildcard)

    # Compile the pattern with re.IGNORECASE for non-wildcard, without it for wildcard
    if not is_wildcard:
        regex = re.compile(f'.*{regex_pattern}.*', re.IGNORECASE)
    else:
        regex = re.compile(f'(?i){regex_pattern}')

    matches = []
    for root, dirs, files in os.walk(starting_path):
        for filename in files:
            if regex.match(filename):
                matches.append({"path": os.path.join(root, filename), "name": filename})
    print(matches)
    return matches