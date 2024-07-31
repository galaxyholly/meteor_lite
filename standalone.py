from PySide6 import QtCore
from PySide6.QtCore import *
from PySide6.QtWidgets import * # QApplication, QMainWindow, QLabel, QWidget, QPushButton, QGridLayout
from PySide6.QtGui import *
from weatherGetter import *

import math
import sys

startUpdateTimes = startup() # This initializes an instance of the User class and does a GET request for 7-day weather data.
start_time = startUpdateTimes[0] # This is just here in case I decide I want graphs to show only data from current time to end of day as opposed to the last weatherstation update time to end of day.
update_time = startUpdateTimes[1] # This denotes the time the weather station posts the next update. Used for the QThread that auto-updates.

themePalettes = {"MeteorLite": (QColor(255,165,0), "(255,165,0)"), "Midnight Pink": (QColor(255,39,95),"(255,39,95)"), "Blue Skies": (QColor(135,206,235),"(135,206,235)"), "Acid Rain": (QColor(210,227,199),"(210,227,199)")}
# themePalettes is just here for easy palette editing.
week_list = sort_week_from_today() # arranges a 7-day list starting with the current day.

zone_difference = 6 # This is not currently in significant use. This is once again something I may choose to use later. It's used for manual time zone adjustment.


# These are the week long processed weather datas. All of these need try except blocks to catch NOAA errors.
temp_7days_24_extend = extend_hours(current_data('temperature', 'C', zone_difference))
wind_7days_24_extend = extend_hours(current_data('windSpeed', 'kph', zone_difference))
winddir_7days_24_extend = extend_hours(current_data('windDirection', '?', zone_difference))
skycover_7days_24_extend = extend_hours(current_data('skyCover', '%', zone_difference))
precipPer_7days_24_extend= extend_hours(current_data('probabilityOfPrecipitation', '%', zone_difference))
precipTot_7days_24_extend = extend_hours(current_data('quantitativePrecipitation', 'cm', zone_difference))
try:
    vis_7days_24_extend = extend_hours(current_data('visibility', '%', zone_difference))
except:
    vis_7days_24_extend = "N/A"
humid_7days_24_extend = extend_hours(current_data('quantitativePrecipitation', 'cm', zone_difference))
dew_7days_24_extend = extend_hours(current_data('dewpoint', 'C', zone_difference))
apparent_7days_24_extend = extend_hours(current_data('apparentTemperature', 'C', zone_difference))
try:
    heatIndex_7days_24_extend = extend_hours(current_data('heatIndex', 'C', zone_difference))
except KeyError:
    heatIndex_7days_24_extend = "none"
gust_7days_24_extend = extend_hours(current_data('windGust', 'kph', zone_difference))
ice_7days_24_extend = extend_hours(current_data('iceAccumulation', 'cm', zone_difference))
snow_7days_24_extend = extend_hours(current_data('snowfallAmount', 'cm', zone_difference))
try:
    ceiling_7days_24_extend = extend_hours(current_data('ceilingHeight', 'm', zone_difference))
except:
    ceiling_7days_24_extend = "N/A"
trnspd_7days_24_extend = extend_hours(current_data('transportWindSpeed', 'kph', zone_difference))
trndir_7days_24_extend = extend_hours(current_data('transportWindDirection', '°', zone_difference))
mixing_7days_24_extend = extend_hours(current_data('mixingHeight', 'm', zone_difference))
try:
    haines_7days_24_extend = extend_hours(current_data('hainesIndex', "C", zone_difference))
except:
    haines_7days_24_extend = "N/A"
try:
    lightning_7days_24_extend = extend_hours(current_data('lightningActivityLevel', "Level", zone_difference))
except:
    lightning_7days_24_extend = "N/A"
try:
    ft20spd_7days_24_extend = extend_hours(current_data('twentyFootWindSpeed', 'kph', zone_difference))
except:
    ft20spd_7days_24_extend = "N/A"
try:
    ft20dir_7days_24_extend = extend_hours(current_data('twentyFootWindDirection', '°', zone_difference))
except:
    ft20dir_7days_24_extend = "N/A"
try:
    grass_7days_24_extend = extend_hours(current_data('grasslandFireDangerIndex', "Index", zone_difference))
except:
    grass_7days_24_extend = "N/A"
#This is a function to look at just the high/low temps for each day of the week.
# max_T = display_week(data_types[2], "C")
# min_T = display_week(data_types[3], "C")
# try:
#     mon_high = max_T[week_list.index('Monday')][0][3].split(".")[0]
#     mon_low = min_T[week_list.index('Monday')][0][3].split(".")[0]
#     tues_high = max_T[week_list.index('Tuesday')][0][3].split(".")[0]
#     tues_low = min_T[week_list.index('Tuesday')][0][3].split(".")[0]
#     wed_high = max_T[week_list.index('Wednesday')][0][3].split(".")[0]
#     wed_low = min_T[week_list.index('Wednesday')][0][3].split(".")[0]
#     thurs_high = max_T[week_list.index('Thursday')][0][3].split(".")[0]
#     thurs_low = min_T[week_list.index('Thursday')][0][3].split(".")[0]
#     fri_high = max_T[week_list.index('Friday')][0][3].split(".")[0]
#     fri_low = min_T[week_list.index('Friday')][0][3].split(".")[0]
#     sat_high = max_T[week_list.index('Saturday')][0][3].split(".")[0]
#     sat_low = min_T[week_list.index('Saturday')][0][3].split(".")[0]
#     sun_high = max_T[week_list.index('Sunday')][0][3].split(".")[0]
#     sun_low = min_T[week_list.index('Sunday')][0][3].split(".")[0]
# except:
#     mon_high = "0"
#     mon_low = "0"
#     tues_high = "0"
#     tues_low = "0"
#     wed_high = "0"
#     wed_low = "0"
#     thurs_high = "0"
#     thurs_low = "0"
#     fri_high = "0"
#     fri_low = "0"
#     sat_high = "0"
#     sat_low = "0"
#     sun_high = "0"
#     sun_low = "0"
# highLowList = [mon_high, mon_low, tues_high, tues_low, wed_high, wed_low, thurs_high, thurs_low, fri_high, fri_low, sat_high, sat_low, sun_high, sun_low]


