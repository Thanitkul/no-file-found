'''
__main__.py

Gather all the components together and run the application.

Created by Mo, 30 September, 2023.
'''
import sys
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout

from .file_explorer.tree_list_generator import TreeListGenerator
from .file_explorer.file_search_engine import FileSearchEngine

class FileTreeViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Tree Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.treeListGenerator = TreeListGenerator()
        self.fileSearchEngine = FileSearchEngine()

        centralLayout = QVBoxLayout(self)
        centralLayout.addWidget(self.fileSearchEngine.searchBar)
        centralLayout.addWidget(self.treeListGenerator.splitter)
        centralLayout.addWidget(self.fileSearchEngine.tree_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = FileTreeViewer()
    viewer.show()
    sys.exit(app.exec_())