import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDesktopWidget, QLabel, QPushButton, QDialog, QVBoxLayout,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit, QWidget, QHBoxLayout,
    QAbstractItemView
)
from PyQt5.QtGui import QIcon, QPainter, QPen, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QDate, QSize

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Pet Care"
        self.setStyleSheet("background-color: #2F4156")
        self.pet_data = []  # To store data

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        #window size
        self.setFixedSize(800, 600)

        #centers the window upon running the code
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        #window icon
        self.setWindowIcon(QIcon('animals.ico'))

        #add the create button 
        self.addCreateButton()

        #create table to display data
        self.createTable()

        # Add the left navigation bar
        self.addNavigationBar()

        # Set the default header to "Vaccination"
        self.onNavButtonClick("Vaccination")

    #table for displaying added item / displays user input
    def createTable(self):
        self.table = QTableWidget(self)
        self.table.setRowCount(0)  
        self.table.setColumnCount(3)  
        self.table.setStyleSheet("background-color: #FFFFFF; border: 1px solid #D9D9D9;")
        
        # Column widths 
        self.table.setColumnWidth(0, 150)  # Date
        self.table.setColumnWidth(1, 200)  # Vaccine / Remarks / Medicine
        self.table.setColumnWidth(2, 100)  # Action (for buttons)

        # Column resize behavior
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Size of the table
        self.table.setFixedSize(565, 277)  
        
        # Position of the table
        self.table.move(200, 279)

        # Hide row numbers
        self.table.verticalHeader().setVisible(False)

        # No highlight
        self.table.setSelectionMode(QAbstractItemView.NoSelection)



    #Create Button
    def addCreateButton(self):
        self.create_button = QPushButton(self)
        self.create_button.setFixedSize(60, 60)
        self.create_button.setStyleSheet("""
            QPushButton {
                background-color: #567C8D;
                border-radius: 30px;
                border: 2px solid #D9D9D9;
            }
            QPushButton:hover {
                background-color: #6B92A2;
            }
        """)
        
        self.create_button.setIcon(QIcon('create.png'))
        self.create_button.setIconSize(self.create_button.size())
        self.create_button.clicked.connect(self.showAddItemModal)

        # Ensure the window size is correct
        window_width = self.width()
        window_height = self.height()

        # Position the button at the bottom-right of the window
        button_x = window_width - self.create_button.width() - 20  
        button_y = window_height - self.create_button.height() - 20  
        self.create_button.move(button_x, button_y)

    # Update Table Headers based on selected category
    def updateTableHeader(self, category):
        if category == "Vaccination":
            self.table.setColumnCount(3)  
            self.table.setHorizontalHeaderLabels(["Date", "Vaccine", "Action"])
        elif category == "Vet Visits":
            self.table.setColumnCount(3)  
            self.table.setHorizontalHeaderLabels(["Date", "Remarks", "Action"])
        elif category == "Medication":
            self.table.setColumnCount(4)  
            self.table.setHorizontalHeaderLabels(["Date", "Medicine", "Dosage", "Action"])


    #Modal for Create Button
    def showAddItemModal(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Item")
        dialog.setFixedSize(400, 250)
        dialog.setStyleSheet("background-color: #FFFFFF; color: #2F4156;")

        layout = QVBoxLayout(dialog)

         # Date Label and Input 
        date_label = QLabel("DATE:")
        date_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(date_label)

        # Use QDateEdit for the Date input
        date_input = QDateEdit(self)
        date_input.setObjectName("date_input")
        date_input.setDisplayFormat("yyyy-MM-dd")  
        date_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
        date_input.setDate(QDate.currentDate())  # Set the date to today's date
        layout.addWidget(date_input)

        # Vaccine Label and Input
        vaccine_label = QLabel("VACCINE:")
        vaccine_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(vaccine_label)

        vaccine_input = QLineEdit()
        vaccine_input.setObjectName("vaccine_input")
        vaccine_input.setPlaceholderText("Enter vaccine name...")
        vaccine_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
        layout.addWidget(vaccine_input)

        # Add button
        add_button = QPushButton("Add")
        add_button.setStyleSheet("""
                QPushButton {
                    background-color: #567C8D;
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #6B92A2;
                }
            """)
        
        def validateAndAddItem():
            # Check if the date or vaccine fields are empty
            is_valid = True

            # Check if the date is empty
            if date_input.text().strip() == "":
                date_input.setStyleSheet("padding: 5px; border: 1px solid red; border-radius: 4px;")
                is_valid = False
            else:
                date_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")

            # Check if the vaccine name is empty
            if vaccine_input.text().strip() == "":
                vaccine_input.setStyleSheet("padding: 5px; border: 1px solid red; border-radius: 4px;")
                is_valid = False
            else:
                vaccine_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")

            # If both fields are valid, add the item and close the dialog
            if is_valid:
                self.addItem(date_input.date().toString("yyyy-MM-dd"), vaccine_input.text())
                dialog.accept()  # Close the dialog
        
       # Connect the "Add" button to the validation function
        add_button.clicked.connect(validateAndAddItem)

        layout.addWidget(add_button)

        # opens the modal
        dialog.exec_()

    def addItem(self, date, vaccine, dosage=None):
        """Add a new row to the table. If dosage is provided, use 4 columns, otherwise 3."""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(date))

        if dosage:  
            self.table.setItem(row_position, 1, QTableWidgetItem(vaccine))  
            self.table.setItem(row_position, 2, QTableWidgetItem(dosage))
            
            self.table.setCellWidget(row_position, 3, self.createActionButtons(row_position))
        else:  
            self.table.setItem(row_position, 1, QTableWidgetItem(vaccine))  
            self.table.setCellWidget(row_position, 2, self.createActionButtons(row_position))


    def createActionButtons(self, row_position):
        """Creates action buttons (Edit/Delete) for the given row."""
        action_widget = QWidget(self)
        action_layout = QHBoxLayout(action_widget)

        # "Edit" button
        edit_button = QPushButton(self)
        edit_button.setIcon(QIcon('edit.png'))
        edit_button.setIconSize(QSize(18, 18))  # icon size
        edit_button.setFixedSize(23, 23)  # button size
        edit_button.setStyleSheet("""QPushButton { background: transparent; border: none; padding: 0px; } QPushButton:hover { background-color: #D9D9D9; border-radius: 4px; }""")
        edit_button.clicked.connect(lambda: self.editRow(row_position))

        # "Delete" button
        delete_button = QPushButton(self)
        delete_button.setIcon(QIcon('delete.png'))
        delete_button.setIconSize(QSize(21, 21))  # icon size
        delete_button.setFixedSize(23, 23)  # button size
        delete_button.setStyleSheet("""QPushButton { background: transparent; border: none; padding: 0px; } QPushButton:hover { background-color: #D9D9D9; border-radius: 4px; }""")
        delete_button.clicked.connect(lambda: self.deleteRow(row_position))

        action_layout.addWidget(edit_button)
        action_layout.addWidget(delete_button)

        action_widget.setLayout(action_layout)
        return action_widget

    #for delete button, deletes the row
    def deleteRow(self, row_position):
        """Delete the row at the given position."""
        self.table.removeRow(row_position)

    #for edit button, edits the row data
    def editRow(self, row_position):
        """Edit the row data at the given position."""
        # Get current data from the row
        current_date = self.table.item(row_position, 0).text()
        current_vaccine = self.table.item(row_position, 1).text()

        # Open the modal for editing
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Item")
        dialog.setFixedSize(400, 250)
        dialog.setStyleSheet("background-color: #FFFFFF; color: #2F4156;")

        layout = QVBoxLayout(dialog)

        # Date Label and Input
        date_label = QLabel("DATE:")
        date_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(date_label)

        # Use QDateEdit for the Date input
        date_input = QDateEdit(self)
        date_input.setObjectName("date_input")
        date_input.setDisplayFormat("yyyy-MM-dd")
        date_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
        date_input.setDate(QDate.fromString(current_date, "yyyy-MM-dd"))  # Set current date
        layout.addWidget(date_input)

        # Vaccine Label and Input
        vaccine_label = QLabel("VACCINE:")
        vaccine_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(vaccine_label)

        vaccine_input = QLineEdit()
        vaccine_input.setObjectName("vaccine_input")
        vaccine_input.setText(current_vaccine)  # Set current vaccine name
        vaccine_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
        layout.addWidget(vaccine_input)

        # Save button
        save_button = QPushButton("Save Changes")
        save_button.setStyleSheet("""
                QPushButton {
                    background-color: #567C8D;
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #6B92A2;
                }
            """)
        
        # Validation and Save
        def validateAndSave():
            # Check if the inputs are valid
            is_valid = True

            if date_input.text().strip() == "":
                date_input.setStyleSheet("padding: 5px; border: 1px solid red; border-radius: 4px;")
                is_valid = False
            else:
                date_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")

            if vaccine_input.text().strip() == "":
                vaccine_input.setStyleSheet("padding: 5px; border: 1px solid red; border-radius: 4px;")
                is_valid = False
            else:
                vaccine_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")

            if is_valid:
                # Update table data
                self.table.setItem(row_position, 0, QTableWidgetItem(date_input.date().toString("yyyy-MM-dd")))
                self.table.setItem(row_position, 1, QTableWidgetItem(vaccine_input.text()))
                dialog.accept()  # Close the dialog

        save_button.clicked.connect(validateAndSave)
        layout.addWidget(save_button)

        # Open the modal
        dialog.exec_()


    def addNavigationBar(self):
        # Sidebar container
        self.sidebar = QWidget(self)
        self.sidebar.setStyleSheet("background-color: #567C8D")
        self.sidebar.setGeometry(35, 280, 165, 275)

        # Vaccination button
        self.vaccination_button = QPushButton("Vaccination", self.sidebar)
        self.vaccination_button.setGeometry(0, 100, 200, 50)
        self.vaccination_button.setStyleSheet("background-color: #567C8D; color: white; font-size: 16px;")
        self.vaccination_button.clicked.connect(lambda: self.onNavButtonClick("Vaccination"))

        # Vet Visits button
        self.vet_visits_button = QPushButton("Vet Visits", self.sidebar)
        self.vet_visits_button.setGeometry(0, 150, 200, 50)
        self.vet_visits_button.setStyleSheet("background-color: #567C8D; color: white; font-size: 16px;")
        self.vet_visits_button.clicked.connect(lambda: self.onNavButtonClick("Vet Visits"))

        # Medication button
        self.medication_button = QPushButton("Medication", self.sidebar)
        self.medication_button.setGeometry(0, 200, 180, 50)
        self.medication_button.setStyleSheet("background-color: #567C8D; color: white; font-size: 16px;")
        self.medication_button.clicked.connect(lambda: self.onNavButtonClick("Medication"))

    def onNavButtonClick(self, category):
        self.selected_category = category
        self.updateTableHeader(category)

    # For other components 
    def paintEvent(self, event):
        painter = QPainter(self)

        # PETCARE TEXT upper right
        PetCare = QFont()
        PetCare.setPointSize(13)
        painter.setFont(PetCare)
        painter.setPen(QColor("#ffffff"))
        painter.drawText(502, 67, 214, 36, Qt.AlignCenter, "PET CARE")

        # Outer box
        pen = QPen(QColor("#E5E4E2"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#E5E4E2"))
        painter.drawRoundedRect(20, 210, 760, 359, 10.0, 10.0)

        # Dog and cat images
        dog_image = QPixmap("Dog.png")
        painter.drawPixmap(73, 7, 149, 259, dog_image)
        cat_image = QPixmap("Cat.png")
        painter.drawPixmap(170, -10, 260, 230, cat_image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
