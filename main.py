from PySide6 import QtCore
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import * # QApplication, QMainWindow, QLabel, QWidget, QPushButton, QGridLayout
from PySide6.QtGui import *
from weatherGetter import *

# needed for command line args
import sys
startup()

week_list = sort_week_from_today()
print(str(week_list) + "WEEKLIST")
max_T = display_week(data_types[2], "C")
min_T = display_week(data_types[3], "C")
print(min_T)
print(max_T)

mon_high = max_T[week_list.index('Monday')][0][3].split(".")[0]
mon_low = min_T[week_list.index('Monday')][0][3].split(".")[0]
tues_high = max_T[week_list.index('Tuesday')][0][3].split(".")[0]
tues_low = min_T[week_list.index('Tuesday')][0][3].split(".")[0]
wed_high = max_T[week_list.index('Wednesday')][0][3].split(".")[0]
wed_low = min_T[week_list.index('Wednesday')][0][3].split(".")[0]
thurs_high = max_T[week_list.index('Thursday')][0][3].split(".")[0]
thurs_low = min_T[week_list.index('Thursday')][0][3].split(".")[0]
fri_high = max_T[week_list.index('Friday')][0][3].split(".")[0]
fri_low = min_T[week_list.index('Friday')][0][3].split(".")[0]
sat_high = max_T[week_list.index('Saturday')][0][3].split(".")[0]
sat_low = min_T[week_list.index('Saturday')][0][3].split(".")[0]
sun_high = max_T[week_list.index('Sunday')][0][3].split(".")[0]
sun_low = min_T[week_list.index('Sunday')][0][3].split(".")[0]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("MeteorLite")
        self.setStyleSheet("border-radius: 5px;")
            
        tempsLabelLayout = QGridLayout()

        self.setGeometry(1920, 0, 400, 30)
            
        self.MondayLabel = QLabel("M")
        self.TuesdayLabel = QLabel("T")
        self.WednesdayLabel = QLabel("W")
        self.ThursdayLabel = QLabel("TH")
        self.FridayLabel = QLabel("F")
        self.SaturdayLabel = QLabel("S")
        self.SundayLabel = QLabel("SN")  

        tempLabels = {
            "Monday":self.MondayLabel, 
            "Tuesday":self.TuesdayLabel, 
            "Wednesday":self.WednesdayLabel, 
            "Thursday":self.ThursdayLabel, 
            "Friday":self.FridayLabel, 
            "Saturday":self.SaturdayLabel, 
            "Sunday":self.SundayLabel
        }

        tempLabelsOrdered = [tempLabels[week_list[i]] for i in range(7)]
        tempsAlign = [label.setAlignment(QtCore.Qt.AlignCenter) for label in tempLabelsOrdered]
        tempsAlign

        for item in tempLabelsOrdered:
            item.setFont(QFont('Arial',8))

        tempsLabelLayout.addWidget(tempLabelsOrdered[0],0,0)
        tempsLabelLayout.addWidget(tempLabelsOrdered[1],0,1)
        tempsLabelLayout.addWidget(tempLabelsOrdered[2],0,2)
        tempsLabelLayout.addWidget(tempLabelsOrdered[3],0,3)
        tempsLabelLayout.addWidget(tempLabelsOrdered[4],0,4)
        tempsLabelLayout.addWidget(tempLabelsOrdered[5],0,5)
        tempsLabelLayout.addWidget(tempLabelsOrdered[6],0,6)

        self.TMLabel = QLabel(f"{mon_high}/{mon_low}")
        self.TTLabel = QLabel(f"{tues_high}/{tues_low}")
        self.TWLabel = QLabel(f"{wed_high}/{wed_low}")
        self.TTHLabel = QLabel(f"{thurs_high}/{thurs_low}")
        self.TFLabel = QLabel(f"{fri_high}/{fri_low}")
        self.TSLabel = QLabel(f"{sat_high}/{sat_low}")
        self.TSNLabel = QLabel(f"{sun_high}/{sun_low}")

        temps = {
            "Monday":self.TMLabel, 
            "Tuesday":self.TTLabel, 
            "Wednesday":self.TWLabel, 
            "Thursday":self.TTHLabel, 
            "Friday":self.TFLabel, 
            "Saturday":self.TSLabel, 
            "Sunday":self.TSNLabel
        }

        tempsOrdered = [temps[week_list[i]] for i in range(7)]
        tempLabelsAlign = [label.setAlignment(QtCore.Qt.AlignCenter) for label in tempsOrdered]
        tempLabelsAlign

        for item in tempsOrdered:
            item.setFont(QFont('Arial',8))

        tempsLabelLayout.addWidget(tempsOrdered[0],1,0)
        tempsLabelLayout.addWidget(tempsOrdered[1],1,1)
        tempsLabelLayout.addWidget(tempsOrdered[2],1,2)
        tempsLabelLayout.addWidget(tempsOrdered[3],1,3)
        tempsLabelLayout.addWidget(tempsOrdered[4],1,4)
        tempsLabelLayout.addWidget(tempsOrdered[5],1,5)
        tempsLabelLayout.addWidget(tempsOrdered[6],1,6)

        self.button = QPushButton("C")
        self.button.setFont(QFont('Arial',7))
        self.button.setFixedSize(11,11)
        self.button.setStyleSheet(
            "border : 0px solid gray;"
            "background-color: rgb(255,165,0);"
            "border-radius: 3px;"
            "margin-right: 1px;"
            "color: rgb(19,19,19);"
        )

        self.button.clicked.connect(self.the_button_was_clicked)

    

        tempsLabelLayout.addWidget(self.button, 0,7)



        self.button2 = QPushButton("V")
        self.button2.setFixedSize(11,11)
        self.button2.setFont(QFont('Arial',7))
        self.button2.setStyleSheet(
            "border : 0px solid gray;"
            "background-color: rgb(255,165,0);"
            "border-radius: 3px;"
            "margin-right: 1px;"
            "color: rgb(19,19,19);"
        )
        tempsLabelLayout.addWidget(self.button2, 1,7)


        widget = QWidget()
        widget.setLayout(tempsLabelLayout)
        tempsLabelLayout.setContentsMargins(2,2,2,2)
        tempsLabelLayout.setSpacing(0)
        self.setCentralWidget(widget)

        self.oldPos = self.pos()
    
    def the_button_was_clicked(self):
        if self.button.text() == "F":
            self.button.setText("C")
            mon_high = max_T[week_list.index('Monday')][0][3].split(".")[0]
            mon_low = min_T[week_list.index('Monday')][0][3].split(".")[0]
            tues_high = max_T[week_list.index('Tuesday')][0][3].split(".")[0]
            tues_low = min_T[week_list.index('Tuesday')][0][3].split(".")[0]
            wed_high = max_T[week_list.index('Wednesday')][0][3].split(".")[0]
            wed_low = min_T[week_list.index('Wednesday')][0][3].split(".")[0]
            thurs_high = max_T[week_list.index('Thursday')][0][3].split(".")[0]
            thurs_low = min_T[week_list.index('Thursday')][0][3].split(".")[0]
            fri_high = max_T[week_list.index('Friday')][0][3].split(".")[0]
            fri_low = min_T[week_list.index('Friday')][0][3].split(".")[0]
            sat_high = max_T[week_list.index('Saturday')][0][3].split(".")[0]
            sat_low = min_T[week_list.index('Saturday')][0][3].split(".")[0]
            sun_high = max_T[week_list.index('Sunday')][0][3].split(".")[0]
            sun_low = min_T[week_list.index('Sunday')][0][3].split(".")[0]
            self.TMLabel.setText(f"{mon_high}/{mon_low}")
            self.TTLabel.setText(f"{tues_high}/{tues_low}")
            self.TWLabel.setText(f"{wed_high}/{wed_low}")
            self.TTHLabel.setText(f"{thurs_high}/{thurs_low}")
            self.TFLabel.setText(f"{fri_high}/{fri_low}")
            self.TSLabel.setText(f"{sat_high}/{sat_low}")
            self.TSNLabel.setText(f"{sun_high}/{sun_low}")
            return
        if self.button.text() == "C":
            self.button.setText("F")
            mon_high = str(float(max_T[week_list.index('Monday')][0][3].split(".")[0]) * 1.8 + 32)
            mon_low = str(float(min_T[week_list.index('Monday')][0][3].split(".")[0]) * 1.8 + 32)
            tues_high = str(float(max_T[week_list.index('Tuesday')][0][3].split(".")[0]) * 1.8 + 32)
            tues_low = str(float(min_T[week_list.index('Tuesday')][0][3].split(".")[0]) * 1.8 + 32)
            wed_high = str(float(max_T[week_list.index('Wednesday')][0][3].split(".")[0]) * 1.8 + 32)
            wed_low = str(float(min_T[week_list.index('Wednesday')][0][3].split(".")[0]) * 1.8 + 32)
            thurs_high = str(float(max_T[week_list.index('Thursday')][0][3].split(".")[0]) * 1.8 + 32)
            thurs_low = str(float(min_T[week_list.index('Thursday')][0][3].split(".")[0]) * 1.8 + 32)
            fri_high = str(float(max_T[week_list.index('Friday')][0][3].split(".")[0]) * 1.8 + 32)
            fri_low = str(float(min_T[week_list.index('Friday')][0][3].split(".")[0]) * 1.8 + 32)
            sat_high = str(float(max_T[week_list.index('Saturday')][0][3].split(".")[0]) * 1.8 + 32)
            sat_low = str(float(min_T[week_list.index('Saturday')][0][3].split(".")[0]) * 1.8 + 32)
            sun_high = str(float(max_T[week_list.index('Sunday')][0][3].split(".")[0]) * 1.8 + 32)
            sun_low = str(float(min_T[week_list.index('Sunday')][0][3].split(".")[0]) * 1.8 + 32)
            self.TMLabel.setText(f"{mon_high}/{mon_low}")
            self.TTLabel.setText(f"{tues_high}/{tues_low}")
            self.TWLabel.setText(f"{wed_high}/{wed_low}")
            self.TTHLabel.setText(f"{thurs_high}/{thurs_low}")
            self.TFLabel.setText(f"{fri_high}/{fri_low}")
            self.TSLabel.setText(f"{sat_high}/{sat_low}")
            self.TSNLabel.setText(f"{sun_high}/{sun_low}")
            return 
    
    def the_button2_was_clicked(self):
        print("wow")

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, e):
        self.oldPos = e.globalPosition().toPoint()

    def mouseMoveEvent(self, e):
        delta = QPoint(e.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = e.globalPosition().toPoint()
        print("wow")
        
# Only need one per application
app = QApplication(sys.argv)
palette = QPalette()
palette.setColor(QPalette.Window, QColor(19,19,19))
palette.setColor(QPalette.WindowText, QColor(255,165,0))
app.setPalette(palette)

# Creating a new widget, which will be the window
w = MainWindow()
w.show() # Windows are hidden by default

# Starts the event loop
app.exec()






