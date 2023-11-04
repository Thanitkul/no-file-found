'''
tree_list_generator.py

Display file tree list, starting from root and 
when clicking open folder, a new file tree list which 
contain file inside that folder appear next to the previous tree list.

Created by Mo, 12 October, 2023.
'''
from qtpy.QtWidgets import QMainWindow, QTableWidgetItem, QTableWidget
from qtpy.QtCore import Qt


class FileAttributeView(QMainWindow):
    def __init__(self):
        super().__init__()

    def updateAttributeTable(self, attributes):
        self.attributeTable = QTableWidget()
        self.attributeTable.setStyleSheet(
            """
            QTableWidget { 
                background: #ffffff; 
                border: 1px solid #e0e0e0; 
                border-radius: 5px; 
            }
            QTableWidget::item {
                padding: 5px; /* Padding inside cells */
                border-right: 1px solid #d0d0d0; /* Right border for each cell */
            }
            QTableWidget::item:last-column { border-right: none; }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border-right: 1px solid #d0d0d0;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QHeaderView::section:last-column {
                border-right: none;
            }
            QTableWidget::focus {
                border: none !important;
                outline: none !important;
            }
            """
        )
        self.attributeTable.setFixedWidth(400)
        self.attributeTable.setColumnCount(2)
        self.attributeTable.setHorizontalHeaderLabels(['Attribute', 'Value'])
        self.attributeTable.horizontalHeader().setStretchLastSection(True)
        self.attributeTable.verticalHeader().setVisible(False)
        
        # Clear the existing attribute table
        self.attributeTable.setRowCount(0)

        # Populate the attribute table with the new attributes
        for key, value in attributes.items():
            rowPosition = self.attributeTable.rowCount()
            self.attributeTable.insertRow(rowPosition)
            
            key_item = QTableWidgetItem(key)
            value_item = QTableWidgetItem(value)
            
            # Make the cells non-editable
            key_item.setFlags(key_item.flags() ^ Qt.ItemIsEditable)
            value_item.setFlags(value_item.flags() ^ Qt.ItemIsEditable)
            
            self.attributeTable.setItem(rowPosition, 0, key_item)
            self.attributeTable.setItem(rowPosition, 1, value_item)

            # Increase the height of each row (you can adjust the value as needed)
            self.attributeTable.setRowHeight(rowPosition, 40)