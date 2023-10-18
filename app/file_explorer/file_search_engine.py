from qtpy.QtWidgets import QLineEdit
from ctypes import *
import json

class FileSearchEngine:
    def __init__(self):
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search...")
        self.file_list_indexer = CDLL("./app/os/file_list_indexer.so")
        self.file_list_indexer.FileSearcher.restype = c_char_p
        self.searchBar.textChanged.connect(self.search)

    def search(self, current_path: str = "/home/pooh/"):
        querry = self.searchBar.text()
        # querry = "*.png"
        search_results = self.file_list_indexer.FileSearcher(b"/home/pooh/code/", b".py")
        print(search_results)
        return json.loads(search_results.decode("utf-8"))
    