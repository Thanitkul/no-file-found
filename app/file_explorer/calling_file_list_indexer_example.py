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


# you have to specify the return type of the function
# in this case, it is a c_char_p (string)
file_list_indexer.FileListFinder.restype = c_char_p

print("Calling file_list_indexer.so library...")

# call the function FileListFinder from file_list_indexer.so
# and pass the path of the folder you want to index in bytes using b"..."
# the function will return a string of the indexed file list
# in the format of JSON
fileList = file_list_indexer.FileListFinder(b"..")

print("File list returned from file_list_indexer.so library:")
print(fileList, "\n")

#convert to python string
fileList = fileList.decode("utf-8")
print("File list converted to python string:")
print(fileList, "\n")

#convert to python dictionary
import json
fileList = json.loads(fileList)
print("File list converted to python dictionary:")
print(fileList, "\n")

#call the function FileSearcher from file_list_indexer.so

# you have to specify the return type of the function
# in this case, it is a c_char_p (string)
file_list_indexer.FileSearcher.restype = c_char_p


searchResult = file_list_indexer.FileSearcher(b"..", b"c?lling_[c-g][a-r]le_*")
print("Search result returned from file_list_indexer.so library:")
print(searchResult, "\n")

#convert to python string
searchResult = searchResult.decode("utf-8")
print("Search result converted to python string:")
print(searchResult, "\n")

#convert to python dictionary
searchResult = json.loads(searchResult)
print("Search result converted to python dictionary:")
print(searchResult, "\n")



