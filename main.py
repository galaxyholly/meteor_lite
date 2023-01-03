from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QWidget, QVBoxLayout, QPushButton


# needed for command line args
import sys
mondayTemps = "60deg"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.label = QLabel()
        self.label.setMargin(1)

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()

        widgets = [
            QLabel(f"Monday {mondayTemps}"),
            QLabel(f"Tuesday {mondayTemps}"),
            QLabel(f"Wednesday {mondayTemps}"),
            QLabel(f"Thursday {mondayTemps}"),
            QLabel(f"Friday {mondayTemps}"),
            QLabel(f"Saturday {mondayTemps}"),
            QLabel(f"Sunday {mondayTemps}"),
            QPushButton("Self")
        ]

        for wid in widgets:
            layout.addWidget(wid)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        
        

# Only need one per application
app = QApplication(sys.argv)

# Creating a new widget, which will be the window
w = MainWindow()
w.show() # Windows are hidden by default

# Starts the event loop
app.exec()






