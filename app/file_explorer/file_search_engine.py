from qtpy.QtWidgets import QLineEdit

class FileSearchEngine:
    def __init__(self):
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")