import requests
import json
import sqlite3
from timeit import default_timer as timer
from datetime import datetime, timedelta

con = sqlite3.connect("meteorlite.db") # This just opens a connection to the db.

def functimer(func): # This is just a decorator function I can use to measure a function's runtime.
    def wrapper(*args, **kwargs):
        start = timer()
        obj = func(*args)
        end = timer()
        time_elapsed = end - start
        print(str(time_elapsed) + " - Time Elapsed")
        return obj
    return wrapper

def date_time_2(): # This function uses the datetime module to do arithmetic with dates. This function returns a lot of different things in order to be used as a catch all for date time arithmetic.
    weekday_map = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    time_now = datetime.now()
    year = time_now.year
    month = time_now.month
    if int(month) <= 9:
        month_revised = "0" + str(month)
    else:
        month_revised = month
    day = time_now.day
    if int(day) <= 9:
        day_revised = "0" + str(day)
    else:
        day_revised = day
    hour = time_now.hour
    if int(hour) <= 9:
        hour_revised = "0" + str(hour)
    else:
        hour_revised = hour
    minute = time_now.minute
    second = time_now.second
    date = (f"{year}-{month_revised}-{day_revised}")
    sql_formtted_date = (f"{year}/{month}/{day}")
    time = (f"{hour_revised}:{minute}:{second}")
    weekday = time_now.weekday()
    weekday_name = weekday_map[weekday]
    sql_new = datetime.strptime(sql_formtted_date, "%Y/%m/%d")
    sql_date = sql_new + timedelta(days=7) # This is a date used for retrieving a set number of days of data from the db. Adds 7 days from current day.
    sql_final_date = str(sql_date).split(" ")[0]
    
    return date, time, weekday_name, str(sql_final_date)

data_types = [ # 26 types of data given by the NOAA.
        'temperature',
        'dewpoint',
        'maxTemperature',
        'minTemperature',
        'relativeHumidity',
        'apparentTemperature',
        'heatIndex',
        'skyCover',
        'windDirection',
        'windSpeed',
        'windGust',
        'weather',
        'probabilityOfPrecipitation',
        'quantitativePrecipitation',
        'iceAccumulation',
        'snowfallAmount',
        'ceilingHeight',
        'visibility',
        'transportWindSpeed',
        'transportWindDirection',
        'mixingHeight',
        'hainesIndex',
        'lightningActivityLevel',
        'twentyFootWindSpeed',
        'twentyFootWindDirection',
        'grasslandFireDangerIndex'
    ]

 # This is the very first runtime task. Next step is to check if there's any information in the db.

def sql_table(con): # This creates a table for the user class information [REDUNDANT]
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE if not exists user(id integer PRIMARY KEY, name text, ipv4 text, latitude integer, longitude integer, gridX integer, gridY integer, office text, date text")
    con.commit()

def sql_insert(con, userData): # This inserts user data from the user class inititalization.
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO user(id, name, ipv4, latitude, longitude, gridX, gridY, office, date, time) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', userData)
    con.commit()

def sql_update(con): # This just edits the first IP in the user settings list
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE user SET ipv4 = "0.0.0.0" where id = 1')
    con.commit()

def sql_get(con): # Not used, just here from dev process
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * from user')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)

def sql_delete(con): # I believe this resets the IP list.
    cursorObj = con.cursor()
    cursorObj.execute('DELETE from user WHERE id = 2')
    con.commit()

def sql_get_last(con): # Returns the last IP address for the startup function.
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM user ORDER BY id DESC LIMIT 1')
    last = cursorObj.fetchone()
    return last

def sql_startup(con): # This creates a table for the user class information
    cursorObj = con.cursor()
    cursorObj.execute('create table if not exists user(id integer PRIMARY KEY, name text, ipv4 text, latitude integer, longitude integer, gridX integer, gridY integer, office text, date text, time text)')
    con.commit()

def sql_datadump(con, data_type, user_data): # Unused.
    cursorObj = con.cursor()
    cursorObj.execute(f'create table if not exists {data_type}(name text, unit text, date date, value integer)')
    con.commit()
    cursorObj.execute(f'INSERT INTO {data_type}(name, unit, date, value) VALUES(?, ?, ?, ?)', user_data)
    con.commit()

def sql_get_test(con, table): # A testing function from dev process.
    cursorObj = con.cursor()
    cursorObj.execute(f'SELECT * from {table}')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)

def sql_make_unformatted_tables(con): # This will be run on startup. Creates 26 tables, one for each data type. Creates time loss on very first time its run, after that it takes no time.
    cursorObj = con.cursor()
    for data_type in data_types:
        cursorObj.execute(f'create table if not exists {data_type}(validTime text, value text)')
        con.commit()
        
def sql_unformatted_test(con): # This is just another tester.
    cursorObj = con.cursor()
    cursorObj.execute(f'SELECT * from temperature')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)

def sql_unformatted_by_date(con, dtype): # This will be the function used to get data for x days for one data type.
    date, time, weekday, sql_time = date_time_2()
    cursorObj = con.cursor()
    cursorObj.execute(f"SELECT * from {dtype} Where validTime BETWEEN '{date}' AND '{sql_time}'") # Don't change these days
    rows = cursorObj.fetchall()
    rowList = [row for row in rows]
    return rowList

def sql_unformatted_add_test(con, weather_data): # This function will add in all the data from the user.get_weather_data() method.
    cursorObj = con.cursor()
    for data_type in data_types:
        for i in range(len(weather_data['properties'][data_type]['values'])):
            data_point = [str(weather_data['properties'][data_type]['values'][i]['validTime']), str(weather_data['properties'][data_type]['values'][i]['value'])]  
            cursorObj.execute(f'INSERT INTO {data_type}(validTime, value) VALUES(?, ?)', data_point)
    con.commit()