class GraphLabel(QLabel): # This is a custom QLabel that can be used to display an entire day's worth of datapoints. It automatically formats the graph when the datapoints are passed as parameters.
    returnToBody = Signal(object)
    graphPaletteChangeSignal = Signal(object, object)
    def __init__(self, title, settings, width, margins, widgetBackgroundColor, valuesY, parent=None): # size, valuesY, tickNumberX, tickXSkipNumber, tickNumberY, tickTextX, textColor, axisTextX, axisTextY,
        super().__init__(parent)
        self.canvas = QPixmap(width-(margins[0]*2), 80)
        self.canvas.fill(widgetBackgroundColor)
        self.setPixmap(self.canvas)
        self.padding_horizontal = 25 # Set all the padding and tick numbers here. The class should auto calculate spacing and such.
        self.padding_vertical = 20
        self.ticks_horizontal = 7
        self.ticks_vertical = 4
        self.title = "Precipitation (mm)"
        self.valuesX = [0,3,6,9,12,15,18,21] # Not used
        self.valuesY = valuesY
        self.widgetBackgroundColor = widgetBackgroundColor
        self.draw_graph(self.title, self.padding_horizontal, self.padding_vertical, self.ticks_vertical, self.valuesY, self.widgetBackgroundColor, settings)
        self.graphPaletteChangeSignal.connect(self.settingsPaletteChanged)
        
    def settingsPaletteChanged(self, object, settings): # When the theme settings are changed this method is called and redraws the graph.
        print("Graph Palette Change Signal")
        self.draw_graph(self.title, self.padding_horizontal, self.padding_vertical, self.ticks_vertical, self.valuesY, self.widgetBackgroundColor, settings)
        
    def draw_graph(self, title, padding_horizontal, padding_vertical, ticks_vertical, values, widgetBackgroundColor, settings): # This method draws the graph. Each part is drawn separately (axis, points, lines, axis values title, etc...)
        print(settings.currentTheme)
        canvas = self.pixmap()
        dimensionsX = canvas.width() # dimensions are passed as parameters to the GraphLabel class so the canvas dimensions match the info widget dimensions.
        dimensionsY = canvas.height()
        painter = QPainter(canvas)

        tempPen = QPen()
        tempPen.setColor(widgetBackgroundColor)
        painter.setPen(tempPen)

        rectBrush = QBrush()
        rectBrush.setColor(widgetBackgroundColor)
        rectBrush.setStyle(Qt.SolidPattern)
        painter.setBrush(rectBrush)
        painter.drawRoundedRect(QRect(0,0,canvas.width()-1,canvas.height()-1), 2, 2) # This draws the rounded rectangle base canvas.

        tempPen = QPen()
        tempPen.setColor(Qt.white)
        painter.setPen(tempPen)

        horizontal_point_y = (dimensionsY - padding_vertical) # y-point at bottom (- padding)
        vertical_point_x = (dimensionsX - padding_horizontal) # x-point on right(- padding)
        x_axis_length = dimensionsX - (padding_horizontal*2) # Sets the x-axis length according to the padding passed in the class init.
        y_axis_length = dimensionsY - (padding_vertical*2) # Sets the y-axis length according to the padding passed in the class init.
        y_axis_tick_interval = y_axis_length/(ticks_vertical-1) # Sets the pixels between each y-axis tick. -1 because the x and y axis intersection counts as one.

        vertical_tick_spacing_list = []
        preValues = values.values() # These functions in this block can absolutely be made better. Don't have time right now. They can be combined into a nested list comprehension.
        nextValues = [item for item in preValues]
        hourValues = [item[2] for item in nextValues] # Arrived at this list of hours from the original list of values passed into the class.
        axisNumbers = [hourValues[i][11:13] for i in range(len(hourValues))] # This is just another reference list for the x-axis tick values.
            
        # for i in range(len(hourValues)): - This is left here in case time zone needs manually adjusted
        #     value = int(hourValues[i][11:13])
        #     if value >= 6:
        #         axisNumbers.append(value-2)
        #     elif value < 6:
        #         axisNumbers.append(value+(23-0+1))

        preList = [item[3] for item in nextValues] # Again nested comprehensions can condense this and make it faster. 
        finalList = [float(item)for item in preList] # An extra list left here in case floats are needed later.
        valuesList = [int(item) for item in finalList] # This is the list of numerical values to map each point on the graph to.
        maxV = max(valuesList) # This block essentially sets a ratio of dataunits per pixel, so that I can have for example, 10 pixels per 1 degree to make graphing consistent in the pixel space provided.
        minV =  min(valuesList)
        total_y_axis_range = abs(maxV-minV) + 20 # Gets total graphable x-axis pixels.
        starting_tick = minV-10 # these help space the ticks out on either side of the axis.
        ending_tick = maxV+10
        working_ticks = ticks_vertical-1 # Just makes a variable representing the total number of ticks minus the 0 tick at the beginning of the axis.
        total_distance = abs(starting_tick - ending_tick) # Gets a numerical number of pixels to work with between the ticks themselves.
        middle_ticks_distance = math.ceil(total_distance/(ticks_vertical-1)) # Gets pixel distance between ticks.
        ticks = [starting_tick + middle_ticks_distance*i for i in range(working_ticks)] # Gets a list of pixels each horizontal tick sits on. Starts at left most tick and goes by the pixel distance between ticks until it finishes.
        ticks.append(ending_tick)
        font = QFont()
        font.setPointSize(8)
        painter.setFont(font)
        pixels_per_value = y_axis_length/(total_y_axis_range) # this gets the pixels/value point. So like, pixels per degree.
        pixels_per_hour = (x_axis_length/24) # gets the distance between each hour in pixels.
        points_to_draw = []
        ref_points = [i for i in range(int(starting_tick), int(ending_tick)+1)] 
    
        for i in range(0, int(ticks_vertical)): # This draws vertical ticks
            tick_spacing_vertical = (horizontal_point_y - (y_axis_tick_interval*i))
            vertical_tick_spacing_list.append(tick_spacing_vertical)
            print(tick_spacing_vertical)
            painter.drawLine(padding_horizontal, tick_spacing_vertical, (padding_horizontal-2), tick_spacing_vertical) # This will be bottom-row ticks
        
        painter.drawLine(padding_horizontal, padding_vertical/2, padding_horizontal, horizontal_point_y) # draws the vertical axis
        painter.drawLine(padding_horizontal, horizontal_point_y, (vertical_point_x+(padding_horizontal/4)), horizontal_point_y) # draws the horizontal axis
        
        for i in range(0, int(ticks_vertical)): # makes the vertical tick numbers
            tick_spacing_vertical = (horizontal_point_y - (y_axis_tick_interval*i))
            painter.drawText(QRectF((padding_horizontal-20), (tick_spacing_vertical-7), 15, 15), Qt.AlignRight, str(int(ticks[i]))) # This will be bottom-row ticks

        for i in range(len(valuesList)): # makes the points to draw lines between. This is only here for extra graph options, like showing points and not just peaks and valleys.
            points_to_draw.append([math.ceil(padding_horizontal + i*pixels_per_hour),(horizontal_point_y - abs((ref_points.index(valuesList[i]))*pixels_per_value))])
        
        for i in range(len(points_to_draw)): # Draws the lines connecting the datapoints.
            try:
                graphPen = QPen()
                graphPen.setColor(themePalettes[settings.currentTheme[2]][0])
                painter.setPen(graphPen)
                painter.drawLine(points_to_draw[i][0], points_to_draw[i][1], points_to_draw[i+1][0], points_to_draw[i+1][1])
                
                if i%3 == 0: # This writes the numbers for the horizontal ticks.
                    tempPen = QPen()
                    tempPen.setColor(Qt.white)
                    painter.setPen(tempPen)
                    painter.drawLine(points_to_draw[i][0], horizontal_point_y, points_to_draw[i][0], (horizontal_point_y+2))
                    painter.drawText(QRectF((points_to_draw[i][0]-6), (horizontal_point_y + 5), 15, 15), Qt.AlignHCenter, str(int(axisNumbers[abs(i)]))) # Draws ticks on 3rd point.

            except IndexError:
                pass

        graphPen = QPen()
        graphPen.setColor(themePalettes[settings.currentTheme[2]][0]) #the settings object passed to this is what allows for easy color updating.
        painter.setPen(graphPen)
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(QRectF((dimensionsX/2 - 75), (5), 150, 50), Qt.AlignHCenter, f"{title}") # Just adds a title.
        painter.end() 
        self.setPixmap(canvas)

