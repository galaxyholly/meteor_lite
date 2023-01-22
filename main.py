from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QGridLayout
from weatherGetter import *

# needed for command line args
import sys
startup()



def sort_week_from_today():
    date, time, weekday = date_time_2()
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    weekday_num = weekdays.index(weekday)
    new_weekdays = [weekdays[weekday_num:] + weekdays[:weekday_num]]
    return new_weekdays[0]

def display_week(data_types, unit):
    data_standard_format = data_list(sql_unformatted_by_date(con, data_types), data_types, unit) #Sends the user data to the formatting function data_list.
    data_by_day = sort_24(data_standard_format) # Returns a dictionary for information by day with keys 0-6 (str)
    num1 = len(data_by_day)
    num2 = num1 - 7
    week_list = [data_by_day[str(num2 + i)] for i in range(7)]
    week_list.append(unit)
    return week_list

week_list = sort_week_from_today()
print(str(week_list) + "WEEKLIST")
max_T = display_week(data_types[2], "C")
min_T = display_week(data_types[3], "C")
print(min_T)
print(max_T)

mon_high = max_T[week_list.index('Monday')][0][3]
mon_low = min_T[week_list.index('Monday')][0][3]
tues_high = max_T[week_list.index('Tuesday')][0][3]
tues_low = min_T[week_list.index('Tuesday')][0][3]
wed_high = max_T[week_list.index('Wednesday')][0][3]
wed_low = min_T[week_list.index('Wednesday')][0][3]
thurs_high = max_T[week_list.index('Thursday')][0][3]
thurs_low = min_T[week_list.index('Thursday')][0][3]
fri_high = max_T[week_list.index('Friday')][0][3]
fri_low = min_T[week_list.index('Friday')][0][3]
sat_high = max_T[week_list.index('Saturday')][0][3]
sat_low = min_T[week_list.index('Saturday')][0][3]
sun_high = max_T[week_list.index('Sunday')][0][3]
sun_low = min_T[week_list.index('Sunday')][0][3]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MeteorLite")
        

        tempsLabelLayout = QGridLayout()
        self.setFixedSize(600, 100)
        
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

        tempsLabelLayout.addWidget(tempsOrdered[0],1,0)
        tempsLabelLayout.addWidget(tempsOrdered[1],1,1)
        tempsLabelLayout.addWidget(tempsOrdered[2],1,2)
        tempsLabelLayout.addWidget(tempsOrdered[3],1,3)
        tempsLabelLayout.addWidget(tempsOrdered[4],1,4)
        tempsLabelLayout.addWidget(tempsOrdered[5],1,5)
        tempsLabelLayout.addWidget(tempsOrdered[6],1,6)

        button = QPushButton("See Hourly")
        tempsLabelLayout.addWidget(button, 2,0,2,3)

        button2 = QPushButton("Arduino")
        tempsLabelLayout.addWidget(button2, 2,4,2,3)

        # button2.clicked.connect()

        widget = QWidget()
        widget.setLayout(tempsLabelLayout)
        tempsLabelLayout.setContentsMargins(0,0,0,0)
        self.setCentralWidget(widget)




# Only need one per application
app = QApplication(sys.argv)

# Creating a new widget, which will be the window
w = MainWindow()
w.show() # Windows are hidden by default

# Starts the event loop
app.exec()