def sql_unformatted_delete(con): # Just allows easier testing on the db.
    for data_type in data_types:
        cursorObj = con.cursor()
        cursorObj.execute(f'DELETE from {data_type}')
    con.commit()

def sql_unformatted_drop_table(con): # Just allows easier testing on the db.
    for data_type in data_types:
        cursorObj = con.cursor()
        cursorObj.execute(f'DROP TABLE {data_type};')
    con.commit()
    # cursorObj = con.cursor()
    # cursorObj.execute('create table if not exists data(id integer PRIMARY KEY, date text, 01 text,latitude integer, longitude integer, gridX integer, gridY integer, office text, date text, time text)')

class Settings(): # This is the settings class. This will be initialized and used as a running list of settings each startup. Will be updated.
    def __init__(self, temperature, humid_dewpt, wind, precip, visibility, apparentTemp_heatIndx, transport, snow, ceilingMixing, fire, ft20, lightning, celsius, fahrenheit, kelvin, theme):
        self.temperature = temperature
        self.humid_dewpt = humid_dewpt
        self.wind = wind
        self.precip = precip
        self.visibility = visibility
        self.apparentTemp_heatIndx = apparentTemp_heatIndx
        self.transport = transport
        self.snow = snow
        self.ceilingMixing = ceilingMixing
        self.fire = fire
        self.ft20 = ft20
        self.lightning = lightning
        self.celsius = celsius
        self.fahrenheit = fahrenheit
        self.kelvin = kelvin
        self.currentTheme = theme

def convertSettingsToWidgets(values): # This is a one off function that selects "active" widgets from all settings and puts them in a list.
    print(values)
    vList = []
    for item in values:
        vList.append(item)

    newList = []
    for i in range(12):
        print("Test")
        if vList[i][2] == 1:
            print("appended")
            newList.append(vList[i])
    return newList

def sql_settings_make_table(con):  # Run on startup of program to ensure there's a table. This is where settings are stored in db.
    startup_settings_list = [['Temperature', 1],['Humidity/Dewpoint', 1],['Heat Index', 0],['Wind', 1],['Precipitation', 1],['Visibility', 1],['Transport Wind', 0],['Snow/Ice', 0],['Ceiling/Mixing Height', 0],['Haines/Grassland Fire', 0],['20ft Windspeed/Direction', 0],['Lightning Activity', 0], ['Celsius', 1],['Fahrenheit', 0],['Kelvin', 0],['Theme', 'MeteorLite']]
    # 16 total settings items, first 12 are widget cards, next 3 are units, last is current theme.
    cursorObj = con.cursor()
    cursorObj.execute(f'create table if not exists settings(id integer PRIMARY KEY, name text, value int)')
    con.commit()
    cursorObj.execute("SELECT * from settings")
    rows = cursorObj.fetchall()
    rowList = [row for row in rows]
    if rowList == []:
        for item in startup_settings_list:
            cursorObj.execute(f'INSERT INTO settings(name, value) VALUES(?, ?)', item)
    con.commit()

def sql_settings_gui_insert(con, settings_obj): # Feed the settings class into this thing. This is called to save current settings.
    settings_attr = vars(settings_obj)
    cursorObj = con.cursor()
    cursorObj.execute(f'DELETE from settings')
    print(settings_attr)
    for item in settings_attr:
        print(settings_attr[item])
        settings_itemized = [settings_attr[item][0], settings_attr[item][1]]
        cursorObj.execute(f'INSERT INTO settings(name, value) VALUES(?, ?)', settings_itemized)
    con.commit()

def sql_settings_gui_get(con): # This inits the settings object when called.
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * from settings")
    rows = cursorObj.fetchall()
    rowList = [row for row in rows]
    
    settingsObj = Settings(rowList[0],rowList[1],rowList[2],rowList[3],rowList[4],rowList[5],rowList[6],rowList[7],rowList[8],rowList[9],rowList[10],rowList[11],rowList[12],rowList[13],rowList[14],rowList[15])
    return settingsObj

# This is the user class. Functionality of the app will be based off of information stored in this class. A single user is defined, 
# the name and ip are taken and stored. This class will contain the methods used to obtain the coordinates associated with the user's ip.
# This will auto update on startup, possibly upon moving, although that is only if there is funding for the app and associated services needed.
# A refresh button will be added. Name may be stored between sessions, ip address is as well to limit the use of the ip website.
class User:
    def __init__(self, identity, name, ip, latitude, longitude, gridX, gridY, office, date, time):
        self.identity = identity
        self.name = name
        self.IPv4 = ip
        self.latitude = latitude
        self.longitude = longitude
        self.gridX = gridX
        self.gridY = gridY
        self.office = office
        self.date = date
        self.time = time

    @functimer
    def get_weather_data(self):
        forecast = requests.get(f"https://api.weather.gov/gridpoints/{self.office}/{int(self.gridX)},{int(self.gridY)}")
        forecast_reader_info = json_converter(forecast.text)
        return forecast_reader_info

def json_converter(content): # This converts the json given from the NOAA API into a Python usable format.
    info = json.loads(content)
    print("json converted")
    return info

def get_ip(): # Can be requested as much as needed. This grabs the users current IPv4 address.
    ipv4 = requests.get('https://api.ipify.org').content.decode('utf8')
    return ipv4
    
