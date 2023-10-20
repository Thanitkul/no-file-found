'''
__main__.py

Gather all the components together and run the application.

Created by Mo, 30 September, 2023.
'''
import sys
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QVBoxLayout, QScrollArea

from .file_explorer.tree_list_generator import TreeListGenerator
from .file_explorer.file_search_engine import FileSearchEngine
from .file_explorer.search_history_table import SearchHistoryTable


class FileTreeViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Tree Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.treeListGenerator = TreeListGenerator()
        self.fileSearchEngine = FileSearchEngine()
        self.searchHistoryTable = SearchHistoryTable()
    
        centralWidget = QWidget()
        centralLayout = QVBoxLayout(centralWidget)
        centralLayout.addWidget(self.fileSearchEngine.searchBar)
        centralLayout.addWidget(self.treeListGenerator.splitter)
        centralLayout.addWidget(self.searchHistoryTable.historyButton)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(centralWidget)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(scrollArea)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = FileTreeViewer()
    viewer.show()
    sys.exit(app.exec_())