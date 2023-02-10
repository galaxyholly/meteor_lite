from PySide6 import QtCore
from PySide6.QtCore import *
from PySide6.QtWidgets import * # QApplication, QMainWindow, QLabel, QWidget, QPushButton, QGridLayout
from PySide6.QtGui import *
from weatherGetter import *

# needed for command line args
import sys
startup()
settings = settings_startup()


week_list = sort_week_from_today()

max_T = display_week(data_types[2], "C")
min_T = display_week(data_types[3], "C")

temp_7days_24 = current_data('temperature', 'C')
temp_7days_24_extend = extend_hours(temp_7days_24)
print(str(week_list) + "WEEKLIST")

try:
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
    vis_7days_24 = current_data('visibility', '%')
    vis_7days_24_extend = extend_hours(vis_7days_24)
    humid_7days_24 = current_data('quantitativePrecipitation', 'cm')
    humid_7days_24_extend = extend_hours(humid_7days_24)
    dew_7days_24 = current_data('dewpoint', 'C')
    dew_7days_24_extend = extend_hours(dew_7days_24)
except:
    wind_7days_24_extend = "0"
    winddir_7days_24_extend = "0"
    skycover_7days_24_extend = "0"
    precipPer_7days_24_extend = "0"
    precipTot_7days_24_extend = "0"
    vis_7days_24_extend = "0"
    humid_7days_24_extend = "0"
    dew_7days_24_extend = "0"


# mon_high = max_T[week_list.index('Monday')][0][3].split(".")[0]
# mon_low = min_T[week_list.index('Monday')][0][3].split(".")[0]
# tues_high = max_T[week_list.index('Tuesday')][0][3].split(".")[0]
# tues_low = min_T[week_list.index('Tuesday')][0][3].split(".")[0]
# wed_high = max_T[week_list.index('Wednesday')][0][3].split(".")[0]
# wed_low = min_T[week_list.index('Wednesday')][0][3].split(".")[0]
# thurs_high = max_T[week_list.index('Thursday')][0][3].split(".")[0]
# thurs_low = min_T[week_list.index('Thursday')][0][3].split(".")[0]
# fri_high = max_T[week_list.index('Friday')][0][3].split(".")[0]
# fri_low = min_T[week_list.index('Friday')][0][3].split(".")[0]
# sat_high = max_T[week_list.index('Saturday')][0][3].split(".")[0]
# sat_low = min_T[week_list.index('Saturday')][0][3].split(".")[0]
# sun_high = max_T[week_list.index('Sunday')][0][3].split(".")[0]
# sun_low = min_T[week_list.index('Sunday')][0][3].split(".")[0]

mon_high = "0"
mon_low = "0"
tues_high = "0"
tues_low = "0"
wed_high = "0"
wed_low = "0"
thurs_high = "0"
thurs_low = "0"
fri_high = "0"
fri_low = "0"
sat_high = "0"
sat_low = "0"
sun_high = "0"
sun_low = "0"

highLowList = [mon_high, mon_low, tues_high, tues_low, wed_high, wed_low, thurs_high, thurs_low, fri_high, fri_low, sat_high, sat_low, sun_high, sun_low]

