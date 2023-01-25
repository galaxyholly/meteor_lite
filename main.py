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
        self.setWindowTitle("MeteorLite")
            
        tempsLabelLayout = QGridLayout()

        self.setGeometry(300, 60, 400, 30)
            
        MondayLabel = QLabel("M")
        TuesdayLabel = QLabel("T")
        WednesdayLabel = QLabel("W")
        ThursdayLabel = QLabel("TH")
        FridayLabel = QLabel("F")
        SaturdayLabel = QLabel("S")
        SundayLabel = QLabel("SN")  

        tempLabels = {
            "Monday":MondayLabel, 
            "Tuesday":TuesdayLabel, 
            "Wednesday":WednesdayLabel, 
            "Thursday":ThursdayLabel, 
            "Friday":FridayLabel, 
            "Saturday":SaturdayLabel, 
            "Sunday":SundayLabel
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

        TMLabel = QLabel(f"{mon_high}/{mon_low}")
        TTLabel = QLabel(f"{tues_high}/{tues_low}")
        TWLabel = QLabel(f"{wed_high}/{wed_low}")
        TTHLabel = QLabel(f"{thurs_high}/{thurs_low}")
        TFLabel = QLabel(f"{fri_high}/{fri_low}")
        TSLabel = QLabel(f"{sat_high}/{sat_low}")
        TSNLabel = QLabel(f"{sun_high}/{sun_low}")

        temps = {
            "Monday":TMLabel, 
            "Tuesday":TTLabel, 
            "Wednesday":TWLabel, 
            "Thursday":TTHLabel, 
            "Friday":TFLabel, 
            "Saturday":TSLabel, 
            "Sunday":TSNLabel
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

        button = QPushButton("C")
        button.setFont(QFont('Arial',7))
        button.setFixedSize(11,11)
        button.setStyleSheet(
            "border : 0px solid gray;"
            "background-color: rgb(255,165,0);"
            "border-radius: 3px;"
            "margin-right: 1px;"
            "color: rgb(19,19,19);"
        )
        button.clicked.connect(button.setText("F"))
        tempsLabelLayout.addWidget(button, 0,7)



        button2 = QPushButton("")
        button2.setFixedSize(11,11)
        button2.setStyleSheet(
            "border : 0px solid gray;"
            "background-color: rgb(255,165,0);"
            "border-radius: 3px;"
            "margin-right: 1px;"
        )
        tempsLabelLayout.addWidget(button2, 1,7)


        widget = QWidget()
        widget.setLayout(tempsLabelLayout)
        tempsLabelLayout.setContentsMargins(2,2,2,2)
        tempsLabelLayout.setSpacing(0)
        self.setCentralWidget(widget)

    #     self.oldPos = self.pos()

    # def center(self):
    #     qr = self.frameGeometry()
    #     cp = QGuiApplication.primaryScreen().availableGeometry().center()
    #     qr.moveCenter(cp)
    #     self.move(qr.topLeft())

    # def mousePressEvent(self, e):
    #     self.oldPos = e.globalPosition().toPoint()

    # def mouseMoveEvent(self, e):
    #     delta = QPoint(e.globalPosition().toPoint() - self.oldPos)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     self.oldPos = e.globalPosition().toPoint()
    #     print("wow")
        
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






