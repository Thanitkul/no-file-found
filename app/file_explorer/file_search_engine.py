from qtpy.QtWidgets import QLineEdit

class FileSearchEngine:
    def __init__(self):
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search...")