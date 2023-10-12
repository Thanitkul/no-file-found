'''
calling_file_list_indexer_example.py

This file is an example of how to call the file_list_indexer.so library.

Created by Phasit Thanitkul (Kane), 11 October 2023

'''

# import ctypes and .so library
from ctypes import *
file_attribute_data = CDLL("../os/file_attribute_data.so")

# you have to specify the return type of the function
# in this case, it is a c_char_p (string)
file_attribute_data.GetFileAttribute.restype = c_char_p

print("Calling file_attribute_data.so library...")
fileAttribute =  file_attribute_data.GetFileAttribute(b"./file_search_engine.py")
print("File attribute returned from file_attribute_data.so library:")
print(fileAttribute, "\n")


#convert to python string
fileAttribute = fileAttribute.decode("utf-8")
print("File attribute converted to python string:")
print(fileAttribute, "\n")

#convert to python dictionary
import json
fileAttribute = json.loads(fileAttribute)
print("File attribute converted to python dictionary:")
print(fileAttribute, "\n")



