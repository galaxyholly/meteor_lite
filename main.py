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


temp_7days_24 = current_data('temperature', 'C')
temp_7days_24_extend = extend_hours(temp_7days_24)


# print(temp_7days_24_extend['0'])
# for item in temp_7days_24_extend:
#     for subitem in temp_7days_24_extend[item]:
#         print(temp_7days_24_extend[item][subitem])



wind_7days_24 = current_data('windSpeed', 'kph')
wind_7days_24_extend = extend_hours(wind_7days_24)
winddir_7days_24 = current_data('windDirection', '?')
winddir_7days_24_extend = extend_hours(winddir_7days_24)
skycover_7days_24 = current_data('skyCover', '%')
skycover_7days_24_extend = extend_hours(skycover_7days_24)
precipPer_7days_24 = current_data('probabilityOfPrecipitation', '%')
precipPer_7days_24_extend= extend_hours(precipPer_7days_24)
precipTot_7days_24 = current_data('quantitativePrecipitation', 'cm')
precipTot_7days_24_extend = extend_hours(precipTot_7days_24)

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

highLowList = [mon_high, mon_low, tues_high, tues_low, wed_high, wed_low, thurs_high, thurs_low, fri_high, fri_low, sat_high, sat_low, sun_high, sun_low]

class AnotherWindow(QWidget):
    # Is a QWidget. If it has no parent, it will appear as a free floating window.
    def __init__(self, dataName):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.day = dataName # Is just the name
        print(self.day)

        day_no = str(week_list.index(self.day))
        time_rn = time_right_now()
        print(time_rn)
        

        temp_rn = str(temp_7days_24_extend[day_no][time_rn][3] + "°")
        windSpd_rn = str(wind_7days_24_extend[day_no][time_rn][3] + "kph")
        skyCover_rn = str(skycover_7days_24_extend[day_no][time_rn][3] + "%")
        windDir_rn = str(winddir_7days_24_extend[day_no][time_rn][3] + "°")
        precipPer_rn = str(precipPer_7days_24_extend[day_no][time_rn][3] + "%")
        precipTot_rn = str(precipTot_7days_24_extend[day_no][time_rn][3] + "cm")
        

        vert1 = QVBoxLayout()
        horz1 = QHBoxLayout()
        vert2 = QVBoxLayout()
        grid1 = QGridLayout()

        vert1.addLayout(horz1) # Main strip containing top box, graph, bottomlabel
        horz1.addLayout(vert2) # This a vertical and a grid, which will house most of the info.
        horz1.addLayout(grid1)

        dayLabel = QLabel(f"{dataName}")
        dayLabel.setFont(QFont('Arial', 12))

        currentTemp = QLabel(f"{temp_rn}")
        currentTemp.setFont(QFont('Arial', 21))
        currentTemp.setStyleSheet(
            "color: white;"
        )
        vert2.addWidget(dayLabel)
        vert2.addWidget(currentTemp)

        windLabel = QLabel("Wind")
        windLabel.setFont(QFont('Arial', 10))

        currentWind = QLabel(f"{windSpd_rn}")
        currentWind.setFont(QFont('Arial', 10))

        currentWindDirection = QLabel(f"{windDir_rn}")
        currentWindDirection.setFont(QFont('Arial', 10))

        currentSkycover = QLabel(f"{skyCover_rn}")
        currentSkycover.setFont(QFont('Arial', 10))

        currentPrecipPercent = QLabel(f"{precipPer_rn}")
        currentPrecipPercent.setFont(QFont('Arial', 10))

        currentPrecipTotal = QLabel(f"{precipTot_rn}")
        currentPrecipTotal.setFont(QFont('Arial', 10))
        
        grid1.addWidget(windLabel,0,0)
        grid1.addWidget(currentWind,1,0)
        grid1.addWidget(currentWindDirection,2,0)
        grid1.addWidget(currentSkycover,0,1)
        grid1.addWidget(currentPrecipTotal, 1,1)
        grid1.addWidget(currentPrecipPercent, 2,1)
        


        


        # self.button2 = QPushButton("V")
        # self.button2.setFixedSize(11,11)
        # self.button2.setFont(QFont('Arial',7))
        # self.button2.setStyleSheet(
        #     "border : 0px solid gray;"
        #     "background-color: rgb(255,165,0);"
        #     "border-radius: 3px;"
        #     "margin-right: 1px;"
        #     "color: rgb(19,19,19);"
        # )
        # tempsLabelLayout.addWidget(self.button2, 1,7)
        
        # self.label = QLabel("Another Window")
        # layout.addWidget(self.label)
        self.setLayout(vert1)
        horz1.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

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

    

