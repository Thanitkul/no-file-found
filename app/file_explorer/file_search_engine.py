'''
file_search_engine.py

This file create a qt widget and interface with the serch code interface

created by pooh, 18 oct, 2023
'''

from qtpy.QtWidgets import QLineEdit, QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout,QMainWindow, QSplitter, QFileIconProvider
from ctypes import *
from qtpy.QtGui import QStandardItem, QIcon, QStandardItemModel
import json
from app.os.file_search_temp import search_directory
import os
from qtpy.QtCore import Qt
import sys


class CustomFileTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.icon_provider = QFileIconProvider()

    def add_directory(self, path, parent_item):
        if os.path.isfile(path):
            item_path = path
            item = QTreeWidgetItem(parent_item)
            item.setText(0, path)
            item.setIcon(0, self.icon_provider.icon(QFileIconProvider.File))
            return
        for item_name in os.listdir(path):
            item_path = os.path.join(path, item_name)
            item = QTreeWidgetItem(parent_item)
            item.setText(0, item_name)
            
            if os.path.isdir(item_path):
                item.setIcon(0, self.icon_provider.icon(QFileIconProvider.Folder))
                self.add_directory(item_path, item)
            else:
                item.setIcon(0, self.icon_provider.icon(QFileIconProvider.File))


class FileSearchEngine(QMainWindow):
    def __init__(self):
        super().__init__()
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search...")
        self.file_list_indexer = CDLL("./app/os/file_list_indexer.so")
        self.file_list_indexer.FileSearcher.restype = c_char_p
        self.searchBar.returnPressed.connect(self.search_folders)
        self.tree_widget = CustomFileTreeWidget()
        self.tree_widget.setHeaderLabel("Search Results")

    def search(self, current_path: str = "/home/pooh/"):
        querry = self.searchBar.text()
        # querry = "*.png"
        # search_results = self.file_list_indexer.FileSearcher(b"..", b"*.py")
        # print(search_results)
        # return json.loads(search_results.decode("utf-8"))
    
    def search_folders(self):
        print("i been ran")
        search_path = self.searchBar.text()
        parent_path = self.windowFilePath()
        print(parent_path)
        result = search_directory(parent_path,search_path)
        print(result)
        if result == None:
            print("no file not found")
            return
        print("routing finish")
        self.tree_widget.clear()  # Clear previous results
        for i in result:
            print(i)
            self.tree_widget.add_directory(i,self.tree_widget.invisibleRootItem())