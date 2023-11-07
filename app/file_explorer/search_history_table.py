'''
search_history_table.py

Adds a button to view search history, and displays the search history in a table,
then adds a export function to export the search history as a CSV file.

Created by Korn Visaltanachoti (Bank), 14 October 2023
'''
from qtpy.QtWidgets import QPushButton , QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import csv
from tkinter import filedialog
from ..history.csv_exporter import exportAsCSV

# Defines the column names for the search history table
tableColumnName = ['File name', 'File path', 'File size', 'File last modified', 'Search starting directory', 'Search term', 'Search date']

# List for storing the search history data
searchHistoryData = []

# This class creates the search history table
class SearchHistoryTable:
    def __init__(self):
        super().__init__()
        # Adds the search history button to the main window
        self.historyButton = QPushButton("Search History")
        self.historyButton.clicked.connect(self.historyButtonClicked)

        # Adds the export button to the search history window
        self.exportButton = QPushButton("Export as CSV")
        # Connects the button to the export function
        # lambda is used otherwise the function will be called when the button is created
        self.exportButton.clicked.connect(lambda: exportAsCSV(searchHistoryData))
        self.tableWidget = QTableWidget()
        self.initUI()
    
    # Creates the search history window
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
    
    # Prepares the data for the history table
    def setupTable(self):
        row = len(searchHistoryData)
        col = len(tableColumnName)
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(col)
        self.tableWidget.setHorizontalHeaderLabels(tableColumnName)
        # Adds the data to the table
        for r in range(row):
            for c in range(col):
                item = QTableWidgetItem(searchHistoryData[r][c])
                self.tableWidget.setItem(r, c, item)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        
    # Displays the search history table
    def historyButtonClicked(self):
        self.searchTableWindow.show()

# This function is called by file_search_engine.py to add the search history to the table
# Arguments:
#   fileName: the name of the file
#   filePath: the path of the file
#   fileSize: the size of the file
#   fileLastModified: the last modified date of the file
#   searchStartingDirectory: the directory that the search started from
#   searchTerm: the search term
#   searchDate: the date that the search was performed
def saveHistory(fileName, filePath, fileSize, fileLastModified, searchStartingDirectory, searchTerm, searchDate):
    searchHistoryData.append([fileName, filePath, fileSize, fileLastModified, searchStartingDirectory, searchTerm, searchDate])