class AnotherWindow(QWidget): # This is the window containing all of the information widgets.
    def __init__(self, dataName, settings, width):
        super().__init__()

        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.day = dataName # Is just the name
        self.settings = settings # This is just a settings object used to inform the program what information widgets need to be shown on startup.
        self.widgetColor = "rgb(65,65,65)"
        self.widgetQColor = QColor(65,65,65)

        day_no = str(week_list.index(self.day))
        current_hour = datetime.now()
        hour_rn = current_hour.hour
        placeholder_rn = datetime(1,1,1,hour_rn,0,0)
        adjusted_time = placeholder_rn + timedelta(hours = 0)
        time_rn = int(adjusted_time.hour)
        if time_rn < 10:
            time_rn = "0" + str(time_rn)
        else:
            time_rn = str(time_rn)

        
        try: # These try-except blocks are here to account for there not being datapoints for a specific hour.
            print("ADJUSTED" + str(int(time_rn)))
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
        except:
            vis_rn = "No Data"
        try:
            humid_rn = str(humid_7days_24_extend[day_no][time_rn][3] + "%")
        except KeyError:
            humid_rn = "No Data"
        try:
            dew_rn = str(dew_7days_24_extend[day_no][time_rn][3] + "°")
        except KeyError:
            dew_rn = "No Data"
        try:
            apparent_rn = str(apparent_7days_24_extend[day_no][time_rn][3] + "°")
        except KeyError:
            apparent_rn = "No Data"
        try:
            heat_rn = str(heatIndex_7days_24_extend[day_no][time_rn][3] + "°")
        except TypeError:
            heat_rn = "No Data"
        except KeyError:
            heat_rn = "No Data"
        try:
            gust_rn = str(gust_7days_24_extend[day_no][time_rn][3] + "°")
        except KeyError:
            gust_rn = "No Data"
        try:
            ice_rn = str(ice_7days_24_extend[day_no][time_rn][3] + "°")
        except KeyError:
            ice_rn = "No Data"
        try:
            snow_rn = str(snow_7days_24_extend[day_no][time_rn][3] + "°")
        except KeyError:
            snow_rn = "No Data"
        try:
            ceiling_rn = str(ceiling_7days_24_extend[day_no][time_rn][3] + "°")
        except:
            ceiling_rn = "No Data"
        try:
            trnspd_rn = str(trnspd_7days_24_extend[day_no][time_rn][3] + "°")
        except:
            trnspd_rn = "No Data"
        try:
            trndir_rn = str(trndir_7days_24_extend[day_no][time_rn][3] + "°")
        except:
            trndir_rn = "No Data"
        try:
            mixing_rn = str(mixing_7days_24_extend[day_no][time_rn][3] + "°")
        except:
            mixing_rn = "No Data"
        try:
            haines_rn = str(haines_7days_24_extend[day_no][time_rn][3] + "°")
        except:
            haines_rn = "No Data"
        try:
            lightning_rn = str(lightning_7days_24_extend[day_no][time_rn][3] + "°")
        except:
            lightning_rn = "No Data"
        try:
            ft20spd_rn = str(ft20spd_7days_24_extend[day_no][time_rn][3] + "°")
        except:
            ft20spd_rn = "No Data"
        try:
            ft20dir_rn = str(ft20dir_7days_24_extend[day_no][time_rn][3] + "°")
        except:
            ft20dir_rn = "No Data"
        try:
            grass_rn = str(grass_7days_24_extend[day_no][time_rn][3] + "°")
        except:
            grass_rn = "No Data"

        self.verticalAlertOver = QVBoxLayout() # Outer layout to group the 3 rows together.
        self.verticalAlertOver.setContentsMargins(6,6,6,6)
        
        self.horz1 = QHBoxLayout() # These are the 3 rows in which the information widgets arrange.
        self.horz2 = QHBoxLayout()
        self.horz3 = QHBoxLayout()

        self.verticalAlertOver.addLayout(self.horz1)
        self.verticalAlertOver.addLayout(self.horz2)
        self.verticalAlertOver.addLayout(self.horz3)
        
        dayLabel = QLabel(f"{dataName}") # This next set of ###Label widgets are all the information and title labels.
        dayLabel.setFont(QFont('Gill Sans', 12))
        dayLabel.setStyleSheet(
            "margin-right: 3px;"
            "margin-bottom: 0px;"
        )

        currentTemp = QLabel(f"{temp_rn}C Current Temperature")
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

        self.currentPrecipGraph = GraphLabel("wow", settings, width, self.verticalAlertOver.getContentsMargins(), self.widgetQColor, temp_7days_24_extend[day_no])
        # currentPrecipGraph is special and is its own custom made class.

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

        windLabel = QLabel("Wind")
        windLabel.setFont(QFont('Gill Sans', 10))

        currentWind = QLabel(f"{windSpd_rn} Wind Speed")
        currentWind.setFont(QFont('Gill Sans', 10))

        currentWindDirection = QLabel(f"{windDir_rn} Wind Direction")
        currentWindDirection.setFont(QFont('Gill Sans', 10))

        currentWindGust = QLabel(f"{gust_rn} Wind Gust")
        currentWindGust.setFont(QFont('Gill Sans', 10))

        heatLabel = QLabel("Heat Index")
        heatLabel.setFont(QFont('Lucida sand unicode', 10))

        currentHeat = QLabel(f"{heat_rn} Heat Index")
        currentHeat.setFont(QFont('Lucida sand unicode', 10))

        currentApparentTemp = QLabel(f"{apparent_rn} Apparent Temperature")
        currentApparentTemp.setFont(QFont('Lucida sand unicode', 10))

        iceSnowLabel = QLabel("Snowfall/Ice")
        iceSnowLabel.setFont(QFont('Lucida sand unicode', 10))

        currentSnow = QLabel(f"{snow_rn} Snowfall")
        currentSnow.setFont(QFont('Lucida sand unicode', 10))

        currentIce = QLabel(f"{ice_rn} Ice Accumulation")
        currentIce.setFont(QFont('Lucida sand unicode', 10))

        ceilingLabel = QLabel("Ceiling Height")
        ceilingLabel.setFont(QFont('Lucida sand unicode', 10))

        currentCeiling = QLabel(f"{ceiling_rn} Ceiling Height")
        currentCeiling.setFont(QFont('Lucida sand unicode', 10))

        currentMixing = QLabel(f"{mixing_rn} Mixing Height")
        currentMixing.setFont(QFont('Lucida sand unicode', 10))

        ft20Label = QLabel("20ft Wind")
        ft20Label.setFont(QFont('Lucida sand unicode', 10))

        currentFt20Speed = QLabel(f"{ft20spd_rn} 20ft Wind Speed")
        currentFt20Speed.setFont(QFont('Lucida sand unicode', 10))

        currentFt20Direction = QLabel(f"{ft20dir_rn} 20ft Wind Direction")
        currentFt20Direction.setFont(QFont('Lucida sand unicode', 10))

        hainesLabel = QLabel(f"Fire Risk")
        hainesLabel.setFont(QFont('Lucida sand unicode', 10))

        currentHaines = QLabel(f"{haines_rn} Haines Index")
        currentHaines.setFont(QFont('Lucida sand unicode', 10))

        currentGrassland = QLabel(f"{grass_rn} Grassland Fire Index")
        currentGrassland.setFont(QFont('Lucida sand unicode', 10))

        lightningLabel = QLabel("Lightning Activity")
        lightningLabel.setFont(QFont('Lucida sand unicode', 10))

        currentLightning = QLabel(F"{lightning_rn} Lightning Activity")
        currentLightning.setFont(QFont('Lucida sand unicode', 10))

        transportLabel = QLabel("Transport Wind")
        transportLabel.setFont(QFont('Lucida sand unicode', 10))

        currentTransportSpeed = QLabel(f"{trnspd_rn} Transport Speed")
        currentTransportSpeed.setFont(QFont('Lucida sand unicode', 10))

        currentTransportDirection = QLabel(f"{trndir_rn} Transport Direction")
        currentTransportDirection.setFont(QFont('Lucida sand unicode', 10))
        

        self.labelContainerTemps = QWidget() # "containers" are just wrapper widgets to make sizing grouping easier.
        self.labelContainerTempsLayout = QGridLayout(self.labelContainerTemps)
        self.labelContainerTempsLayout.addWidget(dayLabel)
        self.labelContainerTempsLayout.addWidget(currentTemp)
        self.labelContainerTemps.setStyleSheet(
            f"background-color: {self.widgetColor};"
            "border-radius: 3px;"
        )
        self.labelContainerTemps.setContentsMargins(0,0,0,0)
        self.labelContainerTempsLayout.setVerticalSpacing(10)

        self.windWidgetWrapper = QWidget()
        self.windWidgetWrapperLayout = QGridLayout(self.windWidgetWrapper)
        self.windWidgetWrapperLayout.addWidget(windLabel)
        self.windWidgetWrapperLayout.addWidget(currentWind)
        self.windWidgetWrapperLayout.addWidget(currentWindDirection)
        self.windWidgetWrapper.setContentsMargins(0,0,0,0)
        self.windWidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
            f"background-color: {self.widgetColor};"
        )
        
        self.precipitationWidgetWrapper = QWidget()
        self.precipitationWidgetWrapperLayout = QGridLayout(self.precipitationWidgetWrapper)
        # self.precipitationWidgetWrapperLayout.addWidget(currentPrecipLabel)
        self.precipitationWidgetWrapperLayout.addWidget(self.currentPrecipGraph)
        # self.precipitationWidgetWrapperLayout.addWidget(currentPrecipTotal)
        self.precipitationWidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
            f"background-color: {self.widgetColor};"
            "padding: 0px;"
        )
        self.precipitationWidgetWrapperLayout.setContentsMargins(0,0,0,0)
        self.precipitationWidgetWrapperLayout.setSpacing(0)


        self.visibilityWidgetWrapper = QWidget()
        self.visibilityWidgetWrapperLayout = QGridLayout(self.visibilityWidgetWrapper)
        self.visibilityWidgetWrapperLayout.addWidget(currentVisLabel)
        self.visibilityWidgetWrapperLayout.addWidget(currentVis)
        self.visibilityWidgetWrapperLayout.addWidget(currentSkycover)
        self.visibilityWidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
            f"background-color: {self.widgetColor};"
        )

        self.humidityWidgetWrapper = QWidget()
        self.humidityWidgetWrapperLayout = QGridLayout(self.humidityWidgetWrapper)
        self.humidityWidgetWrapperLayout.addWidget(humidLabel)
        self.humidityWidgetWrapperLayout.addWidget(currentHumid)
        self.humidityWidgetWrapperLayout.addWidget(currentDewpoint)
        self.humidityWidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
            f"background-color: {self.widgetColor};"
            "border: 1px gray;"
        )

        self.heatIndexWidgetWrapper = QWidget()
        self.heatIndexWidgetWrapperLayout = QGridLayout(self.heatIndexWidgetWrapper)
        self.heatIndexWidgetWrapperLayout.addWidget(heatLabel)
        self.heatIndexWidgetWrapperLayout.addWidget(currentHeat)   
        self.heatIndexWidgetWrapperLayout.addWidget(currentApparentTemp)
        self.heatIndexWidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
            f"background-color: {self.widgetColor};"
            "border: 1px gray;"
        )

        self.transportWindWidgetWrapper = QWidget()
        self.transportWindWidgetWrapperLayout = QGridLayout(self.transportWindWidgetWrapper)
        self.transportWindWidgetWrapperLayout.addWidget(transportLabel)
        self.transportWindWidgetWrapperLayout.addWidget(currentTransportSpeed)
        self.transportWindWidgetWrapperLayout.addWidget(currentTransportDirection)
        self.transportWindWidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
            f"background-color: {self.widgetColor};"
            "border: 1px gray;"
        )

        self.snowIceWidgetWrapper = QWidget()
        self.snowIceWidgetWrapperLayout = QGridLayout(self.snowIceWidgetWrapper)
        self.snowIceWidgetWrapperLayout.addWidget(iceSnowLabel)
        self.snowIceWidgetWrapperLayout.addWidget(currentIce)
        self.snowIceWidgetWrapperLayout.addWidget(currentSnow)
        self.snowIceWidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
            f"background-color: {self.widgetColor};"
            "border: 1px gray;"
        )

        self.ceilingMixingWidgetWrapper = QWidget()
        self.ceilingMixingWidgetWrapperLayout = QGridLayout(self.ceilingMixingWidgetWrapper)
        self.ceilingMixingWidgetWrapperLayout.addWidget(ceilingLabel)
        self.ceilingMixingWidgetWrapperLayout.addWidget(currentCeiling)
        self.ceilingMixingWidgetWrapperLayout.addWidget(currentMixing)
        self.ceilingMixingWidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
        )


        self.hainesWidgetWrapper = QWidget()
        self.hainesWidgetWrapperLayout = QGridLayout()
        self.hainesWidgetWrapperLayout.addWidget(hainesLabel)
        self.hainesWidgetWrapperLayout.addWidget(currentHaines)
        self.hainesWidgetWrapperLayout.addWidget(currentGrassland)
        self.hainesWidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
            f"background-color: {self.widgetColor};"
            "border: 1px gray;"
        )

        self.ft20WidgetWrapper = QWidget()
        self.ft20WidgetWrapperLayout = QGridLayout()
        self.ft20WidgetWrapperLayout.addWidget(ft20Label)
        self.ft20WidgetWrapperLayout.addWidget(currentFt20Speed)
        self.ft20WidgetWrapperLayout.addWidget(currentFt20Direction)
        self.ft20WidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
            f"background-color: {self.widgetColor};"
            "border: 1px gray;"
        )

        self.lightningWidgetWrapper = QWidget()
        self.lightningWidgetWrapperLayout = QGridLayout()
        self.lightningWidgetWrapperLayout.addWidget(lightningLabel)
        self.lightningWidgetWrapperLayout.addWidget(currentLightning)
        self.lightningWidgetWrapper.setStyleSheet(
            "border-radius: 3px;"
            f"background-color: {self.widgetColor};"
            "border: 1px gray;"
        )
        
        values = settings.__dict__.values() # This gets the value lists of each setting.
        newSettingsList = convertSettingsToWidgets(values) # This just grabs all of the widgets set to "active"
        widgetsDict = {"Temperature": [self.labelContainerTemps, self.horz1], "Humidity/Dewpoint":[self.humidityWidgetWrapper, self.horz1], "Wind":[self.windWidgetWrapper, self.horz1], "Precipitation":[self.precipitationWidgetWrapper, self.horz3], "Visibility":[self.visibilityWidgetWrapper, self.horz1], "Heat Index":[self.heatIndexWidgetWrapper, self.horz2], "Transport Wind":[self.transportWindWidgetWrapper, self.horz2], "Snow/Ice":[self.snowIceWidgetWrapper, self.horz3], "Ceiling/Mixing Height":[self.ceilingMixingWidgetWrapper, self.horz2], "Haines/Grassland Fire":[self.hainesWidgetWrapper, self.horz2], "20ft Windspeed/Direction":[self.ft20WidgetWrapper, self.horz2], "Lightning Activity":[self.lightningWidgetWrapper, self.horz2]}
        # widgetsDict is a list that contains the information to fictate what row each widget goes into when added to the layout.
        for item in newSettingsList: # A handy iterator that adds only the "active" widgets to their respective layouts listed in the widgetsDict.
            widgetsDict[item[1]][1].addWidget(widgetsDict[item[1]][0])
        
        self.alertLabel = QLabel("Alerts\n" + "placeholder") # This is a placeholder to the alerts feature.
        self.alertLabel.setFont(QFont('Gill Sans', 10))
        self.alertLabel.setStyleSheet(
            "color: green;"
            "background-color: rgb(127, 255, 212);"
        )
        self.alertLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalAlertOver.addWidget(self.alertLabel)
        self.alertLabel.hide() # This is hidden by default until I decide what to do with it.

        self.setLayout(self.verticalAlertOver) # Sets the main layout of the AnotherWindow widget. Just boilerplate for QT.

    def showAlerts(self): # A method to be connected to a signal later on.
        self.alertLabel.show()
        self.adjustSize()

    def center(self): # center, mousePressEvent, and mouseMoveEvents were event filters I setup to allow the widgets in AnotherWindow to be clicked and dragged as a group. There's no current purpose as it's left over from another design. Leaving it because I think it's a fun quirk.
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
    
    def settingsPaletteChanged(self, object): # This will be used to update themes when a signal connects here. 
        theme = themePalettes[object.currentTheme[2]] # Sets theme to correct theme name
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(19,19,19)) # re-writes self.paletteW to new colors
        palette.setColor(QPalette.WindowText, theme) # re-writes self.paletteW to new colors
        self.setPalette(palette) # re-writes self.paletteW to new colors
        self.update()
        
