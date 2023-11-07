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

        self.treeListGenerator = TreeListGenerator(addTreeViews=self.add)
        self.fileSearchEngine = FileSearchEngine(treeListInstance=self.treeListGenerator, collapsTreeViews=self.remove)
        self.searchHistoryTable = SearchHistoryTable()

        self.centralWidget = QWidget()
        self.centralLayout = QVBoxLayout(self.centralWidget)
        self.centralLayout.addWidget(self.treeListGenerator.backButton)
        self.centralLayout.addWidget(self.fileSearchEngine.searchBar)
        self.centralLayout.addWidget(self.treeListGenerator.treeViews)
        self.centralLayout.addWidget(self.searchHistoryTable.historyButton)
        


        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.centralWidget)


    def remove(self, widget):
        self.centralLayout.removeWidget(widget)
        # self.centralLayout.addWidget(self.fileSearchEngine.tree_widget)



    def add(self):
        # print("test/")
        self.centralLayout.removeWidget(self.fileSearchEngine.tree_widget)
        # print("ok")
        self.centralLayout.addWidget(self.treeListGenerator.treeViews)
        self.fileSearchEngine.remove_widget




if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = FileTreeViewer()
    viewer.show()
    sys.exit(app.exec_())