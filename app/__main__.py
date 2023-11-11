'''
__main__.py

Gather all the components together and run the application.

Created by Mo, 30 September, 2023.
'''
import sys
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QVBoxLayout, QScrollArea

from app.file_explorer.tree_list_generator import TreeListGenerator
from app.file_explorer.file_search_engine import FileSearchEngine
from app.file_explorer.search_history_table import SearchHistoryTable


class FileTreeViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("No File Found")
        self.setGeometry(100, 100, 800, 600)

        self.treeListGenerator = TreeListGenerator()
        self.fileSearchEngine = FileSearchEngine(currentPath=self.treeListGenerator.getCurrentPath)
        self.searchHistoryTable = SearchHistoryTable()

        centralWidget = QWidget()
        centralLayout = QVBoxLayout(centralWidget)
        centralLayout.addWidget(self.treeListGenerator.backButton)
        centralLayout.addWidget(self.fileSearchEngine.searchBar)
        centralLayout.addWidget(self.treeListGenerator.treeViews)
        centralLayout.addWidget(self.fileSearchEngine.tree_widget)
        centralLayout.addWidget(self.searchHistoryTable.historyButton)
        
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(centralWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = FileTreeViewer()
    viewer.show()
    sys.exit(app.exec_())