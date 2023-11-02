import csv
from tkinter import filedialog

def exportAsCSV(csvColumnName, data):
        fileName = filedialog.asksaveasfilename(defaultextension=".csv",
                                                initialfile="export",
                                                filetypes=[("CSV Files", "*.csv"), ("All files", "*.*")])
        if fileName == "":
            print("Export cancelled")
            return
        with open(fileName, 'w', newline='') as file:
            writer = csv.writer(file) 
            writer.writerow(csvColumnName)
            writer.writerows(data)