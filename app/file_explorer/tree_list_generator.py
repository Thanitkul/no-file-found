'''
tree_list_generator.py

Display file tree list, starting from root and
when clicking open folder, a new file tree list which
contain file inside that folder appear next to the previous tree list.

Created by Mo, 12 October, 2023.
'''

# Import the required modules
from qtpy.QtWidgets import (QMainWindow, QSplitter, QMessageBox, QFileSystemModel,
                            QHBoxLayout, QPushButton, QScrollArea, QLabel)
from qtpy.QtGui import QIcon
from qtpy.QtCore import Qt
import os

# Import the file attribute view
from .file_attribute_view import FileAttributeView
from .custom_tree_view import customeTreeView
    
class TreeListGenerator(QMainWindow):
    '''
    Initialize the tree list generator
    Arguments:
        None
    '''
    def __init__(self):
        super().__init__()
        # List storing the tree views
        self.splitter = QSplitter(Qt.Horizontal)
        # Widget to make splitter scrollable
        self.treeViews = QScrollArea()
        self.treeViews.setStyleSheet("QScrollArea { padding: 5px; border: none;}")
        # Set the scroll area as the widget to display
        self.treeViews.setWidgetResizable(True)
        self.treeViews.setWidget(self.splitter)
        
        # Create a horizontal layout for the navigation bar
        # Container for the back button
        self.layout = QHBoxLayout()
        # string to keep track of the file being displayed
        self.displayingFile = None
        # string to keep track of the current path
        self.currentPath = ''
        # List to keep track of tree view
        self.treeViewList = []  # List to keep track of tree view
        self.initUI()

    '''
    Initialize attribute table, first tree list and back button
    Arguments:
        None
    '''
    def initUI(self):
        # Call the class to display file attributes from file_attribute_view.py
        self.attributeViewFile = FileAttributeView()
        # Create the initial file tree list
        self.addNewTreeView(self.splitter, '')
        # Set the splitter as the central widget
        self.setCentralWidget(self.treeViews)
        # Create a back button
        self.backButton()

    '''
    Add a new tree view to the splitter
    Arguments:
        splitter: the splitter to add the tree view to
        startingPath: the path to start the tree view from
    '''
    def addNewTreeView(self, splitter, startingPath):
        # Set the current path to the starting path
        self.currentPath = startingPath
        # Create a new file tree list
        # Widget to display the file tree list
        self.treeView = customeTreeView(self)
        self.treeView.setFixedWidth(250)
        # Create a model for the file system
        # Value stroing os data
        self.model = QFileSystemModel(self.treeView)
        self.model.setRootPath(startingPath)
        self.treeView.setModel(self.model)

        # Hide the columns for file size, file type and date modified
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)

        # Disable scroll bars for the tree view
        self.treeView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.treeView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Set the root path
        self.treeView.setRootIndex(self.model.index(startingPath))

        # Hide header columns
        self.treeView.setHeaderHidden(True)  
        # Optional: Set the column width
        self.treeView.setColumnWidth(0, 250)  

        # Add the new file tree list to the splitter
        splitter.addWidget(self.treeView)

        # Connect the expanded signal to an event handler
        self.treeView.expanded.connect(self.openFolder)
        self.treeView.clicked.connect(self.selectFile)
        
        # Add the new tree view to the tree view list for keeping track
        self.treeViewList.append(self.treeView)

        # Scroll to the right to show the latest tree view
        self.scrollRight()

    '''
    Event handler for when a folder is opened (expanded)
    Arguments:
        index: the index of the folder that was opened
    '''
    def openFolder(self, index):
        # Check if a file is being displayed
        if self.displayingFile is not None:
            # Remove the latest widget from the splitter
            self.removeLatestWidgetFromSplitter()
            self.displayingFile = None
            # Clear the highlight from the file
            self.treeViewList[-1].clearFileHighlight()

        # Get the file path from the model
        folderPath = self.model.filePath(index)

        # Find which treeView the folder was opened from
        originTreeView = self.sender()

        # Find the position of this treeView in the treeViewList
        position = self.treeViewList.index(originTreeView)

        # Remove every tree view after the one that was clicked
        for i in range(len(self.treeViewList) - 1, position, -1):
            # Get the widget to remove
            widget_to_remove = self.splitter.widget(i)
            widget_to_remove.hide()
            self.treeViewList[i].deleteLater()
            self.treeViewList.pop()
        
        
        try :
            # Check if the directory is empty
            if not os.listdir(folderPath):
                # Create a label with the message "No files"
                # Widget to display the empty label
                emptyLabel = QLabel("No files")
                emptyLabel.setAlignment(Qt.AlignCenter)
                emptyLabel.setFixedWidth(250)
                emptyLabel.setStyleSheet("QLabel { background: #ffffff; border: 1px solid #e0e0e0; border-radius: 5px;}")

                # Add the label to the splitter
                self.splitter.addWidget(emptyLabel)

                # Add the label to the tree view list for keeping track
                self.treeViewList.append(emptyLabel)

                # Scroll to the right to show the latest tree view
                self.scrollRight()
                return
        # If the user doesn't have permission to access the folder
        except (FileNotFoundError, PermissionError):
            # Remove the highlight from the folder
            self.treeViewList[-1].clearFolderHighlight()
            # Show a warning message
            QMessageBox.warning(self, "Access Denied", "You don't have permission to access this folder.")
            return

        # Now add the new tree view for showing the files in clicked folder
        self.addNewTreeView(self.splitter, folderPath)
       
    '''
    Event handler for when a file is selected
    Arguments:
        index: the index of the file that was selected
    '''
    def selectFile(self, index):
        # Check if the index is file not folder
        if index.isValid() and not self.model.isDir(index):
            # Get the file path from the model
            filePath = self.model.filePath(index)
            # Check if the file is already being displayed
            if filePath == self.displayingFile:
                # Remove the latest widget
                self.removeLatestWidgetFromSplitter()
                self.displayingFile = None
            else:
                # Check if a file is being displayed
                if self.displayingFile is None:
                    # Find which treeView the folder was opened from
                    originTreeView = self.sender()

                    # Find the position of this treeView in the treeViewList
                    position = self.treeViewList.index(originTreeView)

                    # Remove every tree list after the one that was clicked
                    for i in range(len(self.treeViewList) - 1, position, -1):
                        widget_to_remove = self.splitter.widget(i)
                        widget_to_remove.hide()
                        self.treeViewList[i].deleteLater()
                        self.treeViewList.pop()
                        
                    # Remove the highlight from the folder
                    self.treeViewList[-1].clearFolderHighlight()

                    # Get and display file attributes
                    attributes = {
                        'File Name': filePath.split('/')[-1],
                        'Last Modified': self.model.lastModified(index).toString(),
                        'File Size': f"{self.model.size(index) / 1024:.2f} KB"
                    }

                    # Set the file path as the currently displaying file
                    self.displayingFile = filePath

                    # Update the attribute table
                    self.attributeViewFile.updateAttributeTable(attributes)
                    self.attributeTable = self.attributeViewFile.attributeTable

                    # Add the attribute table to the splitter
                    self.splitter.addWidget(self.attributeTable)

                    # Add the attribute table to the tree view list for keeping track
                    self.treeViewList.append(self.attributeTable)
                else:
                    # Remove the opening attribute table
                    self.removeLatestWidgetFromSplitter()

                    # Get and display file attributes
                    attributes = {
                        'File Name': filePath.split('/')[-1],
                        'Last Modified': self.model.lastModified(index).toString(),
                        'File Size': f"{self.model.size(index) / 1024:.2f} KB"
                    }

                    # Set the file path as the currently displaying file
                    self.displayingFile = filePath

                    # Update the attribute table
                    self.attributeViewFile.updateAttributeTable(attributes)
                    self.attributeTable = self.attributeViewFile.attributeTable

                    # Add the attribute table to the splitter
                    self.splitter.addWidget(self.attributeTable)

                    # Add the attribute table to the tree view list for keeping track
                    self.treeViewList.append(self.attributeTable)

        # Scroll to the right to show the attribute table or the latest tree view
        self.scrollRight()

    '''
    Scroll to the rightest position of the splitter
    Arguments:
        None
    '''
    def scrollRight(self):
        # Ensure that the splitter is updated before scrolling
        self.splitter.adjustSize()

        # Get the horizontal scrollbar of the scroll area and set its value to the maximum
        horizontal_scrollbar = self.treeViews.horizontalScrollBar()
        horizontal_scrollbar.setValue(horizontal_scrollbar.maximum())
    
    '''
    Create a back button UI
    Arguments:
        None
    '''
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

        # Set the focus policy to no focus
        self.backButton.setFocusPolicy(Qt.NoFocus)

        # Set the style sheet for the back button
        self.backButton.setStyleSheet(
            "QPushButton { border: none; border-radius: 15px; background-color: #ffffff; }"
            "QPushButton:hover { background-color: #005A9D; }"
        )

        # Connect the back button to an event handler
        self.backButton.clicked.connect(self.goBack)

        self.layout.addWidget(self.backButton, alignment=Qt.AlignLeft)
        self.layout.addSpacing(10)
        self.setLayout(self.layout)

    '''
    Event handler for when the back button is clicked
    Arguments:
        None
    '''
    def goBack(self):
        # Remove the latest widget
        self.removeLatestWidgetFromSplitter()

        # If there's at least one tree view left, clear its highlight
        if self.treeViewList:
            self.treeViewList[-1].clearFolderHighlight()

    '''
    Remove the latest widget from the splitter
    Arguments:
        None
    '''
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

    '''
    Get the current path
    Arguments:
        None
    '''
    def getCurrentPath(self):
        return self.currentPath