def get_ip_coords(): # Very limited requests. This will run only if the current IP does not match the one stored in settings. It grabs your geo-coordinates (lat an lon). Returns coords.
    ip = get_ip()
    location_data = requests.get(f"http://api.ipstack.com/{ip}?access_key=0b85fa09f8ce75a20932950f1f3a25e6")
    print(f"converting {ip} into coordinates")
    user_coordinate_dictionary = json_converter(location_data.text)
    full_latitude = user_coordinate_dictionary["latitude"]
    full_longitude = user_coordinate_dictionary["longitude"]
    latitude = str(full_latitude)
    longitude = str(full_longitude)
    latitude = latitude[0:9]
    longitude = longitude[0:9]
    latitude = float(latitude)
    longitude = float(longitude)
    print(longitude)
    ip_coords = [ip, latitude, longitude]
    return ip_coords
 
def get_ip_coords_points(): # Request as much as needed. Does a GET request for your gridpoints based off your coordinates. Just identifies what grid point you're on.
    ip_coords = get_ip_coords()
    points_request = requests.get(f"https://api.weather.gov/points/{ip_coords[1]},{ip_coords[2]}")
    points_python = json_converter(points_request.text)
    gridX = points_python["properties"]["gridX"]
    gridY = points_python["properties"]["gridY"]
    office = points_python["properties"]["cwa"]
    print(gridX, gridY, office)
    ip_coords_points= [str(ip_coords[0]), ip_coords[1], ip_coords[2], gridX, gridY, office]
    return ip_coords_points # This builds a list of user settings.

def user_startup(): # Startup will check
    con = sqlite3.connect("meteorlite.db") # This is the very first runtime task. Next step is to check if there's any information in the db.
    sql_startup(con) # This function makes a table only if it does not already exist.
    if sql_get_last(con) == None:
        print("if") # If no db entry exists, then no user object data exists. That data and user object is initialized and saved to db.
        ip, latitude, longitude, gridX, gridY, office = get_ip_coords_points()
        name = "user" # Can be changed later to add multi user functionality.
        date, time, weekday, sql_time = date_time_2()
        user_values = (1, name, ip, latitude, longitude, gridX, gridY, office, date, time)
        sql_insert(con, user_values)
        user_values = sql_get_last(con)
        print(user_values)
        user = User(user_values[0],user_values[1],user_values[2],user_values[3],user_values[4],user_values[5],user_values[6],user_values[7], user_values[8], user_values[9])
        return user # ultimately all of these outcomes result in a db entry on a user object returned.
    else: # If there is a previous db entry, it must be checked against current IP to ensure the user is still in the same geo-location.
        print("else")
        current_ip = get_ip()
        date, time, weekday, sql_time = date_time_2()
        # print(user.get_weather_data()) this is here for diagnostic purposes
        if date != user_values[8]: # if current date is not equal to db listed date, make a new entry with updated date.
            print("if date != user_values[8]:")
            next_id = user_values[0] + 1 # Since this is a new date, we need to denote a new access for forecast data. Id needs to be updated since a unique entry will be made.
            new_date_entry = (next_id,user_values[1],user_values[2],user_values[3],user_values[4],user_values[5],user_values[6],user_values[7], date, time)
            sql_insert(con, new_date_entry)
            return user
        # print("made it")
        # return user
        else: # If current ip is not last db entry ip, make a new entry.
            print("# If current ip is not last db entry ip, make a new entry.")
            ip, latitude, longitude, gridX, gridY, office = get_ip_coords_points()
            name = "user"
            date, time, weekday, sql_time = date_time_2()
            next_id = user_values[0] + 1
            user_values = (next_id, name, ip, latitude, longitude, gridX, gridY, office, date, time)
            sql_insert(con, user_values) # Since the ip in the last db entry has changed, the user object info all has to change too.
            return user
            # calling the get_ip_coords_points(), name, date_time allows for a profile to be created for each location in the db, allowing for later
            # analysis based on location most frequented and such.
    con.close()

def settings_startup(): # Makes sure tables exist, then tries to grab information from them.
    sql_settings_make_table(con)
    return sql_settings_gui_get(con)

def data_pull(user_weather_data): # Inits db if not already exists, grabs and stores weather info, then returns 2 bits of info.
    weather_data = user_weather_data()
    print(weather_data)
    sql_make_unformatted_tables(con) # This is the creation function for the raw data tables.
    sql_unformatted_add_test(con, weather_data) # This function intakes the weather data and stores it all.
    start_time = weather_data['properties']['validTimes'][11:13] # The dataset start time is often before the current hour so this needs to be specified.
    update_time = weather_data['properties']['updateTime'] # This is the time the data updates, so this is the time the program needs to do another request.
    return start_time, update_time


