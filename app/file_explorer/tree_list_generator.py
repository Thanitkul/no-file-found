'''
tree_list_generator.py

Display file tree list, starting from root and
when clicking open folder, a new file tree list which
contain file inside that folder appear next to the previous tree list.

Created by Mo, 12 October, 2023.
'''
from qtpy.QtWidgets import (QMainWindow, QSplitter, QMessageBox,
                            QHBoxLayout, QPushButton, QScrollArea, QLabel)
from qtpy.QtGui import QIcon
from qtpy.QtCore import Qt
import os

# Import the file attribute view
from .file_attribute_view import FileAttributeView
from .custom_tree_view import CustomeTreeView, CustomFileSystemModel
    
class TreeListGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.splitter = QSplitter(Qt.Horizontal)
        self.treeViews = QScrollArea()
        self.treeViews.setStyleSheet("QScrollArea { padding: 5px; border: none;}")
        self.treeViews.setWidgetResizable(True)
        self.treeViews.setWidget(self.splitter)
        
        # Create a horizontal layout for the navigation bar
        self.layout = QHBoxLayout()
        self.displayingFile = None
        self.currentPath = ''
        self.treeViewList = []  # List to keep track of tree view
        self.initUI()

    '''
    Initialize attribute table and first tree list
    Arguments:
        None
    '''

    def initUI(self):
        # Call the class to display file attributes from file_attribute_view.py
        self.attributeViewFile = FileAttributeView()
        # Create the initial file tree list
        self.addFileTreeList(self.splitter, '')
        # Set the splitter as the central widget
        self.setCentralWidget(self.treeViews)
        # Create a back button
        self.backButton()

    
    def addFileTreeList(self, splitter, startingPath):
        self.currentPath = startingPath
        print(self.currentPath)
        # Create a new file tree list
        self.treeView = CustomeTreeView(self)
        self.treeView.setFixedWidth(250)
        self.model = CustomFileSystemModel(self.treeView)
        self.model.setRootPath(startingPath)

        self.treeView.setModel(self.model)
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)
        # Disable scroll bars for the tree view
        self.treeView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.treeView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Set the root path
        self.treeView.setRootIndex(self.model.index(startingPath))

        self.treeView.setHeaderHidden(True)  # Optional: Hide header columns
        self.treeView.setColumnWidth(0, 250)  # Optional: Set the column width
        # self.treeView.setColumnWidth(0, self.treeView.columnWidth(0) / 2)

        # Add the new file tree list to the splitter
        splitter.addWidget(self.treeView)
        # Connect the expanded signal to an event handler
        self.treeView.expanded.connect(self.openFolder)
        self.treeView.clicked.connect(self.selectFile)
        
        self.treeViewList.append(self.treeView)
        self.scrollRight()


    def openFolder(self, index):
        if self.displayingFile is not None:
            # Remove the latest widget
            self.removeLatestWidgetFromSplitter()
            self.displayingFile = None
            # self.treeView.clearSelection()

        # Get the file path from the model
        folderPath = self.model.filePath(index)
        # Event handler for when a folder is opened (expanded)
        folderPath = self.model.filePath(index)

        # Find which treeView the folder was opened from
        originTreeView = self.sender()

        # Find the position of this treeView in the treeViewList
        position = self.treeViewList.index(originTreeView)

        # Remove every tree list after the current one
        for i in range(len(self.treeViewList) - 1, position, -1):
            widget_to_remove = self.splitter.widget(i)
            widget_to_remove.hide()
            self.treeViewList[i].deleteLater()
            self.treeViewList.pop()
        
        # Check if the directory is empty
        try :
            if not os.listdir(folderPath):
                # Create a label with the message
                emptyLabel = QLabel("No files")
                emptyLabel.setAlignment(Qt.AlignCenter)
                emptyLabel.setFixedWidth(250)
                emptyLabel.setStyleSheet("QLabel { background: #ffffff; border: 1px solid #e0e0e0; border-radius: 5px;}")

                # Add the label to the splitter
                self.splitter.addWidget(emptyLabel)

                # Add the label to the tree view list for management
                self.treeViewList.append(emptyLabel)
                self.scrollRight()
                return
        except (FileNotFoundError, PermissionError):
            self.treeViewList[-1].clearFolderHighlight()
            QMessageBox.warning(self, "Access Denied", "You don't have permission to access this folder.")
            return

        # Now add the new tree list for the opened folder
        self.addFileTreeList(self.splitter, folderPath)
        print(f"Folder opened: {folderPath}")
       

    def selectFile(self, index):
        if index.isValid() and not self.model.isDir(index):
            # Event handler for displaying file attributes
            filePath = self.model.filePath(index)
            print('display1',filePath, self.displayingFile)
            if filePath == self.displayingFile:
                # Remove the latest widget
                self.removeLatestWidgetFromSplitter()
                self.displayingFile = None

            else:
                if self.displayingFile is None:
                    # Find which treeView the folder was opened from
                    originTreeView = self.sender()
                    # Find the position of this treeView in the treeViewList
                    position = self.treeViewList.index(originTreeView)
                    # Remove every tree list after the current one
                    for i in range(len(self.treeViewList) - 1, position, -1):
                        widget_to_remove = self.splitter.widget(i)
                        widget_to_remove.hide()
                        self.treeViewList[i].deleteLater()
                        self.treeViewList.pop()
                    # Get and display file attributes
                    attributes = {
                        'File Name': filePath.split('/')[-1],
                        'Last Modified': self.model.lastModified(index).toString(),
                        'File Size': f"{self.model.size(index) / 1024:.2f} KB"
                    }
                    print(attributes)
                    self.displayingFile = filePath
                    print('display2',self.displayingFile)
                    self.attributeViewFile.updateAttributeTable(attributes)
                    self.attributeTable = self.attributeViewFile.attributeTable
                    self.splitter.addWidget(self.attributeTable)
                    self.treeViewList.append(self.attributeTable)
                else:
                    # Remove the latest widget
                    self.removeLatestWidgetFromSplitter()
                    # Get and display file attributes
                    attributes = {
                        'File Name': filePath.split('/')[-1],
                        'Last Modified': self.model.lastModified(index).toString(),
                        'File Size': f"{self.model.size(index) / 1024:.2f} KB"
                    }
                    print(attributes)
                    self.displayingFile = filePath
                    print('display2',self.displayingFile)
                    self.attributeViewFile.updateAttributeTable(attributes)
                    self.attributeTable = self.attributeViewFile.attributeTable
                    self.splitter.addWidget(self.attributeTable)
                    self.treeViewList.append(self.attributeTable)
        self.scrollRight()
    def scrollRight(self):
        # Ensure that the splitter is updated before scrolling
        self.splitter.adjustSize()
        # Get the horizontal scrollbar of the scroll area and set its value to the maximum
        horizontal_scrollbar = self.treeViews.horizontalScrollBar()
        horizontal_scrollbar.setValue(horizontal_scrollbar.maximum())
    
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
        self.backButton.setFocusPolicy(Qt.NoFocus)
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
        self.removeLatestWidgetFromSplitter()
        # If there's at least one tree view left, clear its highlight
        if self.treeViewList:
            self.treeViewList[-1].clearFolderHighlight()

    def removeLatestWidgetFromSplitter(self):
        # Check if there are widgets in the splitter to remove
        if self.splitter.count() > 1:
            # Get the last widget in the splitter
            widget_to_remove = self.splitter.widget(self.splitter.count() - 1)
            # Hide the widget before removing it from the splitter
            widget_to_remove.hide()
            # Remove the widget from the tree view list
            self.treeViewList.pop()
            # Now delete the widget
            widget_to_remove.deleteLater()

