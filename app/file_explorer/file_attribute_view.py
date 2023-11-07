'''
file_attribute_view.py

Create file attribute table and put attributes data into it.

Created by Mo, 12 October, 2023.
'''

# Import from required library
from qtpy.QtWidgets import QMainWindow, QTableWidgetItem, QTableWidget
from qtpy.QtCore import Qt

class FileAttributeView(QMainWindow):
    '''
    Initialize the file attribute table.
    Arguments:
        None
    '''
    def __init__(self):
        super().__init__()

    '''
    Update the attribute table with the new attributes.
    Arguments:
        attributes: a dictionary of attributes
    '''
    def updateAttributeTable(self, attributes):
        # Initialize the attribute table
        # Widget to display attributes table
        self.attributeTable = QTableWidget()

        # Set the stylesheet for the attribute table
        self.attributeTable.setStyleSheet(
            """
            QTableWidget { 
                border: 1px solid #e0e0e0; 
                border-radius: 2px; 
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

        # Set the header for the attribute table
        self.attributeTable.setHorizontalHeaderLabels(['Attribute', 'Value'])
        self.attributeTable.horizontalHeader().setStretchLastSection(True)
        self.attributeTable.verticalHeader().setVisible(False)
            
        # Enable word wrapping
        self.attributeTable.setWordWrap(True)

        # Clear the existing attribute table
        self.attributeTable.setRowCount(0)

        # Populate the attribute table with the new attributes
        for key, value in attributes.items():
            # Insert a new row at the bottom of the table
            rowPosition = self.attributeTable.rowCount()
            self.attributeTable.insertRow(rowPosition)

            # Create items for the key and value
            key_item = QTableWidgetItem(key)
            value_item = QTableWidgetItem(value)

            # Enable text alignment and word wrapping for the value item
            value_item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
            value_item.setFlags(value_item.flags() ^ Qt.ItemIsEditable)

            # Add items to the table
            self.attributeTable.setItem(rowPosition, 0, key_item)
            self.attributeTable.setItem(rowPosition, 1, value_item)

        # Adjust the row height automatically to fit the contents
        self.attributeTable.resizeRowsToContents()