'''
tree_list_generator.py

Display file tree list, starting from root and
when clicking open folder, a new file tree list which
contain file inside that folder appear next to the previous tree list.

Created by Mo, 12 October, 2023.
'''
from qtpy.QtWidgets import (QMainWindow, QTreeView,
                            QFileSystemModel, QSplitter,
                            QTableWidgetItem, QTableWidget)
from qtpy.QtCore import Qt


class TreeListGenerator(QMainWindow):

    def __init__(self):
        super().__init__()
        self.splitter = QSplitter(Qt.Horizontal)
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

        # Create the initial file tree list
        self.addFileTreeList(self.splitter, '')

        # Set the splitter as the central widget
        self.setCentralWidget(self.splitter)

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
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)

        # Set the root path
        self.treeView.setRootIndex(self.model.index(startingPath))

        self.treeView.setHeaderHidden(True)  # Optional: Hide header columns
        self.treeView.setColumnWidth(0, 250)  # Optional: Set the column width
        # self.treeView.setColumnWidth(0, self.treeView.columnWidth(0) / 2)

        # Add the new file tree list to the splitter
        splitter.addWidget(self.treeView)
        # Connect the expanded signal to an event handler
        self.treeView.expanded.connect(self.folderOpened)
        self.treeView.clicked.connect(self.fileClicked)

    def fileClicked(self, index):
        # Event handler for when a file is clicked
        if index.isValid() and not self.model.isDir(index):
            # File clicked, display attributes
            self.fileSelected(index)

    def fileSelected(self, index):
        # Event handler for displaying file attributes
        filePath = self.model.filePath(index)
        if filePath == self.displayingFile:

            # Assuming splitter is your QSplitter instance
            latestWidget = self.splitter.widget(
                self.splitter.count() - 1)  # Get the latest widget
            # Remove the latest widget
            self.splitter.replaceWidget(self.splitter.count(), None)
            latestWidget.deleteLater()  # Delete the widget to release its resources

        else:
            # Get and display file attributes
            attributes = {
                'File Name': filePath.split('/')[-1],
                'Last Modified': self.model.lastModified(index).toString(),
                'File Size': f"{self.model.size(index) / 1024:.2f} KB"
            }
            print(attributes)
            self.displayingFile = filePath
            self.updateAttributeTable(attributes)

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
        self.splitter.addWidget(self.attributeTable)
