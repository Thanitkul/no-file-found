'''
file_search_engine.py

This file create a qt widget and interface with the serch code interface

created by pooh, 18 oct, 2023
'''

from qtpy.QtWidgets import QLineEdit, QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout,QMainWindow, QSplitter, QFileIconProvider
from ctypes import *
from qtpy.QtGui import QStandardItem, QIcon, QStandardItemModel
import json
import os
from app.os.file_searcher import FileSearcher
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
    def __init__(self, treeListInstance: callable, collaps: callable):
        super().__init__()
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.returnPressed.connect(self.search_folders)
        self.tree_widget = CustomFileTreeWidget()
        self.tree_widget.setHeaderLabel("Search Results")
        self.treeListInstance = treeListInstance
        self.is_searching = False
        self.collaps = collaps
    
    def search_folders(self):
        search_path = self.searchBar.text()
        result = FileSearcher(self.treeListInstance.getCurrentPath(),search_path)
        print(result)
        if result == None:
            print("no file not found")
            return
        print("routing finish")
        self.tree_widget.clear()  # Clear previous results
        for i in result:
            print(i)
            self.tree_widget.add_directory(i['path'],self.tree_widget.invisibleRootItem())
        
        self.collaps(self.treeListInstance.treeViews)

