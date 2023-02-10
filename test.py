from PySide6 import QtCore
from PySide6.QtCore import *
from PySide6.QtWidgets import * # QApplication, QMainWindow, QLabel, QWidget, QPushButton, QGridLayout
from PySide6.QtGui import *
import sys
                                                                                                                                                                                                                                                                                             

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.buttonWindow = QWidget()
        layout = QHBoxLayout(self.buttonWindow)
        self.button = QPushButton("settingsButton")
        self.label = QLabel("settingsLabel")
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.button.clicked.connect(self.changeMainWindow)
    
    def changeMainWindow(self):
        pass

class ExtraWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.buttonWindow = QWidget()
        self.setWindowTitle("Extra")
        layout = QHBoxLayout(self.buttonWindow)
        self.button = QPushButton("extraButton")
        self.label = QLabel("extraLabel")
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.button.clicked.connect(self.changeMainWindow)
        self.checkBox = QCheckBox("temps")
        layout.addWidget(self.checkBox)
        self.label.enterEvent.connect(self.hoverEventTest)

    def changeMainWindow(self):
        self.setWindowTitle("Stinky")

    def hoverEventTest(self):
        print("success")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = QWidget()
        layout = QHBoxLayout(self.widget)
        self.setCentralWidget(self.widget)

        self.button = QPushButton("Press for Settings")
        self.button.clicked.connect(self.addSettingsWindow)
        
        self.button2 = QPushButton("Press for Extra")
        self.button2.clicked.connect(self.addExtraWindow)

        self.label = QLabel("MainLabel")

        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        layout.addWidget(self.label)

    def addSettingsWindow(self):
        self.settingsWindow = SettingsWindow()
        self.settingsWindow.show()
        self.settingsWindow.button.clicked.connect(self.settingsChanged)


    def addExtraWindow(self):
        self.extraWindow = ExtraWindow()
        self.extraWindow.show()
        self.extraWindow.checkBox.stateChanged.connect(self.checkBoxChanged)


    def checkBoxChanged(self):
        if self.extraWindow.checkBox.isChecked() == True:
            print("WOWOWOWOW")
            self.testLabel = QLabel("WOWOWOWO")



    def settingsChanged(self):
        self.label.setText("Damgus")
        self.testLabel = QLabel("WOWOWOWO")
        self.setWindowTitle("Changed")


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()