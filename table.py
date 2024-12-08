import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDesktopWidget, QLabel, QPushButton, QDialog, QVBoxLayout,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit, QWidget, QHBoxLayout,
    QAbstractItemView, QStackedWidget
)
from PyQt5.QtGui import QIcon, QPixmap, QColor, QFont, QPainter, QPen
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

        # Set window size and center it
        self.setFixedSize(1000, 600)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Set window icon
        self.setWindowIcon(QIcon('animals.ico'))

        # Add the left navigation bar
        self.addNavigationBar()

        # Create stacked widget for content switching
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setGeometry(200, 0, 800, 600)

        # Create pages for each section
        self.vaccination_page = QWidget(self)
        self.vet_visits_page = QWidget(self)
        self.medication_page = QWidget(self)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.vaccination_page)
        self.stacked_widget.addWidget(self.vet_visits_page)
        self.stacked_widget.addWidget(self.medication_page)

        # Create table for Vaccination page (for now, you can reuse this table or create different ones)
        self.createTable(self.vaccination_page)

    def addNavigationBar(self):
        # Sidebar container
        self.sidebar = QWidget(self)
        self.sidebar.setStyleSheet("background-color: #567C8D")
        self.sidebar.setGeometry(0, 0, 200, self.height())

        # Vaccination button
        self.vaccination_button = QPushButton("Vaccination", self.sidebar)
        self.vaccination_button.setGeometry(0, 100, 200, 50)
        self.vaccination_button.setStyleSheet("background-color: #567C8D; color: white; font-size: 16px;")
        self.vaccination_button.clicked.connect(self.showVaccinationPage)

        # Vet Visits button
        self.vet_visits_button = QPushButton("Vet Visits", self.sidebar)
        self.vet_visits_button.setGeometry(0, 150, 200, 50)
        self.vet_visits_button.setStyleSheet("background-color: #567C8D; color: white; font-size: 16px;")
        self.vet_visits_button.clicked.connect(self.showVetVisitsPage)

        # Medication button
        self.medication_button = QPushButton("Medication", self.sidebar)
        self.medication_button.setGeometry(0, 200, 200, 50)
        self.medication_button.setStyleSheet("background-color: #567C8D; color: white; font-size: 16px;")
        self.medication_button.clicked.connect(self.showMedicationPage)

    def showVaccinationPage(self):
        self.stacked_widget.setCurrentWidget(self.vaccination_page)

    def showVetVisitsPage(self):
        self.stacked_widget.setCurrentWidget(self.vet_visits_page)

    def showMedicationPage(self):
        self.stacked_widget.setCurrentWidget(self.medication_page)

    def createTable(self, page):
        # Create table for displaying added items (Vaccination as example)
        table = QTableWidget(page)
        table.setRowCount(0)  # Start with no rows
        table.setColumnCount(3)  # 3 columns: Date, Vaccine, and Action
        table.setHorizontalHeaderLabels(["Date", "Vaccine", "Action"])
        table.setStyleSheet("background-color: #FFFFFF; border: 1px solid #D9D9D9;")

        # Column widths
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Size of the table
        table.setFixedSize(565, 310)

        # Position of the table
        table.move(20, 100)

        # Hide row numbers
        table.verticalHeader().setVisible(False)

        # No highlight
        table.setSelectionMode(QAbstractItemView.NoSelection)

        # Add the table to the page
        page.layout = QVBoxLayout(page)
        page.layout.addWidget(table)

    def paintEvent(self, event):
        painter = QPainter(self)

        # PETCARE TEXT upper right
        petCareFont = QFont()
        petCareFont.setPointSize(13)
        painter.setFont(petCareFont)
        painter.setPen(QColor("#ffffff"))
        painter.drawText(502, 67, 214, 36, Qt.AlignCenter, "PET CARE")

        # Outer box
        pen = QPen(QColor("#E5E4E2"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#E5E4E2"))
        painter.drawRoundedRect(20, 210, 760, 359, 10.0, 10.0)

        # Dog and cat images (for decoration, you can replace them with actual image files)
        dog_image = QPixmap("Dog.png")
        painter.drawPixmap(73, 7, 149, 259, dog_image)
        cat_image = QPixmap("Cat.png")
        painter.drawPixmap(170, -10, 260, 230, cat_image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
