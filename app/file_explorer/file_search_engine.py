'''
file_search_engine.py

This file create a qt widget and interface with the serch code interface

created by pooh, 18 oct, 2023
'''

from qtpy.QtWidgets import QLineEdit, QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout,QMainWindow, QSplitter, QFileIconProvider
from qtpy.QtGui import QStandardItem, QIcon, QStandardItemModel
import os
from app.os.file_searcher import FileSearcher
from qtpy.QtCore import Qt
from datetime import date, datetime
import time
from .search_history_table import saveHistory


class CustomFileTreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.icon_provider = QFileIconProvider()

    def add_nofilefound(self, parent):
        item = QTreeWidgetItem(parent)
        item.setText(0, "No file found")
        item.setIcon(0, self.icon_provider.icon(QFileIconProvider.File))

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
    def __init__(self, currentPath: callable):
        super().__init__()
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.returnPressed.connect(self.search_folders)
        self.tree_widget = CustomFileTreeWidget()
        self.tree_widget.setHeaderLabel("Search Results")
        self.currentPath = currentPath
        self.is_searching = False
        # Set the stylesheet to remove border lines
        self.tree_widget.setStyleSheet(
            """
            QTreeWidget {
                border: none; /* Remove border */
                outline: 0;   /* Remove focus outline */
                border-radius: 2px;
            }
            """
        )

    
    def search_folders(self):
        search_path = self.searchBar.text()
        print(self.currentPath())
        result = FileSearcher(self.currentPath(),search_path)
        print(result)
        self.tree_widget.clear()  # Clear previous results
        if len(result) == 0:
            print("no file not found")
            self.tree_widget.add_nofilefound(self.tree_widget.invisibleRootItem())
            saveHistory(fileName="-",filePath="-",fileLastModified=0,searchStartingDirectory=self.currentPath(),
                            searchTerm=search_path, searchDate=time.time(),fileSize=0)
            return
        print("routing finish")
        for i in result:
            self.tree_widget.add_directory(i['path'],self.tree_widget.invisibleRootItem())
            if i != None:
                saveHistory(fileName=i['name'], filePath=i['path'], fileLastModified=os.path.getmtime(i['path']), 
                        searchStartingDirectory=self.currentPath(), searchTerm=search_path, searchDate=time.time(), fileSize=os.path.getsize(i["path"]))

    def isSearching(self):
        return self.is_searching