'''
file_search_temp.py

This is a temp function to perform file search in python because me pooh i have problem with kane implementation in C and calling it from the python
Created by pooh, 30 September, 2023.
'''
import glob
from typing  import Union


def search_directory(path: str, query: Union[str, None]) -> list:
    search =  path+ "/**/" + query
    # print(search)
    return glob.glob(search,recursive=True)


if __name__ == "__main__":
    search_directory("/home/pooh/code/", "__main__.py")