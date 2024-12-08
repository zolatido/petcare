import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDesktopWidget, QLabel, QPushButton, QDialog, QVBoxLayout,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QIcon, QPainter, QPen, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Pet Care"
        self.setStyleSheet("background-color: #2F4156")
        self.header_label = None  # Placeholder for header label
        self.active_button = None  # To track the last clicked button
        self.current_tab = "Vaccinations"  # Default tab
        self.table_widget = None  # Table to display added data
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setFixedSize(800, 600)
        self.center()
        self.setWindowIcon(QIcon('animals.ico'))

        # Add navigation bar tabs
        self.addNavBarTabs()

        # Add header label
        self.addHeaderLabel()

        # Add the table widget first
        self.addTable()

        # Add the create button after the table
        self.addCircleButton()

        # Set default to Vaccinations
        self.onTabClicked(self.findChild(QPushButton, "vaccinations_tab"), "Vaccinations")

        self.show()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def addNavBarTabs(self):
        # Fonts for the navigation bar labels
        nav_font = QFont()
        nav_font.setPointSize(11)
        nav_font.setBold(True)

        # Tab 1 - Vaccinations
        vaccinations_tab = QPushButton("Vaccinations", self)
        vaccinations_tab.setObjectName("vaccinations_tab")
        vaccinations_tab.setGeometry(80, 358, 150, 30)
        vaccinations_tab.setFont(nav_font)
        vaccinations_tab.setStyleSheet("""
            color: #2F4156; 
            background: transparent; 
            border: none; 
            padding: 5px;
            text-align: center;
        """)
        vaccinations_tab.clicked.connect(lambda: self.onTabClicked(vaccinations_tab, "Vaccinations"))

        # Tab 2 - Vet Visits
        vet_visits_tab = QPushButton("Vet Visits", self)
        vet_visits_tab.setGeometry(80, 408, 150, 30)
        vet_visits_tab.setFont(nav_font)
        vet_visits_tab.setStyleSheet("""
            color: #2F4156; 
            background: transparent; 
            border: none; 
            padding: 5px;
            text-align: center;
        """)
        vet_visits_tab.clicked.connect(lambda: self.onTabClicked(vet_visits_tab, "Vet Visits"))

        # Tab 3 - Medication
        medication_tab = QPushButton("Medication", self)
        medication_tab.setGeometry(80, 457, 150, 30)
        medication_tab.setFont(nav_font)
        medication_tab.setStyleSheet("""
            color: #2F4156; 
            background: transparent; 
            border: none; 
            padding: 5px;
            text-align: center;
        """)
        medication_tab.clicked.connect(lambda: self.onTabClicked(medication_tab, "Medication"))

    def addHeaderLabel(self):
        self.header_label = QLabel(self)
        self.header_label.setStyleSheet("color: #D9D9D9; font-size: 14px;")
        self.header_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def addCircleButton(self):
        self.circle_button = QPushButton(self)
        self.circle_button.setFixedSize(60, 60)
        self.circle_button.setStyleSheet("""
            QPushButton {
                background-color: #567C8D;
                border-radius: 30px;
                border: 2px solid #D9D9D9;
            }
            QPushButton:hover {
                background-color: #6B92A2;
            }
        """)
        self.circle_button.setIcon(QIcon('create.png'))
        self.circle_button.setIconSize(self.circle_button.size())
        self.repositionCircleButton()
        self.circle_button.clicked.connect(self.showAddItemModal)

    def addTable(self):
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(232, 315, 516, 239)
        self.table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF; 
                color: #2F4156; 
                border: none;
                gridline-color: #D9D9D9;  /* Make grid lines visible */
            }
            QTableWidget::item {
                border-right: 1px solid #D9D9D9;  /* Add a vertical border between columns */
                border-bottom: 1px solid #D9D9D9; /* Add horizontal row borders */
            }
            QTableWidget::item:selected {
                background-color: #B4C7E7;  /* Highlight selected row */
            }
            QHeaderView::section {
                background-color: #F5F5F5; 
                color: #2F4156; 
                border: none;  /* Remove header borders */
            }
        """)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setAlternatingRowColors(True)  # Alternating row colors

    def addItem(self, date, extra, dialog):
        # Validate common input fields
        if not date.strip():
            self.setFieldError(dialog.findChild(QLineEdit, "date_input"), True)
            return
        self.setFieldError(dialog.findChild(QLineEdit, "date_input"), False)

        # Prepare data for each tab
        row_data = []
        if self.current_tab == "Vaccinations":
            vaccine_input = dialog.findChild(QLineEdit, "vaccine_input")
            if not vaccine_input.text().strip():
                self.setFieldError(vaccine_input, True)
                return
            self.setFieldError(vaccine_input, False)
            row_data = [date, vaccine_input.text(), ""]

        elif self.current_tab == "Vet Visits":
            remarks_input = dialog.findChild(QLineEdit, "remarks_input")
            if not remarks_input.text().strip():
                self.setFieldError(remarks_input, True)
                return
            self.setFieldError(remarks_input, False)
            row_data = [date, remarks_input.text(), ""]

        elif self.current_tab == "Medication":
            medication_input = dialog.findChild(QLineEdit, "medication_input")
            dosage_input = dialog.findChild(QLineEdit, "dosage_input")
            if not medication_input.text().strip() or not dosage_input.text().strip():
                self.setFieldError(medication_input, not medication_input.text().strip())
                self.setFieldError(dosage_input, not dosage_input.text().strip())
                return
            self.setFieldError(medication_input, False)
            self.setFieldError(dosage_input, False)
            row_data = [date, medication_input.text(), dosage_input.text(), ""]

        # Add row data to the table
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)  # Insert a new row

        # Add each piece of data to the corresponding column and set text color to black
        for col_index, data in enumerate(row_data):
            item = QTableWidgetItem(data)
            item.setForeground(QColor(0, 0, 0))  # Set text color to black

            self.table_widget.setItem(row_position, col_index, item)

        print(f"Added to {self.current_tab} table: {row_data}")
        dialog.accept()

    def setFieldError(self, field, is_error):
        field.setStyleSheet(
            "padding: 5px; border: 1px solid red; border-radius: 4px;" if is_error else
            "padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;"
        )


    def onTabClicked(self, button, tab_name):
        self.current_tab = tab_name  # Update the current active tab
        if self.active_button:
            self.active_button.setStyleSheet("""
                color: #2F4156; 
                background: transparent; 
                border: none; 
                padding: 5px;
                text-align: center;
            """)
        button.setStyleSheet("""
            color: #FFFFFF; 
            background-color: #567C8D; 
            border: none; 
            padding: 5px;
            text-align: center;
        """)
        if tab_name == "Vaccinations":
            self.updateHeaderText("                                     Date                   Vaccine                Action")
        elif tab_name == "Vet Visits":
            self.updateHeaderText("                                     Date                  Remarks               Action")
        elif tab_name == "Medication":
            self.updateHeaderText("                                 Date          Medication        x/day        Action")
        self.active_button = button

    def updateHeaderText(self, text):
        self.header_text = text
        self.update()

    def getHeaderText(self):
        return self.header_text if hasattr(self, 'header_text') else "Default Header"

    def repositionCircleButton(self):
        # Get the dimensions of the window
        window_width = self.width()
        window_height = self.height()

        # Calculate the position for the button in the bottom-right corner
        button_x = window_width - self.circle_button.width() - 70  # 20px margin from the right edge
        button_y = window_height - self.circle_button.height() - 60  # 20px margin from the bottom edge

        self.circle_button.move(button_x, button_y)


    def showAddItemModal(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Item")
        dialog.setFixedSize(400, 250)
        dialog.setStyleSheet("background-color: #FFFFFF; color: #2F4156;")

        layout = QVBoxLayout(dialog)

        # Common Date Label and Input
        date_label = QLabel("DATE:")
        date_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(date_label)

        date_input = QLineEdit()
        date_input.setObjectName("date_input")
        date_input.setPlaceholderText("Enter date (e.g., YYYY-MM-DD)...")
        date_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
        layout.addWidget(date_input)

        # Tab-specific fields
        if self.current_tab == "Vaccinations":
            # Vaccination-specific fields
            vaccine_label = QLabel("VACCINE:")
            vaccine_label.setStyleSheet("font-size: 14px; font-weight: bold;")
            layout.addWidget(vaccine_label)

            vaccine_input = QLineEdit()
            vaccine_input.setObjectName("vaccine_input")
            vaccine_input.setPlaceholderText("Enter vaccine name...")
            vaccine_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
            layout.addWidget(vaccine_input)

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
            add_button.clicked.connect(lambda: self.addItem(date_input.text(), vaccine_input.text(), dialog))
            layout.addWidget(add_button)

        elif self.current_tab == "Vet Visits":
            # Vet Visits-specific fields
            remarks_label = QLabel("REMARKS:")
            remarks_label.setStyleSheet("font-size: 14px; font-weight: bold;")
            layout.addWidget(remarks_label)

            remarks_input = QLineEdit()
            remarks_input.setObjectName("remarks_input")
            remarks_input.setPlaceholderText("Enter remarks...")
            remarks_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
            layout.addWidget(remarks_input)

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
            add_button.clicked.connect(lambda: self.addItem(date_input.text(), medication_input.text(), dialog))
            layout.addWidget(add_button)

        elif self.current_tab == "Medication":
            # Medication-specific fields
            medication_label = QLabel("MEDICATION:")
            medication_label.setStyleSheet("font-size: 14px; font-weight: bold;")
            layout.addWidget(medication_label)

            medication_input = QLineEdit()
            medication_input.setObjectName("medication_input")
            medication_input.setPlaceholderText("Enter medication name...")
            medication_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
            layout.addWidget(medication_input)

            dosage_label = QLabel("DOSAGE:")
            dosage_label.setStyleSheet("font-size: 14px; font-weight: bold;")
            layout.addWidget(dosage_label)

            dosage_input = QLineEdit()
            dosage_input.setObjectName("dosage_input")
            dosage_input.setPlaceholderText("Enter dosage...")
            dosage_input.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
            layout.addWidget(dosage_input)

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
            add_button.clicked.connect(lambda: self.addItem(date_input.text(), medication_input.text() + ' ' + dosage_input.text(), dialog))
            layout.addWidget(add_button)

        dialog.exec_()


    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor("#E5E4E2"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#E5E4E2"))
        painter.drawRect(20, 210, 760, 359)

        pen = QPen(QColor("#FFFFFF"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawRoundedRect(66, 276, 681, 275, 15.0, 15.0)

        pen.setColor(QColor("#D9D9D9"))
        painter.setPen(pen)
        line_spacing = 20
        for y in range(286, 550, line_spacing):
            painter.drawLine(66, y, 747, y)

        pen = QPen(QColor("#D9D9D9"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#D9D9D9"))
        painter.drawRoundedRect(66, 276, 165, 276, 15.0, 15.0)

        pen = QPen(QColor("#567C8D"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#567C8D"))
        painter.drawRoundedRect(66, 276, 681, 38, 0.0, 15.0)

        font_header = QFont()
        font_header.setPointSize(12)
        font_header.setBold(True)
        painter.setFont(font_header)
        painter.setPen(QColor("#FFFFFF"))
        painter.drawText(76, 278, 661, 34, Qt.AlignLeft | Qt.AlignVCenter, self.getHeaderText())

        dog_image = QPixmap("Dog.png")
        painter.drawPixmap(73, 7, 149, 259, dog_image)
        cat_image = QPixmap("Cat.png")
        painter.drawPixmap(170, -10, 260, 230, cat_image)

        font_title2 = QFont()
        font_title2.setPointSize(13)
        painter.setFont(font_title2)
        painter.setPen(QColor("#ffffff"))
        painter.drawText(502, 67, 214, 36, Qt.AlignCenter, "PET CARE")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.repositionCircleButton()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())