class hoverLabel(QLabel): # Custom label that has custom event handlers to fire off signals when hovered and unhovered.
    enterSignal = Signal(str)
    leaveSignal = Signal(str)
    def __init__(self, text, day, parent=None):
        super(hoverLabel, self).__init__(parent)
        # self.setAttribute(Qt.WA_Hover)
        self.dayData = str(day)
        self.text = text
        self.setText(text)
        self.n_times_clicked = 0
        self.setContentsMargins(0,0,0,0)
        
    # def mousePressEvent(self, e): 
    #     if self.n_times_clicked == 0:
    #         self.w.alertLabel.show()
    #         self.n_times_clicked += 1
    #     elif self.n_times_clicked == 1:
    #         self.w.alertLabel.hide()
    #         self.w.adjustSize()
    #         self.n_times_clicked -= 1

    def enterEvent(self, QEvent):
        self.enterSignal.emit(self.dayData)

    def leaveEvent(self, QEvent):
        self.leaveSignal.emit(self.dayData)
        self.n_times_clicked = 0

class WeatherTab(QWidget): # This is the main information tab. 
    def __init__(self, width, windowHeight, parent=None):
        super().__init__(parent)
        
        self.outlineVertical = QVBoxLayout()
        self.days7_horizontal = QHBoxLayout() # Layout to contain the day labels. Will need updated when day passes.
        self.days7_horizontal.setSpacing(0)


        self.dayInfoWidget = QWidget()
        self.dayInfoStacked = QStackedLayout(self.dayInfoWidget) # Stacked layout allows for the 7-day hover labels to bring that day's info to the surface.
        self.dayInfoWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.dayInfoWidget.setFixedHeight((windowHeight/10)*6)
        self.dayInfoWidget.setStyleSheet(
            "background-color: rgb(45,45,45)"
        )

        self.weatherInfo1 = QWidget()
        self.weatherInfo1.setFixedWidth(width)
        self.weatherInfoWrapper1 = QVBoxLayout(self.weatherInfo1)
        self.weatherInfo1.setStyleSheet(
            "background-color: rgb(19,19,19);"
        )

        self.alertLabel = QLabel("Alerts")
        self.alertLabel.setAlignment(Qt.AlignHCenter)
        self.alertLabel.setStyleSheet(
            "border: solid gray;"
            "border-width: 1px 0px 0px 0px;"
        )
        # self.alertLabel.hide()

        self.MondayLabel = hoverLabel(f"Mon", "Monday")
        self.TuesdayLabel = hoverLabel(f"Tue", "Tuesday")
        self.WednesdayLabel = hoverLabel(f"Wed", "Wednesday")
        self.ThursdayLabel = hoverLabel(f"Thu", "Thursday")
        self.FridayLabel = hoverLabel(f"Fri", "Friday")
        self.SaturdayLabel = hoverLabel(f"Sat", "Saturday")
        self.SundayLabel = hoverLabel(f"Sun", "Sunday")

        self.tempLabels = {
            "Monday":self.MondayLabel,
            "Tuesday":self.TuesdayLabel,
            "Wednesday":self.WednesdayLabel,
            "Thursday":self.ThursdayLabel,
            "Friday":self.FridayLabel,
            "Saturday":self.SaturdayLabel,
            "Sunday":self.SundayLabel
        }

        tempsOrdered = [self.tempLabels[week_list[i]] for i in range(7)] # This adds the labels in order of current day-end of the week. Needs updated with passing of day.
        for item in tempsOrdered:
            self.days7_horizontal.addWidget(item)
            item.setFixedHeight(windowHeight/10)
            item.setStyleSheet(
                "border: solid gray;"
                "border-width: 0px 0px 1px 0px;"
            )

        tempLabelsAlign = [label.setAlignment(QtCore.Qt.AlignCenter) for label in tempsOrdered] # Just a condensed way of setting alignment for all labels
        tempLabelsAlign

        tempLabelsMargins = [label.setContentsMargins(0,0,0,0) for label in tempsOrdered] # convenient way of setting alignment.
        tempLabelsMargins

        self.testLabel = QLabel("wowow") # Was left over from earlier. Can probably delete.

        self.outlineVertical.addLayout(self.days7_horizontal)
        self.outlineVertical.addWidget(self.dayInfoWidget)
        self.outlineVertical.addWidget(self.alertLabel)
        self.outlineVertical.setContentsMargins(0,0,0,0)
        self.outlineVertical.setSpacing(0)

        self.setLayout(self.outlineVertical)

