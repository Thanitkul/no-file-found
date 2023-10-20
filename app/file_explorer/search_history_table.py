from qtpy.QtWidgets import QPushButton, QTableWidget, QMainWindow, QVBoxLayout

class SearchHistoryTable:
    def __init__(self):
        super().__init__()
        self.historyButton = QPushButton("Search History")
        self.historyButton.clicked.connect(self.historyButtonClicked)
    
    def initUI(self):
        # Create a table to display file attributes
        self.searchTableWindow = QMainWindow()
        self.searchTableWindow.setWindowTitle("Search History")
        self.searchTableWindow.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        layout.addWidget(self.searchTable)

    def historyButtonClicked(self):
        self.initUI()
        self.searchTableWindow.show()