'''
tree_list_generator.py

Display file tree list, starting from root and
when clicking open folder, a new file tree list which
contain file inside that folder appear next to the previous tree list.

Created by Mo, 12 October, 2023.
'''
from qtpy.QtWidgets import (QMainWindow, QTreeView, QFileSystemModel, QSplitter,
                            QTableWidgetItem, QTableWidget, QHBoxLayout, QPushButton)
from qtpy.QtGui import QIcon
from qtpy.QtCore import Qt
import os


class TreeListGenerator(QMainWindow):

    def __init__(self):
        super().__init__()
        self.splitter = QSplitter(Qt.Horizontal)
        # Create a horizontal layout for the navigation bar
        self.layout = QHBoxLayout()
        self.treeViewList = []  # List to keep track of tree view
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

        # Create a back button
        self.backButton()
    
    def backButton(self):
        # Create a back button
        self.backButton = QPushButton()

        # Get the absolute path to the directory where your script is located
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Specify the relative path to your SVG image file
        image_path = os.path.join(script_directory, "..",
                                "assets", "icons", "back_button.svg")

        # Create a QIcon using the image_path
        icon = QIcon(image_path)
        self.backButton.setIcon(icon)
        # Set the size of the circular button
        self.backButton.setFixedSize(30, 30)
        self.backButton.setStyleSheet(
            "QPushButton { border: none; border-radius: 15px; background-color: #ffffff; }"
            "QPushButton:hover { background-color: #005A9D; }"
        )
        self.backButton.clicked.connect(self.goBack)

        # Add the back button to the layout
        self.layout.addWidget(self.backButton, alignment=Qt.AlignLeft)

        # Add some spacing to separate the back button from other elements
        self.layout.addSpacing(10)

        # Set the layout for the navigation bar
        self.setLayout(self.layout)

    def goBack(self):
        # Event handler for when the back button is clicked
        # Remove the latest widget
        if self.splitter.count() > 1:
            self.splitter.replaceWidget(self.splitter.count() - 1, None)
            # Delete the widget to release its resources
            self.splitter.widget(self.splitter.count() - 1).deleteLater()
            self.treeViewList.pop()

    def folderOpened(self, index):
        self.treeViewList[len(self.treeViewList) - 1].collapse(index)
        # Event handler for when a folder is opened (expanded)
        folderPath = self.model.filePath(index)
        # Add the opened folder to the list of opened folders
        self.treeViewList.append(self.treeView)
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
        
        self.treeViewList.append(self.treeView)

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