class SettingsListWidget(QListWidget): # This is a custom QListWidget that allows me to setup signals that facilitate the GUI changing with setting changes in real time.
    clickedSignal = Signal(object)
    listSignal = Signal(str, bool)
    widgetSignal = Signal(object, bool) # Routes to MainWindow method.
    def __init__(self, settings, parent=None, max_select = 5):
        super().__init__(parent)
        self.max_widgets_allowed = max_select
        self.setSelectionMode(QListWidget.MultiSelection)
        self.setMouseTracking(True)
        self.clickedSignal.connect(self.itemSelector)
        self.setStyleSheet(
            "border-radius: 3px;"
        )

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
            self.widgetSignal.emit(item.text(), False)
        elif item not in self.selectedItems():
            if len(self.selectedItems()) < 5:
                item.setSelected(True)
                self.listSignal.emit(item.text(), True)
                self.widgetSignal.emit(item.text(), True)
            else:
                print("Limit Reached")
        
class settingsComboBox(QComboBox): # This is just a custom QCombo that allows me to set the selectionSignal to control max select number.
    selectionSignal = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            "left: 0px;"
        )

class SettingsWindow(QWidget): # This is the settingsTab class.
    unitsSignal = Signal(str)
    settingsChangedSignal = Signal(object)
    def __init__(self, settings, windowWidth, windowHeight, parent=None):
        super().__init__(parent)
        self.settingsPage = QWidget()
        self.settingsLayout = QVBoxLayout(self.settingsPage)
        self.setGeometry(0,0,400,400)
        self.setLayout(self.settingsLayout)
        self.settings = settings

        self.settingsChangedSignal.connect(self.settingsPaletteChanged)
        
        # POPUP WIDGET MENU START
        self.widgetsWrapperWidget = QWidget()
        self.widgetsWrapperLayout = QVBoxLayout(self.widgetsWrapperWidget)

        self.widgetsLabel = QLabel("Widgets (Pop-up Information Window)")
        self.widgetsLabel.setFont(QFont('Gill Sans', 10))
        self.widgetsLabel.setAlignment(Qt.AlignLeft)

        self.settingsLabel = QLabel("Settings")
        self.settingsLabel.setFont(QFont('Gill Sans', 12))
        self.settingsLabel.setAlignment(Qt.AlignHCenter)

        self.widgetsList = SettingsListWidget(self)
        self.widgetsList.addItems(["Temperature", "Humidity/Dewpoint", "Wind", "Precipitation", "Visibility", "Heat Index", "Transport Wind", "Snow/Ice", "Ceiling/Mixing Height", "Haines/Grassland Fire", "20ft Windspeed/Direction", "Lightning Activity"])
        
        self.widgetsListItems = []
        self.widgetsList.setCurrentItem(None)
        self.widgetsList.listSignal.connect(self.workingWidgetList)

        self.widgetsWrapperLayout.addWidget(self.settingsLabel)
        self.widgetsWrapperLayout.addWidget(self.widgetsLabel)
        self.widgetsWrapperLayout.addWidget(self.widgetsList)
        self.widgetsWrapperWidget.setFixedHeight(int(windowHeight/10)*6)
        self.widgetsWrapperLayout.setSpacing(5)
        self.widgetsWrapperLayout.setContentsMargins(0,0,0,0)
        self.widgetsWrapperLayout.setAlignment(Qt.AlignVCenter)
        # POPUP WIDGET MENU ENDING

        # UNITS OPTIONS HERE
        self.unitsWrapperWidget = QWidget()
        self.unitsWrapperLayout = QVBoxLayout(self.unitsWrapperWidget)

        self.unitsLabel = QLabel("Units")
        self.unitsLabel.setFont(QFont('Gill Sans', 10))
        self.unitsLabel.setAlignment(Qt.AlignLeft | Qt.AlignBottom) 

        self.unitSelector = settingsComboBox()
        self.unitSelector.addItems(["Celsius", "Fahrenheit"])
        self.unitSelector.setObjectName("unitSelector")
        self.unitSelector.setFixedHeight(windowHeight/20)
        self.unitSelector.setStyleSheet(
            "padding-left: 3px;"
        )
        # self.unitSelector.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.updatedUnitSetting = []
        self.unitSelector.currentIndexChanged.connect(self.unitSettingsList)

        self.unitsWrapperLayout.addWidget(self.unitsLabel)
        self.unitsWrapperLayout.addWidget(self.unitSelector)
        self.unitsWrapperWidget.setFixedHeight((windowHeight/10)*1)
        self.unitsWrapperLayout.setSpacing(5)
        self.unitsWrapperLayout.setContentsMargins(0,0,0,0)
        self.unitsWrapperLayout.setAlignment(Qt.AlignVCenter)
        print(self.unitSelector.currentText())
        # UNITS OPTIONS END HERE

        # THEME OPTIONS
        self.themesWrapperWidget = QWidget()
        self.themesWrapperLayout = QVBoxLayout(self.themesWrapperWidget)

        self.themesLabel = QLabel("Themes")
        self.themesLabel.setFont(QFont('Gill Sans', 10))
        self.themesLabel.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        self.themeSelector = settingsComboBox()
        self.themeSelector.addItems(["MeteorLite", "Midnight Pink", "Blue Skies", "Acid Rain"])
        self.themeSelector.setObjectName("themeSelector")
        self.themeSelector.setFixedHeight(windowHeight/20)
        self.themeSelector.setStyleSheet(
            "padding-left: 3px;"
        )
        # self.themeSelector.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.updatedThemeSetting = []
        self.themeSelector.currentIndexChanged.connect(self.themeSettingsList)
        
        self.widgetButton = QPushButton("Save")
        self.widgetButton.clicked.connect(self.saveSettings)
        self.widgetButton.setObjectName("settingsSaveButton")
        self.widgetButton.setFixedHeight(windowHeight/20)
        
        self.themesWrapperLayout.addWidget(self.themesLabel)
        self.themesWrapperLayout.addWidget(self.themeSelector)
        self.themesWrapperLayout.addWidget(self.widgetButton)
        self.themesWrapperWidget.setFixedHeight((windowHeight/10)*1.5)
        self.themesWrapperLayout.setSpacing(5)
        self.themesWrapperLayout.setContentsMargins(0,0,0,0)
        self.themesWrapperLayout.setAlignment(Qt.AlignVCenter)
        

        # self.settingsLayout.addLayout(popupWindowWidgetsLayout)
        self.settingsLayout.addWidget(self.widgetsWrapperWidget)
        self.settingsLayout.addWidget(self.unitsWrapperWidget)
        self.settingsLayout.addWidget(self.themesWrapperWidget)
        
        self.settingsLayout.setSpacing(0)
        self.settingsLayout.setContentsMargins(3,5,3,5)
        

        savedSettings = [vars(settings)[item] for item in vars(settings)]

        for i in range(12): # This checks if the setting is saved as "active" and pre-checks the settings list to show the active status.
            if savedSettings[i][2] == 1:
                settingsNumber = savedSettings.index(savedSettings[i])
                item = self.widgetsList.item(settingsNumber)
                item.setSelected(True)
                self.widgetsListItems.append([item.text(), 1])
        
        for i in range(12,15): # This sets the dropdown list for the units, C, K, or F based on what's currently set.
            ref = [12,13,14]
            if savedSettings[i][2] == 1:
                settingsNumber = savedSettings.index(savedSettings[i])
                unitsNumber = ref.index(settingsNumber)
                self.unitSelector.setCurrentIndex(unitsNumber)

        for i in range(15,16): # This sets the theme drop down list to the saved theme.
            themesDict = {0:"MeteorLite", 1:"Midnight Pink", 2:"Blue Skies", 3:"Acid Rain"}
            themesWorkable = themesDict.values()
            tList = []
            for item in themesWorkable:
                tList.append(item)
            themesIndex = tList.index(savedSettings[15][2])
            self.themeSelector.setCurrentIndex((themesIndex))
            
    def workingWidgetList(self, item, t_f): # This is a custom event handler that limits the number of selected widgets to 5 to keep the layout clean.
        if t_f == True:
            if self.widgetsListItems == 5: # Can just change this number to increase limit.
                print("Limit Reached")
            else:
                self.widgetsListItems.append([item, 1])
                print(self.widgetsListItems)
        elif t_f == False:
            self.widgetsListItems.remove([item, 1])
            print(self.widgetsListItems)
    
    def unitSettingsList(self, row): # sets a class variable for the updated setting
        unitsDict = {0:"Celsius", 1:"Fahrenheit"}
        self.updatedUnitSetting = [unitsDict[row], 1]
        print(self.updatedUnitSetting)
    
    def themeSettingsList(self, row): # sets a class variable for the updated setting
        themesDict = {0:"MeteorLite", 1:"Midnight Pink", 2:"Blue Skies", 3:"Acid Rain"}
        self.updatedThemeSetting = ["Theme", themesDict[row]]

    def saveSettings(self): # This formats a list of settings selected, clears the current settings, and saves the new ones when the "saved" button is clicked.
        referenceList = [['Temperature', 0],['Humidity/Dewpoint', 0],['Wind', 0],['Precipitation', 0],['Visibility', 0],['Heat Index', 0],['Transport Wind', 0],['Snow/Ice', 0],['Ceiling/Mixing Height', 0],['Haines/Grassland Fire', 0],['20ft Windspeed/Direction', 0],['Lightning Activity', 0], ['Celsius', 0],['Fahrenheit', 0],['Kelvin', 0],['Theme', 'MeteorLite']]
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
        sql_settings_gui_insert(con, newSettings)# Now store this settings with the settings method, then refresh gui? Don't actually return this...
        settings = sql_settings_gui_get(con)
        self.settingsChangedSignal.emit(settings)
        
        
    def settingsPaletteChanged(self, object): # When settings changed signal fires, theme is changed here for the settingsTab.
        print("SETTINGSPALETTECHANGED")
        theme = themePalettes[object.currentTheme[2]] # Sets theme to correct theme name
        print(theme[0])
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(19,19,19)) # re-writes self.paletteW to new colors
        palette.setColor(QPalette.WindowText, theme[0]) # re-writes self.paletteW to new colors
        self.setPalette(palette) # re-writes self.paletteW to new colors
        self.update()

