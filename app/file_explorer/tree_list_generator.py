'''
tree_list_generator.py

Display file tree list, starting from root and 
when clicking open folder, a new file tree list which 
contain file inside that folder appear next to the previous tree list.

Created by Mo, 12 October, 2023.
'''
from qtpy.QtWidgets import QMainWindow, QTreeView, QFileSystemModel
from qtpy.QtCore import Qt

class TreeListGenerator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tree_view = QTreeView(self)
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.tree_view.setModel(self.model)

        self.tree_view.setRootIndex(self.model.index("/"))  # Set the root path

        self.tree_view.setHeaderHidden(True)  # Optional: Hide header columns
        self.tree_view.setColumnWidth(0, 250)  # Optional: Set the column width