class AnotherWindow(QWidget):
    # Is a QWidget. If it has no parent, it will appear as a free floating window.
    def __init__(self, dataName):
        super().__init__()

        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.day = dataName # Is just the name
        print(self.day)

        day_no = str(week_list.index(self.day))
        time_rn = time_right_now()
        print(time_rn)
        

        try:
            temp_rn = str(temp_7days_24_extend[day_no][time_rn][3] + "°")
        except KeyError:
            temp_rn = "No Data"
        try:
            windSpd_rn = str(wind_7days_24_extend[day_no][time_rn][3] + "kph")
        except KeyError:
            windSpd_rn = "No Data"
        try:
            skyCover_rn = str(skycover_7days_24_extend[day_no][time_rn][3] + "%")
        except KeyError:
            skyCover_rn = "No Data"
        try:
            windDir_rn = str(winddir_7days_24_extend[day_no][time_rn][3] + "°")
        except KeyError:
            windDir_rn = "No Data"
        try:
            precipPer_rn = str(precipPer_7days_24_extend[day_no][time_rn][3] + "%")
        except KeyError:
            precipPer_rn = "No Data"
        try:
            precipTot_rn = str(precipTot_7days_24_extend[day_no][time_rn][3] + "cm")
        except KeyError:
            precipTot_rn = "No Data"
        try:
            vis_rn = str(vis_7days_24_extend[day_no][time_rn][3] + "%")
        except KeyError:
            vis_rn = "No Data"
        try:
            humid_rn = str(humid_7days_24_extend[day_no][time_rn][3] + "%")
        except KeyError:
            humid_rn = "No Data"
        try:
            dew_rn = str(dew_7days_24_extend[day_no][time_rn][3] + "°")
        except KeyError:
            dew_rn = "No Data"
        
        
        verticalAlertOver = QVBoxLayout()
        verticalAlertOver.setContentsMargins(0,0,0,0)
        vert1 = QVBoxLayout()
        horz1 = QHBoxLayout()
        vert2 = QVBoxLayout()
        grid1 = QGridLayout()

        verticalAlertOver.addLayout(horz1)
        horz1.addLayout(vert1) # Main strip containing top box, graph, bottomlabel
        vert1.addLayout(grid1) # This a vertical and a grid, which will house most of the info.
        horz1.addLayout(vert2)

        dayLabel = QLabel(f"{dataName}")
        dayLabel.setFont(QFont('Gill Sans', 12))
        dayLabel.setStyleSheet(
            "margin-right: 3px;"
            "margin-bottom: 0px;"
        )

        grid1.setVerticalSpacing(0)
        grid1.setHorizontalSpacing(10)

        currentTemp = QLabel(f"{temp_rn}")
        currentTemp.setFont(QFont('Gill Sans', 21))
        currentTemp.setStyleSheet(
            "color: white;"
            "margin-right: 3px;"
            "margin-top: 0px;"
        )

        

        currentSkycover = QLabel(f"{skyCover_rn}")
        currentSkycover.setFont(QFont('Gill Sans', 10))

        currentPrecipLabel = QLabel("Precipitation")
        currentPrecipLabel.setFont(QFont('Gill Sans', 10))

        currentPrecipPercent = QLabel(f"{precipPer_rn}")
        currentPrecipPercent.setFont(QFont('Gill Sans', 10))

        currentPrecipTotal = QLabel(f"{precipTot_rn}")
        currentPrecipTotal.setFont(QFont('Gill Sans', 10))

        currentVisLabel = QLabel("Visibility")
        currentVisLabel.setFont(QFont('Gill Sans', 10))

        currentVis = QLabel(f"{vis_rn}")
        currentVis.setFont(QFont('Gill Sans', 10))

        humidLabel = QLabel("Humidity")
        humidLabel.setFont(QFont('Gill Sans', 10))

        currentHumid = QLabel(f"{humid_rn}")
        currentHumid.setFont(QFont('Gill Sans', 10))

        currentDewpoint = QLabel(f"{dew_rn}")
        currentDewpoint.setFont(QFont('Gill Sans', 10))

        self.labelContainerTemps = QWidget()
        self.labelContainerTempsLayout = QGridLayout(self.labelContainerTemps)
        self.labelContainerTempsLayout.addWidget(dayLabel)
        self.labelContainerTempsLayout.addWidget(currentTemp)
        self.labelContainerTemps.setStyleSheet(
            "background-color: rgb(105,105,105);"
            "border-radius: 3px;"
        )
        
        self.labelContainerTemps.setContentsMargins(0,0,0,0)
        self.labelContainerTempsLayout.setVerticalSpacing(10)

        grid1.addWidget(self.labelContainerTemps, 0, 0, 3, 1)

        windLabel = QLabel("Wind")
        windLabel.setFont(QFont('Gill Sans', 10))

        currentWind = QLabel(f"{windSpd_rn}")
        currentWind.setFont(QFont('Gill Sans', 10))

        currentWindDirection = QLabel(f"{windDir_rn}")
        currentWindDirection.setFont(QFont('Gill Sans', 10))

        self.windDirectionCompass = QDial()

        self.windWidgetWrapper = QWidget()
        self.windWidgetWrapperLayout = QGridLayout(self.windWidgetWrapper)
        self.windWidgetWrapperLayout.addWidget(windLabel)
        self.windWidgetWrapperLayout.addWidget(currentWind)
        self.windWidgetWrapperLayout.addWidget(currentWindDirection)
        self.windWidgetWrapperLayout.addWidget(self.windDirectionCompass)
        self.windWidgetWrapper.setContentsMargins(0,0,0,0)
        self.windWidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
            "background-color: rgb(105,105,105);"
        )

        grid1.addWidget(self.windWidgetWrapper, 0,2,3,1)

        self.precipitationWidgetWrapper = QWidget()
        self.precipitationWidgetWrapperLayout = QGridLayout(self.precipitationWidgetWrapper)
        self.precipitationWidgetWrapperLayout.addWidget(currentPrecipLabel)
        self.precipitationWidgetWrapperLayout.addWidget(currentPrecipPercent)
        self.precipitationWidgetWrapperLayout.addWidget(currentPrecipTotal)
        self.precipitationWidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
            "background-color: rgb(105,105,105);"
        )
        grid1.addWidget(self.precipitationWidgetWrapper, 0,3,3,1)

        self.visibilityWidgetWrapper = QWidget()
        self.visibilityWidgetWrapperLayout = QGridLayout(self.visibilityWidgetWrapper)
        self.visibilityWidgetWrapperLayout.addWidget(currentVisLabel)
        self.visibilityWidgetWrapperLayout.addWidget(currentVis)
        self.visibilityWidgetWrapperLayout.addWidget(currentSkycover)
        self.visibilityWidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
            "background-color: rgb(105,105,105);"
        )
        grid1.addWidget(self.visibilityWidgetWrapper, 0,4,3,1)

        self.humidityWidgetWrapper = QWidget()
        self.humidityWidgetWrapperLayout = QGridLayout(self.humidityWidgetWrapper)
        self.humidityWidgetWrapperLayout.addWidget(humidLabel)
        self.humidityWidgetWrapperLayout.addWidget(currentHumid)
        self.humidityWidgetWrapperLayout.addWidget(currentDewpoint)
        self.humidityWidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
            "background-color: rgb(105,105,105);"
            "border: 1px gray;"
        )
        grid1.addWidget(self.humidityWidgetWrapper, 0,5,3,1)
        grid1.setVerticalSpacing(5)
        grid1.setContentsMargins(5,5,5,5)

        self.alertLabel = QLabel("Alerts\n" + "lolololoolollolololoolollolololoolollolololoolollolololoolollolololoolol\nlolololoolollolololoolollolololoolollolololoolollolololoolollolololoolol\nlolololoolollolololoolollolololoolollolololoolollolololoolollolololoolol\n")
        self.alertLabel.setFont(QFont('Gill Sans', 10))
        self.alertLabel.setStyleSheet(
            "color: green;"
            "background-color: rgb(127, 255, 212);"
        )
        self.alertLabel.setAlignment(QtCore.Qt.AlignHCenter)
        # self.alertLabel.setMaximumSize(400, 1500)
        verticalAlertOver.addWidget(self.alertLabel)
        self.alertLabel.hide()


        self.setLayout(verticalAlertOver)
        grid1.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

    def showAlerts(self):
        self.alertLabel.show()
        self.adjustSize()


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



