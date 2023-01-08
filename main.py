from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QGridLayout
from weatherGetter import User, get_ip

# needed for command line args
import sys

mon_high = "1"
mon_low = "1"
tues_high = "1"
tues_low = "1"
wed_high = "1"
wed_low = "1"
thurs_high = "1"
thurs_low = "1"
fri_high = "1"
fri_low = "1"
sat_high = "1"
sat_low = "1"
sun_high = "1"
sun_low = "1"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MeteorLite")
        

        tempsLabelLayout = QGridLayout()
        self.setFixedSize(350, 100)
        
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

        tempLabelsSize = [label.setFixedSize(25,25) for label in temps]
        tempLabelsSize

        tempsSize = [label.setFixedSize(25,25) for label in tempLabels]
        tempsSize

        tempsLabelLayout.addWidget(TMLabel,1,0)
        tempsLabelLayout.addWidget(TTLabel,1,1)
        tempsLabelLayout.addWidget(TWLabel,1,2)
        tempsLabelLayout.addWidget(TTHLabel,1,3)
        tempsLabelLayout.addWidget(TFLabel,1,4)
        tempsLabelLayout.addWidget(TSLabel,1,5)
        tempsLabelLayout.addWidget(TSNLabel,1,6)

        button = QPushButton("Update")
        tempsLabelLayout.addWidget(button, 2,0,2,3)

        button2 = QPushButton("WoW")
        tempsLabelLayout.addWidget(button2, 2,4,2,3)

        # button2.clicked.connect()

        def updateTemps():
            print()

    
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






