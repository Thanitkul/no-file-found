'''
custom_tree_view.py

Create custom tree view's user interface and mechanic.

Created by Mo, 5 November, 2023.
'''

# Import from required library
from qtpy.QtWidgets import (QTreeView, QStyleOptionViewItem, QMessageBox)
from qtpy.QtGui import QPalette, QColor
from qtpy.QtCore import Qt, QModelIndex
import os

class CustomeTreeView(QTreeView):
    '''
    Initialize the custom tree view, set custom tree view's stylesheet
    and forbid expanding folder when clicking on it.
    Arguments:
        None
    '''
    def __init__(self, parent=None):
        super(CustomeTreeView, self).__init__(parent)
        # Set folder to collapse immediately if get expanded
        self.expanded.connect(self.collapseImmediately)

        # Initialize the clicked folder and file index
        # Value to keep track of the clicked folder index in this tree view
        self.clicked_folder_index = QModelIndex()

        # Value to keep track of the clicked file index in this tree view
        self.clicked_file_index = QModelIndex()
        
        # Set the stylesheet for the tree view
        self.setStyleSheet("""
            QTreeView::item:selected {
                background: transparent;
            }
            QTreeView::item:hover {
                background: #E0E0E0 !important;
            }
            QTreeView::item {
                color: black;
                outline: none !important;
            }
            QTreeView::focus {
                border: none !important;
                outline: none !important;
            }
            QTreeView { background: #ffffff; border: 1px solid #e0e0e0; border-radius: 5px; }        
        """)

    '''
    Highlight the clicked folder and file.
    Arguments (The value come from library):
        painter: QPainter
        options: QStyleOptionViewItem
        index: QModelIndex
    '''
    def drawRow(self, painter, options, index):
        # Use the original options to maintain the original style, including text color
        original_options = QStyleOptionViewItem(options)

        # Check if the current index is the clicked folder index
        if index == self.clicked_folder_index:
            # Set folder background to blue
            painter.save()
            color = QColor('#0067B4')
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawRect(options.rect)
            painter.restore()
            options.palette.setColor(QPalette.Text, Qt.black)
        
        # Check if the current index is the clicked file index
        if index == self.clicked_file_index:
            # Set file background to blue
            painter.save()
            color = QColor('#0067B4')
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawRect(options.rect)
            painter.restore()
            options.palette.setColor(QPalette.Text, Qt.black)

        # Call the original drawRow method to draw the item with the updated options
        super().drawRow(painter, original_options, index)

    '''
    Clear the highlighted folder.
    Arguments:
        None
    '''
    def clearFolderHighlight(self):
        # Set the clicked folder index to null
        self.clicked_folder_index = QModelIndex()

        # Update the tree view to trigger a repaint
        self.viewport().update()

    '''
    Clear the highlighted file.
    Arguments:
        None
    '''
    def clearFileHighlight(self):
        # Set the clicked file index to null
        self.clicked_file_index = QModelIndex()

        # Update the tree view to trigger a repaint
        self.viewport().update()

    '''
    Collapse the folder immediately when it get expanded.
    Arguments:
        index: QModelIndex
    '''
    def collapseImmediately(self, index):
        self.collapse(index)

    '''
    Handle the mouse press event.
    Arguments (The value come from library):
        event: QMouseEvent
    '''
    def mousePressEvent(self, event):
        # Get the index of the item that was clicked
        index = self.indexAt(event.pos())

        # Ensure the index is valid
        if not index.isValid():
            # If the click is on empty space, do nothing
            return
        
        # Check if the clicked item is a folder or a file
        if self.model().isDir(index):
            # Set the clicked folder index
            self.clicked_folder_index = index

            # Expand or collapse the folder
            self.expand(index) if not self.isExpanded(index) else self.collapse(index)
    
        else:
            # Set the clicked file index
            self.clicked_file_index = index
            super(CustomeTreeView, self).mousePressEvent(event)

    '''
    Expand the folder and check if the folder can be accessed.
    Arguments (The value come from library):
        index: QModelIndex
    '''
    def expand(self, index):
        # Check if the directory can be accessed before expanding it
        if not self.isDirReadable(index):
            # If the directory cannot be accessed, clear the folder highlight
            self.clearFolderHighlight()

            # Show a warning message
            QMessageBox.warning(self, "Access Denied", "You don't have permission to access this folder.")
            return
        super(CustomeTreeView, self).expand(index)

    '''
    Check if the folder can be accessed.
    Arguments (The value come from library):
        index: QModelIndex
    '''
    def isDirReadable(self, index):
        # Try to read the directory contents
        file_info = self.model().fileInfo(index)
        try:
            # Use the os.access method to check if the directory is readable
            # This is a simple check, there might be cases where it returns True
            # but you still can't read the directory due to more complex permission issues
            return os.access(file_info.absoluteFilePath(), os.R_OK)
        
        except Exception as e:
            # Log or handle the error as needed
            print(f"Error checking directory access: {e}")
            return False