# the extend_hours function was by far the most complicated algorithm I've written to date. This function will take all the data points
# for a 24 hour period and check for several different types of extensions listed. If a point is the same for several hours, this
# function will create new points for those hours to create 24 hour dictionaries with a point for each hour.
@functimer
def extend_hours(obj): #obj is a dict with 7 days worth of datapoints, separated by numbers (as the keys) starting from 0, ending in 6.
    print("extend_hours")
    print(obj)
    dict_7_days = {} # This initializes what will be the final dictionary containing 7 dictionaries each with 24 datapoints (or close)
    dict_1_day = {} 
    day_counter = 0 # This will set the current key the data points are being saved to. It's a counter.
    sample = [i for i in range(8)]

    for i in sample:
        dict_7_days[str(i)] = dict_1_day.copy()

    for dataSet in obj: # since this function intakes 7 days worth of data, it needs to process each one separately. This for loop begins.
        if day_counter == 7: # This just cuts off at 7 in case more accidentally gets through.
            return dict_7_days
        working_datapoint_set = obj[dataSet] 
        print(str(working_datapoint_set) + "WORKING_DATAPOINT_SET")
        first_hour = int(obj[dataSet][0][2][11:13]) # Day -> First datapoint -> date_time -> hour 
        print(str(first_hour) + "FIRST_HOUR")

        for point in working_datapoint_set: # ['probabilityOfPrecipitation', '%', '2023-02-02T12:00:00+00:00/PT12H', '7'] - for reference
            # if int(point[2].split("T")[2][0:-1])-1
            print(str(point)+"POINT")
            current_hour = int(point[2][11:13])
            print(str(current_hour) + "CURRENT_HOUR")
            try: # This try except block is actually to make it easier to identify the type of extension we're working with.
                extension_hours = int(point[2].split("PT")[1][0:-1])-1 # This just splits the "PT12H" section of the point. If it fails that means there's a D at the start, indicating whole day extensions.
                print(str(extension_hours)+"EXTENSION_HOURS")
            except IndexError: # This is tripped if there's a day extension in there.
                print("Has Day")
                extension_hours = -1
                try:
                    breakdown = point[2].split("P")[1].split("T") # This is another try except that identifies if it has only day extensions, or day + hour extensions.
                    days = int(breakdown[0][:-1]) # Goes to an algorithm.
                    print(days)
                    hours = int(breakdown[1][:-1])-1 # Waits until days are done and then goes into reg algo.
                    print(hours)
                    hours_total = (days * 24) + hours  # This essentially breaks down the days and hour extensions into a total hour count.
                    print(hours_total)
                    hours_left_of_current_day = 23 - current_hour # Gets hours left of current day to start.
                    print(hours_left_of_current_day)
                    working_point = point.copy()
                    working_point_date_time = working_point[2] # Grabs the current points hour.
                    if current_hour <= 9: # These are repeat, but they are used for dictionary key consistency.
                        new_hour = "0" + str(current_hour)
                    elif current_hour == 0:
                        new_hour = "00"
                    elif current_hour > 9:
                        new_hour = current_hour
                    dict_7_days[str(day_counter)][str(new_hour)] = working_point # add current point to sub dictionary (cant forget)
                    if hours_left_of_current_day != 0: # This takes care of what's left of the current day
                        print("FINISHING DAY")
                        old_hour = int(working_point_date_time[11:13])
                        print(hours_left_of_current_day)
                        for i in range(1, hours_left_of_current_day+1):                    
                            new_hour = old_hour + i
                            if new_hour <= 9: 
                                new_hour = "0" + str(new_hour)
                            elif new_hour == 0:
                                new_hour = "00"
                            elif new_hour > 9:
                                new_hour = str(new_hour)
                            build_point = working_point_date_time[0:11] + new_hour + working_point_date_time[13:26] + "P" +  "T" + str(hours_total) + "H"
                            print(build_point)
                            dict_7_days[str(day_counter)][new_hour] = [working_point[0], working_point[1], build_point, working_point[3]]
                            hours_total -= 1
                        day_counter += 1
                        
                    elif hours_left_of_current_day == 0:
                        day_counter += 1
                    
                    print(str(day_counter)+"DAYCOUNTER")
                    day_change = 1
                    while hours_total != 0:
                        print("while")
                        print(str(day_counter)+"DAYCOUNTER")
                        new_day = int(working_point_date_time[8:10]) + day_change
                        if new_day <= 9: 
                            new_day2 = "0" + str(new_day)
                        elif new_day == 0:
                            new_day2 = "00"
                        elif new_day > 9:
                            new_day2 = str(new_day)
                        print(str(new_day2)+"NEWDAY")
                        if hours_total >= 23:
                            print("if")
                            new_day = int(working_point_date_time[8:10]) + day_change
                            
                            for i in range(24):
                                new_hour = 0 + i
                                print(new_hour)
                                if new_hour <= 9: 
                                    new_hour2 = "0" + str(new_hour)
                                elif new_hour == 0:
                                    new_hour2 = "00"
                                elif new_hour > 9:
                                    new_hour2 = str(new_hour)
                                print(new_hour2)
                                
                                build_point = working_point_date_time[0:8] + new_day2 + "T" + new_hour2 + working_point_date_time[13:26] + "P" + "T" + str(hours_total) + "H"
                                dict_7_days[str(day_counter)][new_hour2] = [working_point[0], working_point[1], build_point, working_point[3]]
                                hours_total -= 1
                            day_change += 1
                            day_counter += 1
                            print(str(day_change) + "DAYCHANGE")
                            
                        elif hours_total < 23:
                            print("elif")
                            print(hours_total)
                            for i in range(hours_total):
                                new_hour = 0 + i
                                if new_hour <= 9: 
                                    new_hour2 = "0" + str(new_hour)
                                elif new_hour == 0:
                                    new_hour2 = "00"
                                elif new_hour > 9:
                                    new_hour2 = str(new_hour)
                                build_point = working_point_date_time[0:8] + new_day2 + "T" + new_hour2 + working_point_date_time[13:26] + "P" + "T" + str(hours_total) + "H"
                                dict_7_days[str(day_counter)][new_hour2] = [working_point[0], working_point[1], build_point, working_point[3]]
                                hours_total -= 1
  
                except IndexError: # This catches if there's only day extensions. Uses the same process as the others.
                    print("JustDay")
                    try:
                        breakdown = point[2].split("P")[1]
                        days = int(breakdown[0:-1])
                        print(days)
                        hours_total = (days * 24) - 1
                        hours_left_of_current_day = 23 - current_hour
                        working_point = point.copy()
                        working_point_date_time = working_point[2]
                        if current_hour <= 9:
                            new_hour = "0" + str(current_hour)
                        elif current_hour == 0:
                            new_hour = "00"
                        elif current_hour > 9:
                            new_hour = current_hour
                        dict_7_days[str(day_counter)][str(new_hour)] = working_point # add current point to list (cant forget)
                        if hours_left_of_current_day != 0: # This takes care of what's left of the current day
                            print("FINISHING DAY")
                            old_hour = int(working_point_date_time[11:13])
                            for i in range(1, hours_left_of_current_day+1):
                                new_hour = old_hour + i
                                if new_hour <= 9: 
                                    new_hour = "0" + str(new_hour)
                                elif new_hour == 0:
                                    new_hour = "00"
                                elif new_hour > 9:
                                    new_hour = str(new_hour)
                                build_point = working_point_date_time[0:11] + new_hour + working_point_date_time[13:26] + "P" +  "T" + str(hours_total) + "H"
                                dict_7_days[str(day_counter)][new_hour] = [working_point[0], working_point[1], build_point, working_point[3]]
                                hours_total -= 1
                            day_counter += 1

                        elif hours_left_of_current_day == 0:
                            day_counter += 1
                        
                        print(str(day_counter)+"DAYCOUNTER")
                        day_change = 1
                        while hours_total != 0:
                            print("while")
                            print(str(day_counter)+"DAYCOUNTER")
                            print(str(hours_total) + "HOURS TOTAL HOLY GOD WHY")
                            new_day = int(working_point_date_time[8:10]) + day_change
                            if new_day <= 9: 
                                new_day2 = "0" + str(new_day)
                            elif new_day == 0:
                                new_day2 = "00"
                            elif new_day > 9:
                                new_day2 = str(new_day)
                            print(str(new_day2)+"NEWDAY")
                            if hours_total >= 23:
                                print("if")
                                new_day = int(working_point_date_time[8:10]) + day_change

                                for i in range(24):
                                    new_hour = 0 + i
                                    print(new_hour)
                                    if new_hour <= 9: 
                                        new_hour2 = "0" + str(new_hour)
                                    elif new_hour == 0:
                                        new_hour2 = "00"
                                    elif new_hour > 9:
                                        new_hour2 = str(new_hour)
                                    print(str(new_hour2) + "NEWHOUR")

                                    build_point = working_point_date_time[0:8] + new_day2 + "T" + new_hour2 + working_point_date_time[13:26] + "P" + "T" + str(hours_total) + "H"
                                    dict_7_days[str(day_counter)][new_hour2] = [working_point[0], working_point[1], build_point, working_point[3]]
                                    hours_total -= 1
                                
                                day_change += 1
                                print(str(day_change) + "DAYCHANGE")
                                day_counter += 1
                                

                            elif hours_total < 23:
                                print("elif")
                                for i in range(hours_total):
                                    new_hour = 0 + i
                                    if new_hour <= 9: 
                                        new_hour2 = "0" + str(new_hour)
                                    elif new_hour == 0:
                                        new_hour2 = "00"
                                    elif new_hour > 9:
                                        new_hour2 = str(new_hour)
                                    build_point = working_point_date_time[0:8] + new_day2 + "T" + new_hour2 + working_point_date_time[13:26] + "P" + "T" + str(hours_total) + "H"
                                    dict_7_days[str(day_counter)][new_hour2] = [working_point[0], working_point[1], build_point, working_point[3]]
                                    hours_total -= 1
                                
                    except IndexError:
                        print("Error handling goes here")
            
            if extension_hours > 0 and (current_hour + extension_hours) <= 23: # This function catches points with only hour extensions.
                print("if")
                
                working_point = point.copy()
                working_point_date_time = working_point[2]
                print(str(working_point_date_time) + "WORKING_POINT_DATE_TIME")
                if current_hour <= 9:
                    new_hour = "0" + str(current_hour)
                elif current_hour == 0:
                    new_hour = "00"
                elif current_hour > 9:
                    new_hour = current_hour
                dict_7_days[str(day_counter)][str(new_hour)] = working_point
                for i in range(1, extension_hours + 1):
                    # We have to take the working point and build a new one using parts, and use i to change the deets. + 1 hour, -1 extn hour. 
                    # Will just add each larger i to a copy of the base point hour.
                    old_hour = int(working_point_date_time[11:13])
                    if old_hour + i <= 9:
                        new_hour = "0" + str(old_hour + i) # Will just add each larger i to a copy of the base point hour.
                    elif old_hour + i == 0:
                        new_hour = "00"
                    else:
                        new_hour = str(old_hour + i) # Will just add each larger i to a copy of the base point hour.
                    
                    new_extension_count = int(working_point_date_time.split("T")[2][0:-1])-i # This is the PT##H at the end. Splits and takes after the T [-1]. Subtracts i.
                    build_point = working_point_date_time[0:11] + str(new_hour) + working_point_date_time[13:26] + "PT" + str(new_extension_count) + "H"
                    print(build_point + "BUILD POINT")
                    dict_7_days[str(day_counter)][str(new_hour)] = [working_point[0], working_point[1], build_point, working_point[3]] #appends to dict.
                    
                if str(dict_7_days[str(day_counter)][str(new_hour)][2][11:13]) == len(working_datapoint_set):
                    day_counter += 1
                    continue

                if str(dict_7_days[str(day_counter)][str(new_hour)][2][11:13]) == str(23):
                    print("TESTER")
                    item = [item for item in dict_7_days['6']]
                    print(str(item) + "ITEM")
                    day_counter += 1
                    continue
                
            elif extension_hours > 0 and (current_hour + extension_hours) > 23:# This function catches points with only hour extensions.
                print("elif")
                hours_to_carry_over = extension_hours - (23 - current_hour)# This grabs the extra off the end of the hours to use for the next days set.
                print(hours_to_carry_over)
                extension_hours_trimmed = extension_hours - hours_to_carry_over
                print(extension_hours_trimmed)
                working_point = point.copy()
                print(working_point)
                working_point_date_time = working_point[2]
                dict_7_days[str(day_counter)][str(current_hour)] = working_point
                for i in range(1, extension_hours_trimmed + 1):
                    print(i)
                    print("for i")
                    old_hour = int(working_point_date_time[11:13])
                    if old_hour < 10:
                        new_hour = "0" + str(old_hour + i) # Will just add each larger i to a copy of the base point hour.
                    else:
                        new_hour = str(old_hour + i) # Will just add each larger i to a copy of the base point hour.
                    print(new_hour)
                    new_extension_count = int(working_point_date_time.split("T")[2][0:-1])-i # This is the PT##H at the end. Splits and takes after the T [-1]. Subtracts i.
                    build_point = working_point_date_time[0:11] + str(new_hour) + working_point_date_time[13:26] + "PT" + str(new_extension_count) + "H"
                    dict_7_days[str(day_counter)][str(new_hour)] = [working_point[0], working_point[1], build_point, working_point[3]]
                    print(build_point)
                day_counter += 1
                
                working_point_next_day_base = working_point.copy() # Need to change the date now and reset time to 00:00, set ## in PT##H to hours_to_carry_over
                old_date = int(working_point_next_day_base[2][8:10])
                if old_date < 10:
                    new_date = "0" + str(old_date + 1)
                else:
                    new_date = str(old_date + 1)

                working_point_next_day = [working_point_next_day_base[0], working_point_next_day_base[1], (working_point_next_day_base[2][0:8] + new_date + "T" + "00" + working_point_next_day_base[2][13:26] + "PT" + str(hours_to_carry_over) + "H"), working_point_next_day_base[3]]
                working_point_next_day_date_time = working_point_next_day[2]
                print(working_point_next_day_date_time)
                print(day_counter)
                
                dict_7_days[str(day_counter)][str("00")] = working_point_next_day
                for i in range(hours_to_carry_over-1):
                    print("for i carry over")
                    old_hour = 0
                    if old_hour < 10:
                        new_hour_int = old_hour + i + 1
                        new_hour2 = "0" + str(new_hour_int)# Will just add each larger i to a copy of the base point hour.
                    elif old_hour == 0:
                        new_hour2 = "00"
                    else:
                        new_hour2 = str(old_hour + i)
                    print(new_hour2)
                    new_extension_count = int(working_point_next_day_date_time.split("T")[2][0:-1])-1-i # This is the PT##H at the end. Splits and takes after the T [-1]. Subtracts i.
                    build_point = working_point_next_day_date_time[0:8] + new_date + "T" + str(new_hour2) + working_point_next_day_date_time[13:26] + "PT" + str(new_extension_count) + "H"
                    print(build_point)
                    dict_7_days[str(day_counter)][str(new_hour2)] = [working_point_next_day[0], working_point_next_day[1], build_point, working_point_next_day[3]]
                
            elif str(point[2][11:13]) == str(23):# This function catches points with only hour extensions. Has to be included to account for the point at hour 23.
                dict_7_days[str(day_counter)][str(current_hour)] = point.copy()
                day_counter += 1
                print("POINT ON 23")

            elif extension_hours == 0: # Catches if there's no extension hours and formats the point properly into the sub dict.
                if current_hour <= 9:
                    print("SPECIF")
                    new_hour = ("0" + str(current_hour))# Will just add each larger i to a copy of the base point hour.
                    dict_7_days[str(day_counter)][str(new_hour)] = point.copy()
                    
                elif current_hour >= 10:
                    print("SPECELSE")
                    new_hour = str(current_hour)
                    dict_7_days[str(day_counter)][str(new_hour)] = point.copy()
                    
                elif current_hour == 0:
                    
                    continue
                print("ADDING POINT")
                print("else")
    return dict_7_days