class hoverLabel(QLabel):
    def __init__(self, stuff, day, parent=None):
        super(hoverLabel, self).__init__(parent)
        self.dayData = day
        self.stuff = stuff
        self.setText(stuff)

    def enterEvent(self, QEvent):
        # here the code for mouse hover
        self.w = AnotherWindow(self.dayData)
        self.w.setGeometry(1920, 30, 400, 75)
        self.w.show()
            
    def leaveEvent(self, QEvent):
        # here the code for mouse leave - perhaps I need to look at the fact that the label is the parent to the window (maybe?) so I can 
        # Find a way to set mouse pointer conditions to only close the window when it's out of the thing.
        # once leave label, check if mouse is still ontop of window elements, if so do nothing, else: close?
        self.w.close()
        self.w = None 





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("MeteorLite")
        self.setStyleSheet("border-radius: 25px;")
        self.w = None
        self.setGeometry(1920, 0, 400, 30)

        horizontalLabelHolder = QHBoxLayout()

        vert1 = QVBoxLayout()
        vert2 = QVBoxLayout()
        vert3 = QVBoxLayout()
        vert4 = QVBoxLayout()
        vert5 = QVBoxLayout()
        vert6 = QVBoxLayout()
        vert7 = QVBoxLayout()
        vert8 = QVBoxLayout()

        vertList = [vert1, vert2, vert3, vert4, vert5, vert6, vert7, vert8]


        addVert = [horizontalLabelHolder.addLayout(obj) for obj in vertList]
        addVert
            
        self.MondayLabel = hoverLabel(f"M\n{mon_high}/{mon_low}", "Monday")
        self.TuesdayLabel = hoverLabel(f"T\n{tues_high}/{tues_low}", "Tuesday")
        self.WednesdayLabel = hoverLabel(f"W\n{wed_high}/{wed_low}", "Wednesday")
        self.ThursdayLabel = hoverLabel(f"TH\n{thurs_high}/{thurs_low}", "Thursday")
        self.FridayLabel = hoverLabel(f"F\n{fri_high}/{fri_low}", "Friday")
        self.SaturdayLabel = hoverLabel(f"S\n{sat_high}/{sat_low}", "Saturday")
        self.SundayLabel = hoverLabel(f"SN\n{sun_high}/{sun_low}", "Sunday")  

        tempLabels = {
            "Monday":self.MondayLabel,
            "Tuesday":self.TuesdayLabel,
            "Wednesday":self.WednesdayLabel,
            "Thursday":self.ThursdayLabel,
            "Friday":self.FridayLabel,
            "Saturday":self.SaturdayLabel,
            "Sunday":self.SundayLabel
        }

        tempsOrdered = [tempLabels[week_list[i]] for i in range(7)]
        tempLabelsAlign = [label.setAlignment(QtCore.Qt.AlignCenter) for label in tempsOrdered]
        tempLabelsAlign

        fontSet = [item.setFont(QFont('Arial', 8)) for item in tempsOrdered]
        fontSet

        vert1.addWidget(tempsOrdered[0])
        vert2.addWidget(tempsOrdered[1])
        vert3.addWidget(tempsOrdered[2])
        vert4.addWidget(tempsOrdered[3])
        vert5.addWidget(tempsOrdered[4])
        vert6.addWidget(tempsOrdered[5])
        vert7.addWidget(tempsOrdered[6])

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
        vert8.addWidget(self.button)
        self.button.clicked.connect(self.the_button_was_clicked)

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
        vert8.addWidget(self.button2)

        widget = QWidget()
        widget.setLayout(horizontalLabelHolder)
        horizontalLabelHolder.setContentsMargins(2,2,2,2)
        horizontalLabelHolder.setSpacing(0)
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
            self.MondayLabel.setText(f"M\n{mon_high}/{mon_low}")
            self.TuesdayLabel.setText(f"T\n{tues_high}/{tues_low}")
            self.WednesdayLabel.setText(f"W\n{wed_high}/{wed_low}")
            self.ThursdayLabel.setText(f"TH\n{thurs_high}/{thurs_low}")
            self.FridayLabel.setText(f"F\n{fri_high}/{fri_low}")
            self.SaturdayLabel.setText(f"S\n{sat_high}/{sat_low}")
            self.SundayLabel.setText(f"SN\n{sun_high}/{sun_low}")
            return
        if self.button.text() == "C":
            self.button.setText("F")
            mon_high = str(float(max_T[week_list.index('Monday')][0][3].split(".")[0]) * 1.8 + 32).split(".")[0]
            mon_low = str(float(min_T[week_list.index('Monday')][0][3].split(".")[0]) * 1.8 + 32).split(".")[0]
            tues_high = str(float(max_T[week_list.index('Tuesday')][0][3].split(".")[0]) * 1.8 + 32).split(".")[0]
            tues_low = str(float(min_T[week_list.index('Tuesday')][0][3].split(".")[0]) * 1.8 + 32).split(".")[0]
            wed_high = str(float(max_T[week_list.index('Wednesday')][0][3].split(".")[0]) * 1.8 + 32).split(".")[0]
            wed_low = str(float(min_T[week_list.index('Wednesday')][0][3].split(".")[0]) * 1.8 + 32).split(".")[0]
            thurs_high = str(float(max_T[week_list.index('Thursday')][0][3].split(".")[0]) * 1.8 + 32).split(".")[0]
            thurs_low = str(float(min_T[week_list.index('Thursday')][0][3].split(".")[0]) * 1.8 + 32).split(".")[0]
            fri_high = str(float(max_T[week_list.index('Friday')][0][3].split(".")[0]) * 1.8 + 32).split(".")[0]
            fri_low = str(float(min_T[week_list.index('Friday')][0][3].split(".")[0]) * 1.8 + 32).split(".")[0]
            sat_high = str(float(max_T[week_list.index('Saturday')][0][3].split(".")[0]) * 1.8 + 32).split(".")[0]
            sat_low = str(float(min_T[week_list.index('Saturday')][0][3].split(".")[0]) * 1.8 + 32).split(".")[0]
            sun_high = str(float(max_T[week_list.index('Sunday')][0][3].split(".")[0]) * 1.8 + 32).split(".")[0]
            sun_low = str(float(min_T[week_list.index('Sunday')][0][3].split(".")[0]) * 1.8 + 32).split(".")[0]
            self.MondayLabel.setText(f"M\n{mon_high}/{mon_low}")
            self.TuesdayLabel.setText(f"T\n{tues_high}/{tues_low}")
            self.WednesdayLabel.setText(f"W\n{wed_high}/{wed_low}")
            self.ThursdayLabel.setText(f"TH\n{thurs_high}/{thurs_low}")
            self.FridayLabel.setText(f"F\n{fri_high}/{fri_low}")
            self.SaturdayLabel.setText(f"S\n{sat_high}/{sat_low}")
            self.SundayLabel.setText(f"SN\n{sun_high}/{sun_low}")
            return 

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






