'''
calling_file_list_indexer_example.py

This file is an example of how to call the file_list_indexer.so library.

Created by Phasit Thanitkul (Kane), 11 October 2023

'''

# import ctypes and .so library
from ctypes import *
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