def cut_data(trimmed_datas, day): # This is unused but is here for manual time zone adjustment.
    reversedObj = trimmed_datas[::-1]
    
    keptList = []
    for i in range(len(reversedObj)):
        print("DAY" + str(day))
        print(reversedObj[i][0][8:10])
        print(type(day))
        print(type(reversedObj[i][0][8:10]))
        if int(reversedObj[i][0][8:10]) == day:
            print("if")
            keptList.append(reversedObj[i])
            print(keptList)
            if (int(reversedObj[i][0][8:10]) + int(reversedObj[i][0][11:13])) == (int(reversedObj[i+1][0][8:10]) + int(reversedObj[i+1][0][11:13])):
                return keptList
            elif int(reversedObj[i][0][11:13]) > int(reversedObj[i+1][0][11:13]):
                return keptList
                     
def trim_dataset(obj, starterDay, zoneDifference): # This trims the dataset down to all but the last 7 day period.
    newList = []
    newList.clear()
    reversedObj = obj[::-1] # This is the reversed total list of datapoints for the 7 day period. It's reversed in order to work back to a point.

    for i in range(len(reversedObj)):
        if int(reversedObj[i][0][8:10]) == starterDay: # This If-Else adds each data point to the newList variable until it reaches the last datapoint with the same day as the first day of the 7-day period.
            newList.append(reversedObj[i]) # Adds that first point.
            try:
                if reversedObj[i][0][8:10] != reversedObj[i+1][0][8:10]: # This then checks each current point against the subsequent point to determine if they have the same day.
                    refBreakdown = reversedObj[i][0].split("T")
                    refDate = refBreakdown[0].split("-") # refDate is a list of the numbers involved in the date
                    refTime = refBreakdown[1].split(":") # refTime is a list of the numbers involved in the time
                    refDateTime = datetime(int(refDate[0]), int(refDate[1]), int(refDate[2]), int(refTime[0]), int(refTime[1]), 0, 0) # For each point this makes (year, month, day, hour, minute)
                    dateTimeAdjusted = refDateTime + timedelta(hours = -zoneDifference) # makes a dateTime object and adds timezone difference onto it in case the timezone needs to be manually accounted for.
                    for x in range(zoneDifference): # This just adds
                        breakdown = reversedObj[i+x][0].split("T")
                        date = breakdown[0].split("-")
                        time = breakdown[1].split(":")
                        dateTime = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), 0, 0) # Makes date + hour object for each new point examined for the zoneDifference.
                        if dateTime < dateTimeAdjusted: # Adds each point for the zoneDifference as long as the date for the point isn't earlier than the time zone difference calculated with dateTimeAdjusted.
                            return newList[::-1]
                        else:
                            newList.append(reversedObj[i+x])
                  
            except IndexError:
                print("IndexError")
                # print(newList[::-1])
                return newList[::-1]
        else:
            newList.append(reversedObj[i])

