from qtpy.QtWidgets import (QTreeView, QFileSystemModel, 
                            QStyleOptionViewItem, QMessageBox)
from qtpy.QtGui import QPalette, QColor
from qtpy.QtCore import Qt, QModelIndex
import os

class CustomeTreeView(QTreeView):
    def __init__(self, parent=None):
        super(CustomeTreeView, self).__init__(parent)
        self.expanded.connect(self.collapseImmediately)
        self.clicked_folder_index = QModelIndex()  # No index at start
        
        # Set the stylesheet to have a transparent selection background color
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

    def drawRow(self, painter, options, index):
        # Use the original options to maintain the original style, including text color
        original_options = QStyleOptionViewItem(options)

        if index == self.clicked_folder_index:
            painter.save()
            color = QColor('#0067B4')
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawRect(options.rect)
            painter.restore()

            # Set the text color to black
            options.palette.setColor(QPalette.Text, Qt.black)
                # If the item is selected, change the background to blue

            # Set the text color to white for better contrast
            options.palette.setColor(QPalette.Text, Qt.white)
        else:
            # If the item is not selected, keep the original background
            options.palette.setColor(QPalette.Text, Qt.black)
        # Now let the base class draw the row with the possibly modified options
        super().drawRow(painter, original_options, index)

    def clearFolderHighlight(self):
        self.clicked_folder_index = QModelIndex()
        self.viewport().update()  # This will trigger a repaint of the tree view

    def collapseImmediately(self, index):
        self.collapse(index)

    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            # If the click is on empty space, do nothing
            return

        # Ensure we only expand/collapse directories
        if self.model().isDir(index):
            self.clicked_folder_index = index
            # Instead of directly toggling, use the expand method which checks for read access
            self.expand(index) if not self.isExpanded(index) else self.collapse(index)
        else:
            super(CustomeTreeView, self).mousePressEvent(event)

    def expand(self, index):
        # Check if the directory can be accessed before expanding it
        if not self.isDirReadable(index):
            self.clearFolderHighlight()
            QMessageBox.warning(self, "Access Denied", "You don't have permission to access this folder.")
            return
        super(CustomeTreeView, self).expand(index)

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

class CustomFileSystemModel(QFileSystemModel):
    def __init__(self, tree_view):
        super().__init__()
        self.tree_view = tree_view

