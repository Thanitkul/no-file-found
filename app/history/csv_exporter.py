'''
csv_exporter.py

Module for exporting the search history table as a CSV file

Created by Korn Visaltanachoti (Bank), 6 November 2023
'''
import csv
from tkinter import filedialog

# Defines the column names for the CSV file
csvColumnName = ['fileName', 'filePath', 'fileSize', 'fileLastModified', 'searchStartingDirectory', 'searchTerm', 'searchDate']

# Exports the search history table as a CSV file
def exportAsCSV(data):
        # Asks the user for the file name and location
        fileName = filedialog.asksaveasfilename(defaultextension=".csv",
                                                initialfile="export",
                                                filetypes=[("CSV Files", "*.csv"), ("All files", "*.*")])
        # If the user cancels the export, the function will return
        if fileName == "":
            print("Export cancelled")
            return
        # Writes the data to the CSV file
        with open(fileName, 'w', newline='') as file:
            writer = csv.writer(file) 
            writer.writerow(csvColumnName)
            writer.writerows(data)