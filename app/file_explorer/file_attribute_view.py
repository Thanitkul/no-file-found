'''
tree_list_generator.py

Display file tree list, starting from root and 
when clicking open folder, a new file tree list which 
contain file inside that folder appear next to the previous tree list.

Created by Mo, 12 October, 2023.
'''
from qtpy.QtWidgets import QMainWindow, QTreeView, QFileSystemModel, QSplitter, QTableWidgetItem, QTableWidget, QSizePolicy
from qtpy.QtCore import Qt


class FileAttributeView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    '''
    Initialize attribute table and first tree list
    Arguments:
        None
    '''
    def initUI(self):
        # Create a table to display file attributes
        self.displayingFile = None
        self.attributeTable = QTableWidget()
        self.attributeTable.setFixedWidth(500)
        self.attributeTable.setColumnCount(2)
        self.attributeTable.setHorizontalHeaderLabels(['Attribute', 'Value'])
        self.attributeTable.horizontalHeader().setStretchLastSection(True)

    def updateAttributeTable(self, attributes):
        # Clear the existing attribute table
        self.attributeTable.setRowCount(0)

        # Populate the attribute table with the new attributes
        for key, value in attributes.items():
            print(key, value)
            rowPosition = self.attributeTable.rowCount()
            self.attributeTable.insertRow(rowPosition)
            self.attributeTable.setItem(rowPosition, 0, QTableWidgetItem(key))
            self.attributeTable.setItem(
                rowPosition, 1, QTableWidgetItem(value))
        