class SettingsListWidget(QListWidget):
    clickedSignal = Signal(object)
    listSignal = Signal(str, bool)
    def __init__(self, parent=None, max_select = 5):
        super().__init__(parent)
        self.max_widgets_allowed = max_select
        self.setSelectionMode(QListWidget.MultiSelection)
        self.setMouseTracking(True)
        self.clickedSignal.connect(self.itemSelector)

    def focusInEvent(self, placeholder):
        pass
    def focusOutEvent(self, placeholder):
        pass

    def mousePressEvent(self, event): # Emits the clickedSignal that carries the event object.
        self.clickedSignal.emit(event.pos())
    
    def mouseMoveEvent(self, event): # This overrides the default handler. This is here to stop a highlighting issue where the user would click and drag on an item and it wouldn't trigger the signal but still leave the item highlighted. Fixed by disabling mouseMoveEvent and creating my own mousePressEvent handler with custom signals.
        pass
    
    def itemSelector(self, object):
        item = self.itemAt(object)
        if item in self.selectedItems():
            item.setSelected(False)
            self.listSignal.emit(item.text(), False)
        elif item not in self.selectedItems():
            if len(self.selectedItems()) < 5:
                item.setSelected(True)
                self.listSignal.emit(item.text(), True)
            else:
                print("Limit Reached")
        
