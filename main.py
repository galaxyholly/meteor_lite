from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QGridLayout
from weatherGetter import *

# needed for command line args
import sys
startup()
data_standard_format = data_list(sql_unformatted_by_date(con), data_types[0], "degC") #Sends the user data to the formatting function data_list.
data_by_day = sort_24(data_standard_format) # Returns a dictionary for information by day with keys 0-6 (str)
print(data_by_day)
mon_high_num = str(data_by_day["3"][0][3])
print(mon_high_num)



mon_high = mon_high_num
mon_low = "1"
tues_high = data_by_day["4"][0][3]
tues_low = "1"
wed_high = data_by_day["5"][0][3]
wed_low = "1"
thurs_high = data_by_day["6"][0][3]
thurs_low = "1"
fri_high = data_by_day["0"][0][3]
fri_low = "1"
sat_high = data_by_day["1"][0][3]
sat_low = "1"
sun_high = data_by_day["2"][0][3]
sun_low = "1"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MeteorLite")
        

        tempsLabelLayout = QGridLayout()
        self.setFixedSize(400, 100)
        
        MLabel = QLabel("M")
        TLabel = QLabel("T")
        WLabel = QLabel("W")
        THLabel = QLabel("TH")
        FLabel = QLabel("F")
        SLabel = QLabel("S")
        SNLabel = QLabel("SN")  

        tempLabels = [
            MLabel,
            TLabel,
            WLabel,
            THLabel,
            FLabel,
            SLabel,
            SNLabel
        ]

        tempsAlign = [label.setAlignment(QtCore.Qt.AlignCenter) for label in tempLabels]
        tempsAlign      

        tempsLabelLayout.addWidget(MLabel,0,0)
        tempsLabelLayout.addWidget(TLabel,0,1)
        tempsLabelLayout.addWidget(WLabel,0,2)
        tempsLabelLayout.addWidget(THLabel,0,3)
        tempsLabelLayout.addWidget(FLabel,0,4)
        tempsLabelLayout.addWidget(SLabel,0,5)
        tempsLabelLayout.addWidget(SNLabel,0,6)

        TMLabel = QLabel(f"{mon_high}/{mon_low}")
        TTLabel = QLabel(f"{tues_high}/{tues_low}")
        TWLabel = QLabel(f"{wed_high}/{wed_low}")
        TTHLabel = QLabel(f"{thurs_high}/{thurs_low}")
        TFLabel = QLabel(f"{fri_high}/{fri_low}")
        TSLabel = QLabel(f"{sat_high}/{sat_low}")
        TSNLabel = QLabel(f"{sun_high}/{sun_low}")

        temps = [
            TMLabel,
            TTLabel,
            TWLabel,
            TTHLabel,
            TFLabel,
            TSLabel,
            TSNLabel
        ]

        tempLabelsAlign = [label.setAlignment(QtCore.Qt.AlignCenter) for label in temps]
        tempLabelsAlign

        tempsLabelLayout.addWidget(TMLabel,1,0)
        tempsLabelLayout.addWidget(TTLabel,1,1)
        tempsLabelLayout.addWidget(TWLabel,1,2)
        tempsLabelLayout.addWidget(TTHLabel,1,3)
        tempsLabelLayout.addWidget(TFLabel,1,4)
        tempsLabelLayout.addWidget(TSLabel,1,5)
        tempsLabelLayout.addWidget(TSNLabel,1,6)

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






