from qtpy.QtWidgets import QPushButton , QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import csv

tableColumnName = ['File name', 'File path', 'File size', 'File last modified', 'Search starting directory', 'Search term', 'Search date']
csvColumnName = ['fileName', 'filePath', 'fileSize', 'fileLastModified', 'searchStartingDirectory', 'searchTerm', 'searchDate']
testData = [
    ['Test.png', 'C:\\Desktop\\Test.png', '1.2 MB', '12/10/2023 12:00:00 AM', 'C:\\', 'Test', '12/10/2023 12:00:00 AM'],
    ['Test2.png', 'C:\\Desktop\\Test2.png', '1.2 MB', '12/10/2023 12:00:00 AM', 'C:\\', 'Test', '12/10/2023 12:00:00 AM'],
]
row = testData.__len__()
col = testData[0].__len__()

class SearchHistoryTable:
    def __init__(self):
        super().__init__()
        self.historyButton = QPushButton("Search History")
        self.historyButton.clicked.connect(self.historyButtonClicked)
        self.exportButton = QPushButton("Export as CSV")
        self.exportButton.clicked.connect(self.exportAsCSV)
        self.tableWidget = QTableWidget()
    
    def initUI(self):
        self.searchTableWindow = QMainWindow()
        self.searchTableWindow.setWindowTitle("Search History")
        self.searchTableWindow.setGeometry(100, 100, 800, 600)

        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.exportButton)
        self.searchTableWindow.setCentralWidget(centralWidget)
        self.setupTable()
        
    def setupTable(self):
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(col)
        self.tableWidget.setHorizontalHeaderLabels(tableColumnName)
        for r in range(row):
            for c in range(col):
                item = QTableWidgetItem(testData[r][c])
                self.tableWidget.setItem(r, c, item)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        

    def historyButtonClicked(self):
        self.initUI()
        self.searchTableWindow.show()

    def exportAsCSV(self):
        fileName = 'export.csv'
        with open(fileName, 'w', newline='') as file:
            writer = csv.writer(file) 
            writer.writerow(columnName)
            writer.writerows(testData) 
    
