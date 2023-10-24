from qtpy.QtWidgets import QPushButton, QMainWindow

import csv

testData = [
    ['searchTerm', 'searchDate', 'fileResult', 'filePath', 'fileLastModified'],
    ['Homework', '2020-10-12', 'Homework 1', 'TestPath', '2020-10-12 12:00:00']
]

class SearchHistoryTable:
    def __init__(self):
        super().__init__()
        self.historyButton = QPushButton("Search History")
        self.historyButton.clicked.connect(self.historyButtonClicked)

        self.exportButton = QPushButton("Export as CSV")
        self.exportButton.clicked.connect(self.exportAsCSV)
    
    def initUI(self):
        
        self.searchTableWindow = QMainWindow()
        self.searchTableWindow.setWindowTitle("Search History")
        self.searchTableWindow.setGeometry(100, 100, 400, 300)
        
        self.searchTableWindow.setCentralWidget(self.exportButton)


    def historyButtonClicked(self):
        self.initUI()
        self.searchTableWindow.show()

    def exportAsCSV(self):
        fileName = 'export.csv'
        with open(fileName, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(testData)