def adjust_time_zone(obj, adjustment): # This function is not used currently, and exists as a backup in case time zone needs to be accounted for.
    masterList = [obj[item][item2] for item in obj for item2 in obj[item]] # This comprehension is just a list of each individual datapoint contained in the dictionary of (24hr) dictionaries in order
    newDict = {}
    newDict.clear()
    for i in range(adjustment): # This deletes the datapoints that occur before the target time.
        del masterList[0]
    # need a solid function to determine the number of hours left in the current day.
    refHour = int(masterList[0][2][11:13])
    hoursLeft = 23 - refHour
    newDict["0"] = {masterList[i][2][11:13]:masterList[i]for i in range(hoursLeft + 6 + 1)}
    # finish the remaining 24 hour periods
    # print(newDict['0'])
    setNumber = 1
    currentIter = int(len(newDict["0"]))
    position = len(masterList) - currentIter + 1
    print(position)
    while currentIter < (position + 6):
        try:
            print("try")
            newDict[str(setNumber)] =  {masterList[i + currentIter][2][11:13]:masterList[i + currentIter] for i in range(24)}
            setNumber += 1
            currentIter += 24 
        except:
            print("EXCEPT")
            newDict[str(setNumber)] = {masterList[i + currentIter][2][11:13]:masterList[i + currentIter] for i in range(abs(currentIter - len(masterList)))}
            position = 0
            
    return newDict
         
