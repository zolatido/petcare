import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QLabel, QPushButton
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
        try:
            self.setWindowIcon(QIcon('animals.ico'))
        except Exception as e:
            print(f"Error loading window icon: {e}")

        # Add navigation bar tabs
        self.addNavBarTabs()

        # Add header label
        self.addHeaderLabel()

        # Initialize default content
        self.updateHeaderText("                                     Date                   Vaccine                Action")

        self.show()

    # Add navigation bar tabs
    def addNavBarTabs(self):
        # Fonts for the navigation bar labels
        nav_font = QFont()
        nav_font.setPointSize(11)
        nav_font.setBold(True)

        # Tab 1 - Vaccinations
        vaccinations_tab = QPushButton("Vaccinations", self)
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

    # Add header label
    def addHeaderLabel(self):
        self.header_label = QLabel(self)
        self.header_label.setStyleSheet("color: #D9D9D9; font-size: 14px;")
        self.header_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    # Update header text
    def updateHeaderText(self, text):
        self.header_text = text
        self.update() 

    def getHeaderText(self):
        return self.header_text if hasattr(self, 'header_text') else "Default Header"

    # Tab click handler
    def onTabClicked(self, button, tab_name):
        # Reset the style of the previously active button
        if self.active_button:
            self.active_button.setStyleSheet("""
                color: #2F4156; 
                background: transparent; 
                border: none; 
                padding: 5px;
                text-align: center;
            """)

        # Set the new active button style
        button.setStyleSheet("""
            color: #FFFFFF; 
            background-color: #567C8D; 
            border: none; 
            padding: 5px;
            text-align: center;
        """)

        # Update header text based on tab clicked
        if tab_name == "Vaccinations":
            self.updateHeaderText("                                     Date                   Vaccine                Action")
        elif tab_name == "Vet Visits":
            self.updateHeaderText("                                     Date                  Remarks               Action")
        elif tab_name == "Medication":
            self.updateHeaderText("                                 Date          Medication        x/day        Action")

        # Set the clicked button as the active one
        self.active_button = button

    # centers window
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # style sheet for components
    def paintEvent(self, event):
        painter = QPainter(self)

        # Outer box
        pen = QPen(QColor("#E5E4E2"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#E5E4E2"))
        painter.drawRect(20, 210, 760, 359)

        # Dashboard with notebook lines
        pen = QPen(QColor("#FFFFFF"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawRoundedRect(66, 276, 681, 275, 15.0, 15.0)

        # Draw notebook lines inside the dashboard
        pen.setColor(QColor("#D9D9D9"))  # Set the line color to a light gray
        painter.setPen(pen)

        # Calculate the spacing between the lines (you can adjust this for more/less lines)
        line_spacing = 20  # Space between each line
        for y in range(286, 550, line_spacing):  # Start drawing lines from y=286 to y=550 (inside the dashboard area)
            painter.drawLine(66, y, 747, y)  # Draw a line from x=66 to x=747 (covering the full width of the dashboard)

        # Nav bar
        pen = QPen(QColor("#D9D9D9"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#D9D9D9"))
        painter.drawRoundedRect(66, 276, 165, 276.88, 15.0, 15.0)

        # Header
        pen = QPen(QColor("#567C8D"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#567C8D"))
        painter.drawRoundedRect(66, 276, 681, 38.88, 0.0, 15.0)

        # Draw header text
        font_header = QFont()
        font_header.setPointSize(12)
        font_header.setBold(True)
        painter.setFont(font_header)
        painter.setPen(QColor("#FFFFFF"))
        painter.drawText(76, 278, 661, 34, Qt.AlignLeft | Qt.AlignVCenter, self.getHeaderText())

        # Dog and cat images
        dog_image = QPixmap("Dog.png")
        painter.drawPixmap(73, 7, 149, 259, dog_image)
        cat_image = QPixmap("Cat.png")
        painter.drawPixmap(170, -10, 260, 230, cat_image)

        # Pet Care
        font_title2 = QFont()
        font_title2.setPointSize(13)
        painter.setFont(font_title2)
        painter.setPen(QColor("#ffffff"))
        painter.drawText(502, 67, 214, 36, Qt.AlignCenter, "PET CARE")

        # 'Wall' - Background for dog and cat
        pen = QPen(QColor("#e8e7e7"), 0)
        painter.setPen(pen)
        painter.setBrush(QColor("#e8e7e7"))
        painter.setOpacity(0.3)
        painter.drawRect(0, 170, self.width(), self.height())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = App()
    sys.exit(app.exec_())
