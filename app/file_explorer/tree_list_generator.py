'''
tree_list_generator.py

Display file tree list, starting from root and 
when clicking open folder, a new file tree list which 
contain file inside that folder appear next to the previous tree list.

Created by Mo, 12 October, 2023.
'''
from qtpy.QtWidgets import QMainWindow, QTreeView, QFileSystemModel, QSplitter
from qtpy.QtCore import Qt

class TreeListGenerator(QMainWindow):
    def __init__(self):
        super().__init()
        self.splitter = QSplitter(Qt.Horizontal)

        self.addFileTreeList(self.splitter, '')
    
    def folderOpened(self, index):
        # Event handler for when a folder is opened (expanded)
        folderPath = self.model.filePath(index)
        
        # Create a splitter to divide the window into parts for each tree view

        # Create the initial file tree list
        self.addFileTreeList(self.splitter, folderPath)
        print(f"Folder opened: {folderPath}")

    def addFileTreeList(self, splitter, startingPath):
        # Create a new file tree list
        self.treeView = QTreeView(self)
        self.treeView.setFixedWidth(250)
        self.model = QFileSystemModel()
        self.model.setRootPath(startingPath)
        self.treeView.setModel(self.model)

        self.treeView.setRootIndex(self.model.index(startingPath))  # Set the root path

        self.treeView.setHeaderHidden(True)  # Optional: Hide header columns
        self.treeView.setColumnWidth(0, 250)  # Optional: Set the column width
        self.treeView.setColumnWidth(0, self.treeView.columnWidth(0) / 2)

        # Add the new file tree list to the splitter
        splitter.addWidget(self.treeView)
        # Connect the expanded signal to an event handler
        self.treeView.expanded.connect(self.folderOpened)