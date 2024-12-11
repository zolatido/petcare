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
        self.data_store = {
            "Vaccination": [],
            "Vet Visits": [],
            "Medication": []
        }

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

        #add the left navigation bar
        self.addNavigationBar()

        #set the default header to "Vaccination"
        self.onNavButtonClick("Vaccination")

    #table for displaying added item / displays user input
    def createTable(self):
        self.table = QTableWidget(self)
        self.table.setRowCount(0)  
        self.table.setColumnCount(3)  
        self.table.setStyleSheet("background-color: #FFFFFF; border: 1px solid #D9D9D9;")
        
        #column widths 
        self.table.setColumnWidth(0, 150)  #Date
        self.table.setColumnWidth(1, 200)  #Vaccine / Remarks / Medicine
        self.table.setColumnWidth(2, 100)  #Action (for buttons)

        #clumn matic resize
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # dashboard table size
        self.table.setFixedSize(565, 277)  
        
        #position of the dashboard table
        self.table.move(200, 279)

        # hide row numbers
        self.table.verticalHeader().setVisible(False)

        # remove highlifhgt
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
    
        self.create_button.move(690, 215)

    #update table headers based on navbar
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
        dialog.setWindowTitle(f"Add {self.selected_category} Item")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet("background-color: #FFFFFF; color: #2F4156;")
        layout = QVBoxLayout(dialog)

        #common Date Input
        date_label = QLabel("DATE:")
        date_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(date_label)

        date_input = QDateEdit(self)
        date_input.setObjectName("date_input")
        date_input.setDisplayFormat("yyyy-MM-dd")
        date_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
        date_input.setDate(QDate.currentDate())
        layout.addWidget(date_input)

        # modal input per nav bar tab
        if self.selected_category == "Vaccination":
            label = QLabel("VACCINE:")
            input_field = QLineEdit()
            input_field.setPlaceholderText("Enter vaccine name...")

            layout.addWidget(label)
            layout.addWidget(input_field)

        elif self.selected_category == "Vet Visits":
            label = QLabel("REMARKS:")
            input_field = QLineEdit()
            input_field.setPlaceholderText("Enter visit remarks...")

            layout.addWidget(label)
            layout.addWidget(input_field)

        elif self.selected_category == "Medication":
            label = QLabel("MEDICINE: ")
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
            input_field = QLineEdit()
            input_field.setPlaceholderText("Enter medicine name...")

            layout.addWidget(label)
            layout.addWidget(input_field)

            dosage_label = QLabel("DOSAGE (x/day): ")
            dosage_label.setStyleSheet("font-size: 14px; font-weight: bold;")
            dosage_input = QLineEdit()
            dosage_input.setPlaceholderText("Enter dosage frequency...")
            dosage_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")

            layout.addWidget(dosage_label)
            layout.addWidget(dosage_input)

        label.setStyleSheet("font-size: 14px; font-weight: bold;")
        input_field.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")

        # Add Button
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
            is_valid = True

            # Validate Date
            if date_input.text().strip() == "":
                date_input.setStyleSheet("padding: 5px; border: 1px solid red; border-radius: 4px;")
                is_valid = False
            else:
                date_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")

            # Validate Main Input
            if input_field.text().strip() == "":
                input_field.setStyleSheet("padding: 5px; border: 1px solid red; border-radius: 4px;")
                is_valid = False
            else:
                input_field.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")

            # Validate Dosage
            if self.selected_category == "Medication" and dosage_input.text().strip() == "":
                dosage_input.setStyleSheet("padding: 5px; border: 1px solid red; border-radius: 4px;")
                is_valid = False
            elif self.selected_category == "Medication":
                dosage_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")

            if is_valid:
                if self.selected_category == "Medication":
                    self.addItem(
                        date_input.date().toString("yyyy-MM-dd"),
                        input_field.text(),
                        dosage_input.text()
                    )
                else:
                    self.addItem(
                        date_input.date().toString("yyyy-MM-dd"),
                        input_field.text()
                    )
                dialog.accept()

        add_button.clicked.connect(validateAndAddItem)
        layout.addWidget(add_button)

        dialog.exec_()

    def addItem(self, date, main_input, dosage=None):

        # Save data to the category
        if self.selected_category == "Medication":
            self.data_store[self.selected_category].append({
                "date": date,
                "medicine": main_input,
                "dosage": dosage
            })
        else:
            self.data_store[self.selected_category].append({
                "date": date,
                "details": main_input
            })

        # Add the data to the table
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(date))         #date
        self.table.setItem(row_position, 1, QTableWidgetItem(main_input))   #2nd col - vacc|remarks|med

        #for action buttons (edit and delete)
        if dosage: 
            self.table.setItem(row_position, 2, QTableWidgetItem(dosage))   #med tab - 3rd col | dosage
            self.table.setCellWidget(row_position, 3, self.createActionButtons(row_position))
        else:  
            self.table.setCellWidget(row_position, 2, self.createActionButtons(row_position))

    def createActionButtons(self, row_position):
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
        self.table.removeRow(row_position)

    def editRow(self, row_position):
        #Get current data from the row
        current_date = self.table.item(row_position, 0).text()
        current_main_input = self.table.item(row_position, 1).text()

        if self.selected_category == "Medication":
            current_dosage = self.table.item(row_position, 2).text()

        #open the modal for editing
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Edit {self.selected_category} Item")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet("background-color: #FFFFFF; color: #2F4156;")

        layout = QVBoxLayout(dialog)

        #Date Label and Input
        date_label = QLabel("DATE:")
        date_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(date_label)

        date_input = QDateEdit(self)
        date_input.setObjectName("date_input")
        date_input.setDisplayFormat("yyyy-MM-dd")
        date_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
        date_input.setDate(QDate.fromString(current_date, "yyyy-MM-dd"))
        layout.addWidget(date_input)

        #ctegory navbar tabs
        if self.selected_category == "Vaccination":
            label = QLabel("VACCINE:")
            input_field = QLineEdit(self)
            input_field.setText(current_main_input)
            input_field.setPlaceholderText("Enter vaccine name...")
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
            layout.addWidget(label)
            input_field.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
            layout.addWidget(input_field)

        elif self.selected_category == "Vet Visits":
            label = QLabel("REMARKS:")
            input_field = QLineEdit(self)
            input_field.setText(current_main_input)
            input_field.setPlaceholderText("Enter visit remarks...")
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
            layout.addWidget(label)
            input_field.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
            layout.addWidget(input_field)

        elif self.selected_category == "Medication":
            #medicine Name
            med_label = QLabel("MEDICINE:")
            med_input = QLineEdit(self)
            med_input.setText(current_main_input)
            med_input.setPlaceholderText("Enter medicine name...")

            med_label.setStyleSheet("font-size: 14px; font-weight: bold;")
            layout.addWidget(med_label)
            med_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
            layout.addWidget(med_input)

            #dosage
            dosage_label = QLabel("DOSAGE:")
            dosage_input = QLineEdit(self)
            dosage_input.setText(current_dosage)
            dosage_input.setPlaceholderText("Enter dosage...")

            dosage_label.setStyleSheet("font-size: 14px; font-weight: bold;")
            layout.addWidget(dosage_label)
            dosage_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
            layout.addWidget(dosage_input)

        #save Button
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

        #Validation and Save
        def validateAndSave():
            is_valid = True

            if date_input.text().strip() == "":
                date_input.setStyleSheet("padding: 5px; border: 1px solid red; border-radius: 4px;")
                is_valid = False
            else:
                date_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")

            if self.selected_category != "Medication" and input_field.text().strip() == "":
                input_field.setStyleSheet("padding: 5px; border: 1px solid red; border-radius: 4px;")
                is_valid = False
            elif self.selected_category == "Medication":
                if med_input.text().strip() == "" or dosage_input.text().strip() == "":
                    med_input.setStyleSheet("padding: 5px; border: 1px solid red; border-radius: 4px;")
                    dosage_input.setStyleSheet("padding: 5px; border: 1px solid red; border-radius: 4px;")
                    is_valid = False
                else:
                    med_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
                    dosage_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")

            if is_valid:
                #Update table
                self.table.setItem(row_position, 0, QTableWidgetItem(date_input.date().toString("yyyy-MM-dd")))
                if self.selected_category == "Medication":
                    self.table.setItem(row_position, 1, QTableWidgetItem(med_input.text()))
                    self.table.setItem(row_position, 2, QTableWidgetItem(dosage_input.text()))
                else:
                    self.table.setItem(row_position, 1, QTableWidgetItem(input_field.text()))
                dialog.accept()

        save_button.clicked.connect(validateAndSave)
        layout.addWidget(save_button)

        #Open the modal
        dialog.exec_()


    def addNavigationBar(self):
        #sidebar container
        self.sidebar = QWidget(self)
        self.sidebar.setStyleSheet("background-color: #567C8D")
        self.sidebar.setGeometry(35, 280, 165, 275)

        # My Pet's Info
        pet_name_label = QLabel("My Pet's Info", self.sidebar)
        pet_name_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        pet_name_label.move(35, 40)
        
        #vaccination tan
        self.vaccination_button = QPushButton("Vaccination", self.sidebar)
        self.vaccination_button.setGeometry(0, 90, 180, 50)
        self.vaccination_button.setStyleSheet("background-color: #567C8D; color: white; font-size: 16px;")
        self.vaccination_button.clicked.connect(lambda: self.onNavButtonClick("Vaccination"))

        #vet Visits tab
        self.vet_visits_button = QPushButton("Vet Visits", self.sidebar)
        self.vet_visits_button.setGeometry(0, 140, 180, 50)
        self.vet_visits_button.setStyleSheet("background-color: #567C8D; color: white; font-size: 16px;")
        self.vet_visits_button.clicked.connect(lambda: self.onNavButtonClick("Vet Visits"))

        #medication tab
        self.medication_button = QPushButton("Medication", self.sidebar)
        self.medication_button.setGeometry(0, 190, 180, 50)
        self.medication_button.setStyleSheet("background-color: #567C8D; color: white; font-size: 16px;")
        self.medication_button.clicked.connect(lambda: self.onNavButtonClick("Medication"))

    def onNavButtonClick(self, category):
        #update the selected category
        self.selected_category = category

        #Highlight the active button
        buttons = [self.vaccination_button, self.vet_visits_button, self.medication_button]
        for button in buttons:
            button.setStyleSheet("background-color: #567C8D; color: white; font-size: 16px;")

        if category == "Vaccination":
            self.vaccination_button.setStyleSheet("background-color: #6B92A2; color: white; font-size: 16px;")
        elif category == "Vet Visits":
            self.vet_visits_button.setStyleSheet("background-color: #6B92A2; color: white; font-size: 16px;")
        elif category == "Medication":
            self.medication_button.setStyleSheet("background-color: #6B92A2; color: white; font-size: 16px;")

        #update the table headers and content
        self.updateTableHeader(category)

        #clear the table
        self.table.setRowCount(0)

        #put data the selected category
        for item in self.data_store[category]:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(item["date"]))

            if category == "Medication":
                self.table.setItem(row_position, 1, QTableWidgetItem(item["medicine"]))
                self.table.setItem(row_position, 2, QTableWidgetItem(item["dosage"]))
                self.table.setCellWidget(row_position, 3, self.createActionButtons(row_position))
            else:  # Vaccination or Vet Visits
                self.table.setItem(row_position, 1, QTableWidgetItem(item["details"]))
                self.table.setCellWidget(row_position, 2, self.createActionButtons(row_position))

    def refreshTableData(self):
        """Refresh the table with data"""
        #vlear the current table
        self.table.setRowCount(0)

        #get data 
        data = self.data_store.get(self.selected_category, [])

        #put data in the table
        for item in data:
            if self.selected_category == "Medication":
                self.addItem(item["date"], item["medicine"], item["dosage"])
            else:
                self.addItem(item["date"], item["details"])

    #for other components 
    def paintEvent(self, event):
        painter = QPainter(self)

        #PETCARE TEXT upper right
        PetCare = QFont()
        PetCare.setPointSize(13)
        painter.setFont(PetCare)
        painter.setPen(QColor("#ffffff"))
        painter.drawText(502, 67, 214, 36, Qt.AlignCenter, "PET CARE")

        #Outer box
        pen = QPen(QColor("#E5E4E2"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#E5E4E2"))
        painter.drawRoundedRect(20, 210, 760, 359, 10.0, 10.0)

        #Dog and cat images
        dog_image = QPixmap("Dog.png")
        painter.drawPixmap(73, 7, 149, 259, dog_image)
        cat_image = QPixmap("Cat.png")
        painter.drawPixmap(170, -10, 260, 230, cat_image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