class settingsComboBox(QComboBox):
    selectionSignal = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)

        
class SettingsWindow(QWidget):
    unitsSignal = Signal(str)
    def __init__(self):
        super().__init__()
        self.settingsPage = QWidget()
        settingsLayout = QVBoxLayout(self.settingsPage)
        self.setGeometry(0,0,400,400)
        self.setLayout(settingsLayout)

        self.widgetsLabel = QLabel("Widgets (Pop-up Information Window)")
        self.widgetsLabel.setFont(QFont('Gill Sans', 10))
        self.widgetsLabel.setAlignment(Qt.AlignLeft)

        self.settingsLabel = QLabel("Settings")
        self.settingsLabel.setFont(QFont('Gill Sans', 12))
        self.settingsLabel.setAlignment(Qt.AlignHCenter)

        self.unitsLabel = QLabel("Units")
        self.unitsLabel.setFont(QFont('Gill Sans', 10))
        self.unitsLabel.setAlignment(Qt.AlignLeft)   

        self.themesLabel = QLabel("Themes")
        self.themesLabel.setFont(QFont('Gill Sans', 10))
        self.themesLabel.setAlignment(Qt.AlignLeft)

        
        # POPUP WIDGET MENU START
        popupWindowWidgetsLayout = QHBoxLayout()
        self.widgetsList = SettingsListWidget(self)
        self.widgetsList.addItems(["Temperature", "Humidity/Dewpoint", "Wind", "Precipitation", "Visibility", "Heat Index", "Transport Wind", "Snow/Ice", "Ceiling/Mixing Height", "Haines/Grassland Fire", "20ft Windspeed/Direction", "Lightning Activity"])
        self.widgetsListItems = []
        self.widgetsList.setCurrentItem(None)
        self.widgetsList.listSignal.connect(self.workingWidgetList)
        # POPUP WIDGET MENU ENDING


        # UNITS OPTIONS HERE
        self.unitSelector = settingsComboBox()
        self.unitSelector.addItems(["Celsius", "Fahrenheit", "Kelvin"])
        self.updatedUnitSetting = []
        self.unitSelector.currentIndexChanged.connect(self.unitSettingsList)
        print(self.unitSelector.currentText())
        # UNITS OPTIONS END HERE

        # THEME OPTIONS
        self.themeSelector = settingsComboBox()
        self.themeSelector.addItems(["MeteorLite", "Midnight Pink", "Blue Skies", "Acid Rain"])
        self.updatedThemeSetting = []
        self.themeSelector.currentIndexChanged.connect(self.themeSettingsList)
        
        self.widgetButton = QPushButton("Save")
        self.widgetButton.clicked.connect(self.saveSettings)

        settingsLayout.addWidget(self.settingsLabel)
        settingsLayout.addWidget(self.widgetsLabel)
        settingsLayout.addLayout(popupWindowWidgetsLayout)
        
        settingsLayout.addWidget(self.unitsLabel)
        settingsLayout.addWidget(self.unitSelector)
        settingsLayout.addWidget(self.themesLabel)
        settingsLayout.addWidget(self.themeSelector)
        settingsLayout.addWidget(self.widgetButton)
        settingsLayout.setSpacing(0)
        settingsLayout.setContentsMargins(0,0,0,0)
        popupWindowWidgetsLayout.addWidget(self.widgetsList)
        popupWindowWidgetsLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

    def workingWidgetList(self, item, t_f):
        if t_f == True:
            if self.widgetsListItems == 5:
                print("Limit Reached")
            else:
                self.widgetsListItems.append([item, 1])
                print(self.widgetsListItems)
        elif t_f == False:
            self.widgetsListItems.remove([item, 1])
            print(self.widgetsListItems)
    
    def unitSettingsList(self, row):
        unitsDict = {0:"Celsius", 1:"Fahrenheit", 2:"Kelvin"}
        self.updatedUnitSetting = [unitsDict[row], 1]
        print(self.updatedUnitSetting)
    
    def themeSettingsList(self, row):
        themesDict = {0:"MeteorLite", 1:"Midnight Pink", 2:"Blue Skies", 3:"Acid Rain"}
        self.updatedThemeSetting = ["Theme", themesDict[row]]

    def saveSettings(self):
        referenceList = [['Temperature', 0],['Humidity/Dewpoint', 0],['Heat Index', 0],['Wind', 0],['Precipitation', 0],['Visibility', 0],['Transport Wind', 0],['Snow/Ice', 0],['Ceiling/Mixing Height', 0],['Haines/Grassland Fire', 0],['20ft Windspeed/Direction', 0],['Lightning Activity', 0], ['Celsius', 0],['Fahrenheit', 0],['Kelvin', 0],['Theme', 'MeteorLite']]
        if self.updatedUnitSetting != []:
            self.widgetsListItems.append(self.updatedUnitSetting)
        elif self.updatedUnitSetting == []:
            self.updatedUnitSetting = ["Celsius", 1]
            self.widgetsListItems.append(self.updatedUnitSetting)
        if self.updatedThemeSetting != []:
            referenceList[-1] = self.updatedThemeSetting
        newWidgetIndexes = [referenceList.index([item[0], 0]) for item in self.widgetsListItems]
        for index in newWidgetIndexes:
            referenceList[index] = self.widgetsListItems[newWidgetIndexes.index(index)]
        print(referenceList)
        newSettings = Settings(referenceList[0], referenceList[1], referenceList[2], referenceList[3], referenceList[4], referenceList[5], referenceList[6], referenceList[7], referenceList[8], referenceList[9], referenceList[10], referenceList[11], referenceList[12], referenceList[13], referenceList[14], referenceList[15])
        print(newSettings.apparentTemp_heatIndx)
        sql_settings_gui_insert(con, newSettings)# Now store this settings with the settings method, then refresh gui? Don't actually return this...
        self.close() # Add functionality to not allow user to have 0 selected pop up cards. Now add something that checks settings for theme before it opens.