class MainWindow(QMainWindow):
    settingsObjectSignal = Signal(object)
    paletteChangeSignal = Signal(object)
    def __init__(self):
        super().__init__()
        self.settingsW = settings_startup() # makes a settings object for this window
        self.setWindowFlag(Qt.CustomizeWindowHint)
        self.setWindowFlags(Qt.Window |  Qt.WindowStaysOnTopHint | Qt.WindowSystemMenuHint) # These may need changed.
        self.setWindowTitle("MeteorLite")
        self.setGeometry(500, 500, 500, 500)
        self.setFixedSize(500, 500)
        self.setContentsMargins(0,0,0,0)
        

        self.settingsTab = SettingsWindow(self.settingsW, self.width(), self.height())
        self.settingsTab.setContentsMargins(3,3,3,3)
        self.settingsTab.settingsChangedSignal.connect(self.themeChange) # Fires off to the themeChange method to change the color of the tab.
        # self.settingsTab.settingsChangedSignal.connect(self.widgetsChange)
        self.settingsTab.widgetsLabel.setStyleSheet( # These just set the stylesheet to the saved theme.
            f"color: rgb{themePalettes[self.settingsW.currentTheme[2]][1]}"
        )
        self.settingsTab.settingsLabel.setStyleSheet(
            f"color: rgb{themePalettes[self.settingsW.currentTheme[2]][1]}"
        )
        self.settingsTab.unitsLabel.setStyleSheet(
            f"color: rgb{themePalettes[self.settingsW.currentTheme[2]][1]}"
        )
        self.settingsTab.themesLabel.setStyleSheet(
            f"color: rgb{themePalettes[self.settingsW.currentTheme[2]][1]}"
        )

        self.weatherTab = WeatherTab(self.width(), self.height()) # Sets dimensions and initializes main weather tab.
        self.weatherTab.MondayLabel.enterSignal.connect(self.enterLabel) # A set of signals that tell the enterLabel and leaveLabel methods where the cursor is.
        self.weatherTab.MondayLabel.leaveSignal.connect(self.leaveLabel)
        self.weatherTab.TuesdayLabel.enterSignal.connect(self.enterLabel)
        self.weatherTab.TuesdayLabel.leaveSignal.connect(self.leaveLabel)
        self.weatherTab.WednesdayLabel.enterSignal.connect(self.enterLabel)
        self.weatherTab.WednesdayLabel.leaveSignal.connect(self.leaveLabel)
        self.weatherTab.ThursdayLabel.enterSignal.connect(self.enterLabel)
        self.weatherTab.ThursdayLabel.leaveSignal.connect(self.leaveLabel)
        self.weatherTab.FridayLabel.enterSignal.connect(self.enterLabel)
        self.weatherTab.FridayLabel.leaveSignal.connect(self.leaveLabel)
        self.weatherTab.SaturdayLabel.enterSignal.connect(self.enterLabel)
        self.weatherTab.SaturdayLabel.leaveSignal.connect(self.leaveLabel)
        self.weatherTab.SundayLabel.enterSignal.connect(self.enterLabel)
        self.weatherTab.SundayLabel.leaveSignal.connect(self.leaveLabel)
        
        self.navigationTabs = QTabWidget() # This is the QTabWidget that all the widgets sit on.
        self.navigationTabs.setTabPosition(QTabWidget.North) # Specifies where the tabs are.
        self.navigationTabs.setContentsMargins(0,0,0,0)
        self.navigationTabs.setStyleSheet(
            "margin: 0px 0px 0px 0px;"
            "padding: 0px;"
        )

        self.navigationTabs.addTab(self.weatherTab, "Weather") # Adds these in order.
        self.navigationTabs.addTab(QWidget(), "Arduino")
        self.navigationTabs.addTab(QWidget(), "Data")
        self.navigationTabs.addTab(self.settingsTab, "Settings")


        self.day0Info = AnotherWindow(week_list[0], self.settingsW, self.weatherTab.weatherInfo1.width()) # These initialize each individual information widget. week_list is a reference that dictates what order the days are displayed.
        self.day1Info = AnotherWindow(week_list[1], self.settingsW, self.weatherTab.weatherInfo1.width())
        self.day2Info = AnotherWindow(week_list[2], self.settingsW, self.weatherTab.weatherInfo1.width())
        self.day3Info = AnotherWindow(week_list[3], self.settingsW, self.weatherTab.weatherInfo1.width())
        self.day4Info = AnotherWindow(week_list[4], self.settingsW, self.weatherTab.weatherInfo1.width())
        self.day5Info = AnotherWindow(week_list[5], self.settingsW, self.weatherTab.weatherInfo1.width())
        self.day6Info = AnotherWindow(week_list[6], self.settingsW, self.weatherTab.weatherInfo1.width())
        self.weatherTab.dayInfoStacked.addWidget(self.day0Info) # Boilerplate
        self.weatherTab.dayInfoStacked.addWidget(self.day1Info)
        self.weatherTab.dayInfoStacked.addWidget(self.day2Info)
        self.weatherTab.dayInfoStacked.addWidget(self.day3Info)
        self.weatherTab.dayInfoStacked.addWidget(self.day4Info)
        self.weatherTab.dayInfoStacked.addWidget(self.day5Info)
        self.weatherTab.dayInfoStacked.addWidget(self.day6Info)
        self.weatherTab.dayInfoStacked.setCurrentIndex(0)
        self.weatherTab.setStyleSheet(
            f"color: rgb{themePalettes[self.settingsW.currentTheme[2]][1]}"
        )

        self.settingsTab.widgetsList.widgetSignal.connect(self.widgetsChange) # The connector from the widgetSignal to the changer method.
        self.setCentralWidget(self.navigationTabs)

    def enterLabel(self, day): # Sets the widget order to include the day that's being moused over on top.
        if day != week_list[0]:
            stackedIndex = week_list.index(day)
            self.weatherTab.dayInfoStacked.setCurrentIndex(stackedIndex)
            # print(day)
            
            # self.w = self.weatherTab.tempLabels[day]
            # self.weatherTab.days7_horizontal.addWidget(self.w)

    def leaveLabel(self, day): # Returns to the current day when not moused over any other.
        if day != week_list[0]:
            self.weatherTab.dayInfoStacked.setCurrentIndex(0)
            # print(day)

    def themeChange(self, settings): # This is where most of the theme change signals meet. This changes the colors of the different parts of the GUI with the exception of the graphlabel, which has custom methods.
        print(themePalettes[settings.currentTheme[2]][1])
        
        self.weatherTab.setStyleSheet( # makes 
            f"color: rgb{themePalettes[settings.currentTheme[2]][1]}"
        )

        self.day0Info.currentPrecipGraph.graphPaletteChangeSignal.emit(QColor(200,50,200), settings) # Updates each of the graphs.
        self.day1Info.currentPrecipGraph.graphPaletteChangeSignal.emit(QColor(200,50,200), settings)
        self.day2Info.currentPrecipGraph.graphPaletteChangeSignal.emit(QColor(200,50,200), settings)
        self.day3Info.currentPrecipGraph.graphPaletteChangeSignal.emit(QColor(200,50,200), settings)
        self.day4Info.currentPrecipGraph.graphPaletteChangeSignal.emit(QColor(200,50,200), settings)
        self.day5Info.currentPrecipGraph.graphPaletteChangeSignal.emit(QColor(200,50,200), settings)
        self.day6Info.currentPrecipGraph.graphPaletteChangeSignal.emit(QColor(200,50,200), settings)

        self.settingsTab.widgetsLabel.setStyleSheet(
            f"color: rgb{themePalettes[settings.currentTheme[2]][1]}"
        )
        self.settingsTab.settingsLabel.setStyleSheet(
            f"color: rgb{themePalettes[settings.currentTheme[2]][1]}"
        )
        self.settingsTab.unitsLabel.setStyleSheet(
            f"color: rgb{themePalettes[settings.currentTheme[2]][1]}"
        )
        self.settingsTab.themesLabel.setStyleSheet(
            f"color: rgb{themePalettes[settings.currentTheme[2]][1]}"
        )

    def widgetsChange(self, widget, t_f): # The widgetSignal signal leads here. This takes the widget that's changed and hides/shows the widgets selected in real time.
        widgetsDict0 = {"Temperature": [self.day0Info.labelContainerTemps, self.day0Info.horz1], "Humidity/Dewpoint":[self.day0Info.humidityWidgetWrapper, self.day0Info.horz1], "Wind":[self.day0Info.windWidgetWrapper, self.day0Info.horz1], "Precipitation":[self.day0Info.precipitationWidgetWrapper, self.day0Info.horz3], "Visibility":[self.day0Info.visibilityWidgetWrapper, self.day0Info.horz1], "Heat Index":[self.day0Info.heatIndexWidgetWrapper, self.day0Info.horz2], "Transport Wind":[self.day0Info.transportWindWidgetWrapper, self.day0Info.horz2], "Snow/Ice":[self.day0Info.snowIceWidgetWrapper, self.day0Info.horz3], "Ceiling/Mixing Height":[self.day0Info.ceilingMixingWidgetWrapper, self.day0Info.horz2], "Haines/Grassland Fire":[self.day0Info.hainesWidgetWrapper, self.day0Info.horz2], "20ft Windspeed/Direction":[self.day0Info.ft20WidgetWrapper, self.day0Info.horz2], "Lightning Activity":[self.day0Info.lightningWidgetWrapper, self.day0Info.horz2]}
        widgetsDict1 = {"Temperature": [self.day1Info.labelContainerTemps, self.day1Info.horz1], "Humidity/Dewpoint":[self.day1Info.humidityWidgetWrapper, self.day1Info.horz1], "Wind":[self.day1Info.windWidgetWrapper, self.day1Info.horz1], "Precipitation":[self.day1Info.precipitationWidgetWrapper, self.day1Info.horz3], "Visibility":[self.day1Info.visibilityWidgetWrapper, self.day1Info.horz1], "Heat Index":[self.day1Info.heatIndexWidgetWrapper, self.day1Info.horz2], "Transport Wind":[self.day1Info.transportWindWidgetWrapper, self.day1Info.horz2], "Snow/Ice":[self.day1Info.snowIceWidgetWrapper, self.day1Info.horz3], "Ceiling/Mixing Height":[self.day1Info.ceilingMixingWidgetWrapper, self.day1Info.horz2], "Haines/Grassland Fire":[self.day1Info.hainesWidgetWrapper, self.day1Info.horz2], "20ft Windspeed/Direction":[self.day1Info.ft20WidgetWrapper, self.day1Info.horz2], "Lightning Activity":[self.day1Info.lightningWidgetWrapper, self.day1Info.horz2]}
        widgetsDict2 = {"Temperature": [self.day2Info.labelContainerTemps, self.day2Info.horz1], "Humidity/Dewpoint":[self.day2Info.humidityWidgetWrapper, self.day2Info.horz1], "Wind":[self.day2Info.windWidgetWrapper, self.day2Info.horz1], "Precipitation":[self.day2Info.precipitationWidgetWrapper, self.day2Info.horz3], "Visibility":[self.day2Info.visibilityWidgetWrapper, self.day2Info.horz1], "Heat Index":[self.day2Info.heatIndexWidgetWrapper, self.day2Info.horz2], "Transport Wind":[self.day2Info.transportWindWidgetWrapper, self.day2Info.horz2], "Snow/Ice":[self.day2Info.snowIceWidgetWrapper, self.day2Info.horz3], "Ceiling/Mixing Height":[self.day2Info.ceilingMixingWidgetWrapper, self.day2Info.horz2], "Haines/Grassland Fire":[self.day2Info.hainesWidgetWrapper, self.day2Info.horz2], "20ft Windspeed/Direction":[self.day2Info.ft20WidgetWrapper, self.day2Info.horz2], "Lightning Activity":[self.day2Info.lightningWidgetWrapper, self.day2Info.horz2]}
        widgetsDict3 = {"Temperature": [self.day3Info.labelContainerTemps, self.day3Info.horz1], "Humidity/Dewpoint":[self.day3Info.humidityWidgetWrapper, self.day3Info.horz1], "Wind":[self.day3Info.windWidgetWrapper, self.day3Info.horz1], "Precipitation":[self.day3Info.precipitationWidgetWrapper, self.day3Info.horz3], "Visibility":[self.day3Info.visibilityWidgetWrapper, self.day3Info.horz1], "Heat Index":[self.day3Info.heatIndexWidgetWrapper, self.day3Info.horz2], "Transport Wind":[self.day3Info.transportWindWidgetWrapper, self.day3Info.horz2], "Snow/Ice":[self.day3Info.snowIceWidgetWrapper, self.day3Info.horz3], "Ceiling/Mixing Height":[self.day3Info.ceilingMixingWidgetWrapper, self.day3Info.horz2], "Haines/Grassland Fire":[self.day3Info.hainesWidgetWrapper, self.day3Info.horz2], "20ft Windspeed/Direction":[self.day3Info.ft20WidgetWrapper, self.day3Info.horz2], "Lightning Activity":[self.day3Info.lightningWidgetWrapper, self.day3Info.horz2]}
        widgetsDict4 = {"Temperature": [self.day4Info.labelContainerTemps, self.day4Info.horz1], "Humidity/Dewpoint":[self.day4Info.humidityWidgetWrapper, self.day4Info.horz1], "Wind":[self.day4Info.windWidgetWrapper, self.day4Info.horz1], "Precipitation":[self.day4Info.precipitationWidgetWrapper, self.day4Info.horz3], "Visibility":[self.day4Info.visibilityWidgetWrapper, self.day4Info.horz1], "Heat Index":[self.day4Info.heatIndexWidgetWrapper, self.day4Info.horz2], "Transport Wind":[self.day4Info.transportWindWidgetWrapper, self.day4Info.horz2], "Snow/Ice":[self.day4Info.snowIceWidgetWrapper, self.day4Info.horz3], "Ceiling/Mixing Height":[self.day4Info.ceilingMixingWidgetWrapper, self.day4Info.horz2], "Haines/Grassland Fire":[self.day4Info.hainesWidgetWrapper, self.day4Info.horz2], "20ft Windspeed/Direction":[self.day4Info.ft20WidgetWrapper, self.day4Info.horz2], "Lightning Activity":[self.day4Info.lightningWidgetWrapper, self.day4Info.horz2]}
        widgetsDict5 = {"Temperature": [self.day5Info.labelContainerTemps, self.day5Info.horz1], "Humidity/Dewpoint":[self.day5Info.humidityWidgetWrapper, self.day5Info.horz1], "Wind":[self.day5Info.windWidgetWrapper, self.day5Info.horz1], "Precipitation":[self.day5Info.precipitationWidgetWrapper, self.day5Info.horz3], "Visibility":[self.day5Info.visibilityWidgetWrapper, self.day5Info.horz1], "Heat Index":[self.day5Info.heatIndexWidgetWrapper, self.day5Info.horz2], "Transport Wind":[self.day5Info.transportWindWidgetWrapper, self.day5Info.horz2], "Snow/Ice":[self.day5Info.snowIceWidgetWrapper, self.day5Info.horz3], "Ceiling/Mixing Height":[self.day5Info.ceilingMixingWidgetWrapper, self.day5Info.horz2], "Haines/Grassland Fire":[self.day5Info.hainesWidgetWrapper, self.day5Info.horz2], "20ft Windspeed/Direction":[self.day5Info.ft20WidgetWrapper, self.day5Info.horz2], "Lightning Activity":[self.day5Info.lightningWidgetWrapper, self.day5Info.horz2]}
        widgetsDict6 = {"Temperature": [self.day6Info.labelContainerTemps, self.day6Info.horz1], "Humidity/Dewpoint":[self.day6Info.humidityWidgetWrapper, self.day6Info.horz1], "Wind":[self.day6Info.windWidgetWrapper, self.day6Info.horz1], "Precipitation":[self.day6Info.precipitationWidgetWrapper, self.day6Info.horz3], "Visibility":[self.day6Info.visibilityWidgetWrapper, self.day6Info.horz1], "Heat Index":[self.day6Info.heatIndexWidgetWrapper, self.day6Info.horz2], "Transport Wind":[self.day6Info.transportWindWidgetWrapper, self.day6Info.horz2], "Snow/Ice":[self.day6Info.snowIceWidgetWrapper, self.day6Info.horz3], "Ceiling/Mixing Height":[self.day6Info.ceilingMixingWidgetWrapper, self.day6Info.horz2], "Haines/Grassland Fire":[self.day6Info.hainesWidgetWrapper, self.day6Info.horz2], "20ft Windspeed/Direction":[self.day6Info.ft20WidgetWrapper, self.day6Info.horz2], "Lightning Activity":[self.day6Info.lightningWidgetWrapper, self.day6Info.horz2]}
        if t_f == True:
            widgetsDict0[widget][1].addWidget(widgetsDict0[widget][0])
            widgetsDict1[widget][1].addWidget(widgetsDict1[widget][0])
            widgetsDict2[widget][1].addWidget(widgetsDict2[widget][0])
            widgetsDict3[widget][1].addWidget(widgetsDict3[widget][0])
            widgetsDict4[widget][1].addWidget(widgetsDict4[widget][0])
            widgetsDict5[widget][1].addWidget(widgetsDict5[widget][0])
            widgetsDict6[widget][1].addWidget(widgetsDict6[widget][0])
            widgetsDict0[widget][0].show()
            widgetsDict1[widget][0].show()
            widgetsDict2[widget][0].show()
            widgetsDict3[widget][0].show()
            widgetsDict4[widget][0].show()
            widgetsDict5[widget][0].show()
            widgetsDict6[widget][0].show()
        elif t_f == False:
            widgetsDict0[widget][0].hide()
            widgetsDict1[widget][0].hide()
            widgetsDict2[widget][0].hide()
            widgetsDict3[widget][0].hide()
            widgetsDict4[widget][0].hide()
            widgetsDict5[widget][0].hide()
            widgetsDict6[widget][0].hide()
        
        
        # for item in newSettingsList:
        #     widgetsDict[item[1]][1].addWidget(widgetsDict[item[1]][0])
        # self.day0Info.update()

    # def center(self): # This was here from when I was trying a custom frame design.
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
    #     print("moving...")

# Only need one per application
app = QApplication(sys.argv)

# Creating a new widget, which will be the window
w = MainWindow()
w.show() # Windows are hidden by default

with open("meteorlite.qss", "r") as f: # Stylesheet that functions like css. Not much on it currently, may use more in the future.
        _style = f.read()
        app.setStyleSheet(_style)

# Starts the event loop
app.exec()