'''
tree_list_generator.py

Display file tree list, starting from root and 
when clicking open folder, a new file tree list which 
contain file inside that folder appear next to the previous tree list.

Created by Mo, 12 October, 2023.
'''
from qtpy.QtWidgets import QMainWindow, QTreeView, QFileSystemModel, QSplitter, QTableWidgetItem, QTableWidget, QWidget, QVBoxLayout, QSizePolicy
from qtpy.QtCore import Qt

class TreeListGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.splitter = QSplitter(Qt.Horizontal)
        self.initUI()
    
    def initUI(self):
        # Create a table to display file attributes
        self.attributeTable = QTableWidget()
        self.attributeTable.setFixedWidth(500)
        self.attributeTable.setColumnCount(2)
        self.attributeTable.setHorizontalHeaderLabels(['Attribute', 'Value'])
        self.attributeTable.horizontalHeader().setStretchLastSection(True)
        # Set the vertical size policy to expanding
        self.attributeTable.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)



        # Create the initial file tree list
        self.addFileTreeList(self.splitter, '', isInitial=True)
        self.splitter.addWidget(self.attributeTable)

        self.setCentralWidget(self.splitter)

    def folderOpened(self, index):
        # Event handler for when a folder is opened (expanded)
        folderPath = self.model.filePath(index)
        
        # Create a splitter to divide the window into parts for each tree view

        # Create the initial file tree list
        self.addFileTreeList(self.splitter, folderPath)
        print(f"Folder opened: {folderPath}")

    def addFileTreeList(self, splitter, startingPath, isInitial=False):
        # Create a new file tree list
        self.treeView = QTreeView(self)
        self.treeView.setFixedWidth(250)
        self.model = QFileSystemModel()
        self.model.setRootPath(startingPath)

        self.treeView.setModel(self.model)
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)

        self.treeView.setRootIndex(self.model.index(startingPath))  # Set the root path


        self.treeView.setHeaderHidden(True)  # Optional: Hide header columns
        self.treeView.setColumnWidth(0, 250)  # Optional: Set the column width
        # self.treeView.setColumnWidth(0, self.treeView.columnWidth(0) / 2)

        # Add the new file tree list to the splitter
        if isInitial:
            splitter.addWidget(self.treeView)
        else:
            self.splitter.insertWidget(self.splitter.count() - 1, self.treeView)
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

        # Get and display file attributes
        attributes = {
            'File Name': filePath.split('/')[-1],
            'Last Modified': self.model.lastModified(index).toString(),
            'File Size': f"{self.model.size(index) / 1024:.2f} KB"
        }
        print(attributes)

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