def data_list(user_weather_data, data_type, data_unit): # returns the lists of value pairs for each data type ( a list with lists[[datetime, value],[datetime,value]])
    print(user_weather_data)
    data_pre_sort = [[data_type, data_unit, user_weather_data[i][0], str(user_weather_data[i][1])[0:4]] for i in range(int(len(user_weather_data)))]
    return data_pre_sort

# This algorithm works by comparing the current point to the next and finding where the days no longer match. Works in linear big O.
def sort_24(obj): # This is here to split the week long data sets into days for further processing in extend_hours()
    x = 0
    placeholderList = []
    daysDict = {}
    for i in range(len(obj)):
        try:
            if obj[i][2][8:10] == obj[i+1][2][8:10]: # If the dates are the same, add the x to the beginning of a 3 part [date,value,unit] list.
                placeholderList.append([obj[i][0], obj[i][1], obj[i][2], obj[i][3]])
            elif obj[i][2][8:10] != obj[i+1][2][8:10]:
                placeholderList.append([obj[i][0], obj[i][1], obj[i][2], obj[i][3]]) # each element gets appended to the empty list until you
                daysDict[str(x)] = [elt for elt in placeholderList] # have all the elements of a single day, which the list gets added to a dict keyed for that day
                placeholderList.clear() # list is cleared to start again.
                x += 1
        except IndexError:
            placeholderList.append([obj[i][0], obj[i][1], obj[i][2], obj[i][3]]) # each element gets appended to the empty list until you
            daysDict[str(x)] = [elt for elt in placeholderList]
    return daysDict # This will return a dictionary coded from 0:6 that will store all of the individual days of data for a data type.

def sort_week_from_today(): # This just finds the current day and arranges a list in order of days after.
    date, time, weekday, sql_time = date_time_2()
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    weekday_num = weekdays.index(weekday)
    new_weekdays = [weekdays[weekday_num:] + weekdays[:weekday_num]]
    return new_weekdays[0]

def display_week(data_types, unit): # This is currently unused but is left over from previous toolbar design.
    data_standard_format = data_list(sql_unformatted_by_date(con, data_types), data_types, unit) #Sends the user data to the formatting function data_list.
    data_by_day = sort_24(data_standard_format) # Returns a dictionary for information by day with keys 0-6 (str)
    num1 = len(data_by_day)
    num2 = num1 - 7
    week_list = [data_by_day[str(num2 + i)] for i in range(7)]
    week_list.append(unit)
    return week_list

