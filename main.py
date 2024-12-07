import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDesktopWidget, QLabel, QPushButton, QDialog, QVBoxLayout, QLineEdit
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

        # Add the create button
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
        vaccinations_tab.setObjectName("vaccinations_tab")  # Assign an object name for identification
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

    def updateHeaderText(self, text):
        self.header_text = text
        self.update()

    def getHeaderText(self):
        return self.header_text if hasattr(self, 'header_text') else "Default Header"

    def onTabClicked(self, button, tab_name):
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

    def repositionCircleButton(self):
        dashboard_bottom_right_x = 747
        dashboard_bottom_right_y = 550
        button_x = dashboard_bottom_right_x - 70
        button_y = dashboard_bottom_right_y - 70
        self.circle_button.move(button_x, button_y)

    def showAddItemModal(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Item")
        dialog.setFixedSize(400, 200)
        dialog.setStyleSheet("background-color: #FFFFFF; color: #2F4156;")

        layout = QVBoxLayout(dialog)

        label = QLabel("DATE")
        label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(label)

        input_field = QLineEdit()
        input_field.setPlaceholderText("Item details...")
        input_field.setStyleSheet("padding: 5px; border: 1px solid #D9D9D9; border-radius: 4px;")
        layout.addWidget(input_field)

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

        add_button.clicked.connect(lambda: self.addItem(input_field.text(), dialog))
        layout.addWidget(add_button)

        dialog.exec_()

    def addItem(self, item_details, dialog):
        if item_details.strip():
            print(f"Item added: {item_details}")
            dialog.accept()
        else:
            print("No details entered!")

    

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
