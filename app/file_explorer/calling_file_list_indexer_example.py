'''
calling_file_list_indexer_example.py

This file is an example of how to call the file_list_indexer.so library.

recompile by "cc -fPIC -shared -o file_list_indexer.so file_list_indexer.c"

Created by Phasit Thanitkul (Kane), 11 October 2023

'''

# import ctypes and .so library
from ctypes import *
# open the file_list_indexer.so library from cwd + ../os/file_list_indexer.so

file_list_indexer = CDLL("../os/file_list_indexer.so")



#call the function FileSearcher from file_list_indexer.so

# you have to specify the return type of the function
# in this case, it is a c_char_p (string)
file_list_indexer.FileSearcher.restype = c_char_p

# call the function FileSearcher from file_list_indexer.so
rawSearchResult = file_list_indexer.FileSearcher(b"../..", b"list")
print("debug: rawSearchResult: ", id(rawSearchResult))

print("Search result returned from file_list_indexer.so library:")
print(rawSearchResult, "\n")

#convert to python string
searchResult = rawSearchResult.decode("utf-8")
print("Search result converted to python string:")
print(searchResult, "\n")

import json
#convert to python dictionary
searchResultJson = json.loads(searchResult)
print("debug: searchResult: ", id(searchResult))
print("debug: searchResultJson: ", id(searchResultJson))
print(f"Pointer in Python: {hex(cast(rawSearchResult, c_void_p).value)}")


#free memory using the original pointer
file_list_indexer.FreeMemory(rawSearchResult)
print("Search result converted to python dictionary:")
print(searchResultJson, "\n")