@functimer
def current_data(data_type, unit, zoneDifference): # This function just runs the data through each algorithm.
    time_now = datetime.now()
    day = int(time_now.day)
    current_datas = sql_unformatted_by_date(con, data_type) # Grabs all temp data for a week period from the db.
    trimmed_datas = trim_dataset(current_datas, day, zoneDifference) # Trims it down to the last 7-day set stored instead of all sets stored.
    data_standard_format = data_list(trimmed_datas, data_type, unit) # This just formats the points into a different order and adds units.
    data_by_day = sort_24(data_standard_format) # Sorts the data into 24 hour periods. Returns a dict of dicts.
    last_7 = int(len(data_by_day)) - 7 # This is left over from before the trim_dataset function was created. 
    dict_of_dicts = {}
    dict_of_dicts.clear()
    
    if int(len(data_by_day)) >= 7: # This is supposed to properly format the data received into a dict of dicts so extend_hours can accept it.
        for i in range(7):
            dict_of_dicts[str(i)] = data_by_day[str(last_7 + i)]
        return dict_of_dicts
    elif int(len(data_by_day)) < 7:
        for i in range(int(len(data_by_day))):
            try:
                dict_of_dicts[str(i)] = data_by_day[str(i)]
            except KeyError:
                print("error")
        return dict_of_dicts 

def catch_api_error(seven_days_unprocessed): # Unused tester.
    dayNums = [seven_days_unprocessed[elt][0][2][8:10] for elt in seven_days_unprocessed] # list of keys
    print(dayNums)

def time_right_now(adjustment): # Grabs current hour.
    print("time_right_now")
    date, time, day, sql_time = date_time_2()
    print(time)
    hour = str(time.split(':')[0])
    return hour

def startup(): # This needs reworked. This just inits the user object and does the GET request from the NOAA API.
    try:
        user = user_startup() # __init__ user object
        times = data_pull(user.get_weather_data)
        return times
        print("done")
    except:
        print("error")
        user = user_startup() # __init__ user object
        times = data_pull(user.get_weather_data)
        return times

# forecast = requests.get(f"https://api.weather.gov/products/types")
# print(forecast)

# converted = json_converter(forecast.text)
# for item in converted['@graph']:
#     print(item)

# dictRequest = {
#     '1':startup()
# }

# print(dictRequest['key'])


# r=requests.get("https://cloud.feedly.com/v3/collections", headers={'Authorization':'Bearer A7KOXa9rC01q5Ft5kP9pShqxMRoBAR-omBqIOA04KWZ16F5lwFL4K9nfvbqOOytZr1WhhNKXiko70RL79stTG4rkp6_z4iIR257odoc7JxobJnqbCuwU-2-6uMWU8sSIGc24pBVC_hToNlkygc7BbHNedJdIU9F_sTqzNUF7iokFmagA-vVeohDcPh2wKBj_sJEhhzBUAdPLbKVPP2jWMIE42LRAqRAhWNIVpoZB4e5V5VELPwW0WJzLhUs:feedlydev'})
# # Once your access token expires, the Feedly Cloud will return an HTTP/401 (“token expired”) response back.

# converted = json_converter(r.text) # converted is a list, trans law at end.
# collectionsIndex = len(converted)-1
# transLawId = converted[collectionsIndex]['id']
# fr=requests.get(f"https://cloud.feedly.com/v3/streams/ids?streamId={transLawId}", headers={'Authorization':'Bearer A7KOXa9rC01q5Ft5kP9pShqxMRoBAR-omBqIOA04KWZ16F5lwFL4K9nfvbqOOytZr1WhhNKXiko70RL79stTG4rkp6_z4iIR257odoc7JxobJnqbCuwU-2-6uMWU8sSIGc24pBVC_hToNlkygc7BbHNedJdIU9F_sTqzNUF7iokFmagA-vVeohDcPh2wKBj_sJEhhzBUAdPLbKVPP2jWMIE42LRAqRAhWNIVpoZB4e5V5VELPwW0WJzLhUs:feedlydev'})
# convertedFeedIds = json_converter(fr.text)
# for item in convertedFeedIds['ids']:
#     print(item)






# efr=requests.get(f"https://cloud.feedly.com/v3/entries/r50dK%2BYAGzv7dCh4KLS0ECEbMBnbGWBftAFgWV%2FFUUM%3D_188662098a4%3Ab23da1%3A46468d4d", headers={'Authorization':'Bearer A7KOXa9rC01q5Ft5kP9pShqxMRoBAR-omBqIOA04KWZ16F5lwFL4K9nfvbqOOytZr1WhhNKXiko70RL79stTG4rkp6_z4iIR257odoc7JxobJnqbCuwU-2-6uMWU8sSIGc24pBVC_hToNlkygc7BbHNedJdIU9F_sTqzNUF7iokFmagA-vVeohDcPh2wKBj_sJEhhzBUAdPLbKVPP2jWMIE42LRAqRAhWNIVpoZB4e5V5VELPwW0WJzLhUs:feedlydev'})
# convertedEntries = json_converter(efr.text)



#language
# id
# fingerprint
# originId
# origin
# title
# crawled
# published
# summary
# alternate
# visual
# canonicalUrl
# fullContent
# canonicalFeed
# unread
# categories
# commonTopics
# entities
# leoSummary
# engagement
# engagementRate
# featuredMeme


# [{"customizable":false,"id":"user/6c7bdaff-82e6-4042-8256-200e19531fe7/tag/global.saved","label":"Saved For Later","enterprise":false},
# {"customizable":true,"id":"user/6c7bdaff-82e6-4042-8256-200e19531fe7/tag/8354ad91-ad3b-477c-ab66-64f127896ded","label":"Transcidal Legislation ","enterprise":false,"created":1684369668447}]