class hoverLabel(QLabel):
    def __init__(self, stuff, day, parent=None):
        super(hoverLabel, self).__init__(parent)
        # self.setAttribute(Qt.WA_Hover)
        self.dayData = day
        self.stuff = stuff
        self.setText(stuff)
        self.n_times_clicked = 0
        self.setContentsMargins(0,0,0,0)
        self.w = AnotherWindow(self.dayData)
        self.w.setGeometry(1920, 55, 400, 75)
        self.w.setMaximumSize(400, 75)
        self.w.hide()


    def mousePressEvent(self, e):
        if self.n_times_clicked == 0:
            self.w.alertLabel.show()
            self.n_times_clicked += 1
        elif self.n_times_clicked == 1:
            self.w.alertLabel.hide()
            self.n_times_clicked -= 1

    def enterEvent(self, QEvent):
        # here the code for mouse hover
        self.w.show()

    def leaveEvent(self, QEvent):
        # here the code for mouse leave - perhaps I need to look at the fact that the label is the parent to the window (maybe?) so I can 
        # Find a way to set mouse pointer conditions to only close the window when it's out of the thing.
        # once leave label, check if mouse is still ontop of window elements, if so do nothing, else: close?
        self.n_times_clicked = 0
        self.w.hide()
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.Window |  Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowTitle("MeteorLite")
        self.setGeometry(1920, 0, 400, 30)
        self.setContentsMargins(0,0,0,0)
        # self.w = None

        horizontalLabelHolder = QHBoxLayout()
        
        vert1 = QVBoxLayout()
        vert2 = QVBoxLayout()
        vert3 = QVBoxLayout()
        vert4 = QVBoxLayout()
        vert5 = QVBoxLayout()
        vert6 = QVBoxLayout()
        vert7 = QVBoxLayout()
        vert8 = QVBoxLayout()

        horizontalLabelHolder.addLayout(vert1)
        horizontalLabelHolder.addLayout(vert2)
        horizontalLabelHolder.addLayout(vert3)
        horizontalLabelHolder.addLayout(vert4)
        horizontalLabelHolder.addLayout(vert5)
        horizontalLabelHolder.addLayout(vert6)
        horizontalLabelHolder.addLayout(vert7)
        horizontalLabelHolder.addLayout(vert8)

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

        
        tempLabelsMargins = [label.setContentsMargins(0,0,0,0) for label in tempsOrdered]
        tempLabelsMargins

        stylesheetLabels = [label.setStyleSheet("") for label in tempsOrdered]
        stylesheetLabels

        fontSet = [item.setFont(QFont('Gill Sans', 8)) for item in tempsOrdered]
        fontSet

        vert1.addWidget(tempsOrdered[0])
        vert2.addWidget(tempsOrdered[1])
        vert3.addWidget(tempsOrdered[2])
        vert4.addWidget(tempsOrdered[3])
        vert5.addWidget(tempsOrdered[4])
        vert6.addWidget(tempsOrdered[5])
        vert7.addWidget(tempsOrdered[6])

        self.button = QPushButton("")
        self.button.setIcon(QIcon('icons8settings.png'))
        self.button.setFixedSize(12,14)
        self.button.setStyleSheet(
            "border : 0px solid gray;"
        )
        self.button.clicked.connect(self.settingsClicked)

        self.button2 = QPushButton("")
        self.button2.setIcon(QIcon('icons8-expand-arrow-24.png'))
        # <a target="_blank" href="https://icons8.com/icon/83214/settings">Settings</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        self.button2.setFixedSize(12,12)
        self.button2.setStyleSheet(
            "border : 0px solid gray;"
        )

        self.button_container = QWidget()
        self.button_container.setFixedSize(16,30)
        self.button_container.setContentsMargins(0,0,0,0)
        
        self.button_container_layout = QVBoxLayout(self.button_container)
        self.button_container_layout.addWidget(self.button)
        self.button_container_layout.addWidget(self.button2)
        self.button_container_layout.setSpacing(0)
        self.button_container_layout.setContentsMargins(0,2,0,2)
         
        vert8.addWidget(self.button_container)
        vert8.setContentsMargins(0,0,3,0)

        widget = QWidget()
        widget.setLayout(horizontalLabelHolder)
        horizontalLabelHolder.setContentsMargins(0,0,0,0)
        horizontalLabelHolder.setSpacing(0)
        # horizontalLabelHolder.setSpacing(5)
        
        
        self.setCentralWidget(widget)
        self.oldPos = self.pos()
        print(settings.fahrenheit)
        if settings.fahrenheit[2] == 1:
            self.cToF()
        
            


    def openInfoWindow(self):
        print("dangus")

    def cToF(self):
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

    def fToC(self):
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
            
    
    def settingsClicked(self):
        self.settings = SettingsWindow()
        # if settings_start.temperature
        self.settings.show()
        
        # self.settings.tempsCheckbox.stateChanged.connect(self.tempsToggle)
        # self.settings.windCheckBox.stateChanged.connect(self.windToggle)
        # self.settings.precipitationCheckBox.stateChanged.connect(self.precipitationToggle)
        # self.settings.visibilityCheckBox.stateChanged.connect(self.visibilityToggle)
        # self.settings.humidityCheckBox.stateChanged.connect(self.humidityToggle)

        # Now for a section to init the settings.
         
            

    def tempsToggle(self):
        if self.settings.tempsCheckbox.isChecked() == True:
            self.MondayLabel.w.labelContainerTemps.show()
            self.TuesdayLabel.w.labelContainerTemps.show()
            self.WednesdayLabel.w.labelContainerTemps.show()
            self.ThursdayLabel.w.labelContainerTemps.show()
            self.FridayLabel.w.labelContainerTemps.show()
            self.SaturdayLabel.w.labelContainerTemps.show()
            self.SundayLabel.w.labelContainerTemps.show()
        elif self.settings.tempsCheckbox.isChecked() == False:
            self.MondayLabel.w.labelContainerTemps.hide()
            self.TuesdayLabel.w.labelContainerTemps.hide()
            self.WednesdayLabel.w.labelContainerTemps.hide()
            self.ThursdayLabel.w.labelContainerTemps.hide()
            self.FridayLabel.w.labelContainerTemps.hide()
            self.SaturdayLabel.w.labelContainerTemps.hide()
            self.SundayLabel.w.labelContainerTemps.hide()

    def windToggle(self):
        if self.settings.windCheckBox.isChecked() == True:
            self.MondayLabel.w.windWidgetWrapper.show()
            self.TuesdayLabel.w.windWidgetWrapper.show()
            self.WednesdayLabel.w.windWidgetWrapper.show()
            self.ThursdayLabel.w.windWidgetWrapper.show()
            self.FridayLabel.w.windWidgetWrapper.show()
            self.SaturdayLabel.w.windWidgetWrapper.show()
            self.SundayLabel.w.windWidgetWrapper.show()
        elif self.settings.windCheckBox.isChecked() == False:
            self.MondayLabel.w.windWidgetWrapper.hide()
            self.TuesdayLabel.w.windWidgetWrapper.hide()
            self.WednesdayLabel.w.windWidgetWrapper.hide()
            self.ThursdayLabel.w.windWidgetWrapper.hide()
            self.FridayLabel.w.windWidgetWrapper.hide()
            self.SaturdayLabel.w.windWidgetWrapper.hide()
            self.SundayLabel.w.windWidgetWrapper.hide()

    def precipitationToggle(self):
        if self.settings.precipitationCheckBox.isChecked() == True:
            self.MondayLabel.w.precipitationWidgetWrapper.show()
            self.TuesdayLabel.w.precipitationWidgetWrapper.show()
            self.WednesdayLabel.w.precipitationWidgetWrapper.show()
            self.ThursdayLabel.w.precipitationWidgetWrapper.show()
            self.FridayLabel.w.precipitationWidgetWrapper.show()
            self.SaturdayLabel.w.precipitationWidgetWrapper.show()
            self.SundayLabel.w.precipitationWidgetWrapper.show()
        elif self.settings.precipitationCheckBox.isChecked() == False:
            self.MondayLabel.w.precipitationWidgetWrapper.hide()
            self.TuesdayLabel.w.precipitationWidgetWrapper.hide()
            self.WednesdayLabel.w.precipitationWidgetWrapper.hide()
            self.ThursdayLabel.w.precipitationWidgetWrapper.hide()
            self.FridayLabel.w.precipitationWidgetWrapper.hide()
            self.SaturdayLabel.w.precipitationWidgetWrapper.hide()
            self.SundayLabel.w.precipitationWidgetWrapper.hide()

    def visibilityToggle(self):
        if self.settings.visibilityCheckBox.isChecked() == True:
            self.MondayLabel.w.visibilityWidgetWrapper.show()
            self.TuesdayLabel.w.visibilityWidgetWrapper.show()
            self.WednesdayLabel.w.visibilityWidgetWrapper.show()
            self.ThursdayLabel.w.visibilityWidgetWrapper.show()
            self.FridayLabel.w.visibilityWidgetWrapper.show()
            self.SaturdayLabel.w.visibilityWidgetWrapper.show()
            self.SundayLabel.w.visibilityWidgetWrapper.show()
        elif self.settings.visibilityCheckBox.isChecked() == False:
            self.MondayLabel.w.visibilityWidgetWrapper.hide()
            self.TuesdayLabel.w.visibilityWidgetWrapper.hide()
            self.WednesdayLabel.w.visibilityWidgetWrapper.hide()
            self.ThursdayLabel.w.visibilityWidgetWrapper.hide()
            self.FridayLabel.w.visibilityWidgetWrapper.hide()
            self.SaturdayLabel.w.visibilityWidgetWrapper.hide()
            self.SundayLabel.w.visibilityWidgetWrapper.hide()

    def humidityToggle(self):
        if self.settings.humidityCheckBox.isChecked() == True:
            self.MondayLabel.w.humidityWidgetWrapper.show()
            self.TuesdayLabel.w.humidityWidgetWrapper.show()
            self.WednesdayLabel.w.humidityWidgetWrapper.show()
            self.ThursdayLabel.w.humidityWidgetWrapper.show()
            self.FridayLabel.w.humidityWidgetWrapper.show()
            self.SaturdayLabel.w.humidityWidgetWrapper.show()
            self.SundayLabel.w.humidityWidgetWrapper.show()
        elif self.settings.humidityCheckBox.isChecked() == False:
            self.MondayLabel.w.humidityWidgetWrapper.hide()
            self.TuesdayLabel.w.humidityWidgetWrapper.hide()
            self.WednesdayLabel.w.humidityWidgetWrapper.hide()
            self.ThursdayLabel.w.humidityWidgetWrapper.hide()
            self.FridayLabel.w.humidityWidgetWrapper.hide()
            self.SaturdayLabel.w.humidityWidgetWrapper.hide()
            self.SundayLabel.w.humidityWidgetWrapper.hide()


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






