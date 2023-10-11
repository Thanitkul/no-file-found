'''
__main__.py

Gather all the widgets together and run the application.

Created by Mo, 30 September, 2023.
'''
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout

from .file_explorer.tree_list_generator import TreeListGenerator
from .file_explorer.file_search_engine import FileSearchEngine

import sys

class FileTreeViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Tree Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.tree_list_generator = TreeListGenerator()
        self.file_search_engine = FileSearchEngine()

        central_layout = QVBoxLayout(self)
        central_layout.addWidget(self.file_search_engine.search_bar)
        central_layout.addWidget(self.tree_list_generator.splitter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = FileTreeViewer()
    viewer.show()
    sys.exit(app.exec_())