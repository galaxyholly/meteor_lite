import requests
import json
import sqlite3

from timeit import default_timer as timer
from datetime import datetime, timedelta

def functimer(func): # This is just a decorator function I can use to measure a functions runtime.
    def wrapper(*args, **kwargs):
        start = timer()
        obj = func(*args)
        end = timer()
        time_elapsed = end - start
        print(str(time_elapsed) + " - Time Elapsed")
        return obj
    return wrapper

@functimer
def date_time_2():
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
    sql_date = sql_new + timedelta(days=7)
    sql_final_date = str(sql_date).split(" ")[0]
    
    return date, time, weekday_name, str(sql_final_date)

data_types = [ # 26 dt's
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

con = sqlite3.connect("meteorlite.db") # This is the very first runtime task. Next step is to check if there's any information inthe db.

def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE if not exists user(id integer PRIMARY KEY, name text, ipv4 text, latitude integer, longitude integer, gridX integer, gridY integer, office text, date text")
    con.commit()

def sql_insert(con, userData):
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO user(id, name, ipv4, latitude, longitude, gridX, gridY, office, date, time) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', userData)
    con.commit()

def sql_update(con):
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE user SET ipv4 = "0.0.0.0" where id = 1')
    con.commit()

def sql_get(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * from user')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)

def sql_delete(con):
    cursorObj = con.cursor()
    cursorObj.execute('DELETE from user WHERE id = 2')
    con.commit()

def sql_get_last(con):
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * FROM user ORDER BY id DESC LIMIT 1')
    last = cursorObj.fetchone()
    return last

def sql_startup(con):
    cursorObj = con.cursor()
    cursorObj.execute('create table if not exists user(id integer PRIMARY KEY, name text, ipv4 text, latitude integer, longitude integer, gridX integer, gridY integer, office text, date text, time text)')
    con.commit()

def sql_datadump(con, data_type, user_data):
    cursorObj = con.cursor()
    cursorObj.execute(f'create table if not exists {data_type}(name text, unit text, date date, value integer)')
    con.commit()
    cursorObj.execute(f'INSERT INTO {data_type}(name, unit, date, value) VALUES(?, ?, ?, ?)', user_data)
    con.commit()

def sql_get_test(con, table):
    cursorObj = con.cursor()
    cursorObj.execute(f'SELECT * from {table}')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)

def sql_make_unformatted_tables(con): # This will be run on startup. Creates time loss on very first time its run, after that it takes no time.
    cursorObj = con.cursor()
    for data_type in data_types:
        cursorObj.execute(f'create table if not exists {data_type}(validTime text, value text)')
        con.commit()
        
@functimer
def sql_unformatted_test(con):
    cursorObj = con.cursor()
    cursorObj.execute(f'SELECT * from temperature')
    rows = cursorObj.fetchall()
    for row in rows:
        print(row)

def sql_unformatted_by_date(con, dtype): # This will be the function we use to get data for x days.
    date, time, weekday, sql_time = date_time_2()
    cursorObj = con.cursor()
    cursorObj.execute(f"SELECT * from {dtype} Where validTime BETWEEN '{date}' AND '{sql_time}'") # Don't change these days
    rows = cursorObj.fetchall()
    rowList = [row for row in rows]
    return rowList

@functimer
def sql_unformatted_add_test(con, weather_data): # This function will add in all the data from the user.get_weather_data() method.
    cursorObj = con.cursor()
    for data_type in data_types:
        for i in range(len(weather_data['properties'][data_type]['values'])):
            data_point = [str(weather_data['properties'][data_type]['values'][i]['validTime']), str(weather_data['properties'][data_type]['values'][i]['value'])]  
            cursorObj.execute(f'INSERT INTO {data_type}(validTime, value) VALUES(?, ?)', data_point)
    con.commit()

def sql_unformatted_delete(con):
    for data_type in data_types:
        cursorObj = con.cursor()
        cursorObj.execute(f'DELETE from {data_type}')
    con.commit()

def sql_unformatted_drop_table(con):
    for data_type in data_types:
        cursorObj = con.cursor()
        cursorObj.execute(f'DROP TABLE {data_type};')
    con.commit()
    # cursorObj = con.cursor()
    # cursorObj.execute('create table if not exists data(id integer PRIMARY KEY, date text, 01 text,latitude integer, longitude integer, gridX integer, gridY integer, office text, date text, time text)')

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
        forecast = requests.get(f"https://api.weather.gov/gridpoints/{str(self.office)}/{str(self.gridX)},{str(self.gridY)}/")
        forecast_reader_info = json_converter(forecast.text)
        return forecast_reader_info

def json_converter(content):
    info = json.loads(content)
    print("json converted")
    return info

def get_ip(): # Can be requested as much as needed.
    ipv4 = requests.get('https://api.ipify.org').content.decode('utf8')
    return ipv4
    
def get_ip_coords(): # Very limited requests.
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
 
def get_ip_coords_points(): # Request as much as needed.
    ip_coords = get_ip_coords()
    points_request = requests.get(f"https://api.weather.gov/points/{ip_coords[1]},{ip_coords[2]}")
    points_python = json_converter(points_request.text)
    gridX = points_python["properties"]["gridX"]
    gridY = points_python["properties"]["gridY"]
    office = points_python["properties"]["cwa"]
    print(gridX, gridY, office)
    ip_coords_points= [str(ip_coords[0]), ip_coords[1], ip_coords[2], gridX, gridY, office]
    return ip_coords_points

def user_startup(): # Startup will check
    con = sqlite3.connect("meteorlite.db") # This is the very first runtime task. Next step is to check if there's any information in the db.
    sql_startup(con) # This function makes a table only if it does not already exist.
    if sql_get_last(con) == None:
        print("if") # If no db entry exists, then no user object data exists. That data and user object is initialized and documented in db.
        ip, latitude, longitude, gridX, gridY, office = get_ip_coords_points()
        name = "user"
        date, time, weekday, sql_time = date_time_2()
        user_values = (1, name, ip, latitude, longitude, gridX, gridY, office, date, time)
        sql_insert(con, user_values)
        user_values = sql_get_last(con)
        print(user_values)
        user = User(user_values[0],user_values[1],user_values[2],user_values[3],user_values[4],user_values[5],user_values[6],user_values[7], user_values[8], user_values[9])
        return user # ultimately all of these outcomes result in a db entry on a user object returned.
    else: # If there is a previous db entry, it must be checked against IP to ensure the user is still in the same geo-location.
        print("else")
        user_values = sql_get_last(con) # Start by getting the latest entry from the db. get ip, check if ip is same.
        current_ip = get_ip()
        if current_ip == user_values[2]: # comparing the current ip to the last db entries ip. If ==, user object is init with the previous db info. 
            print("if current_ip == user_values[2]:")
            user = User(user_values[0],user_values[1],user_values[2],user_values[3],user_values[4],user_values[5],user_values[6],user_values[7], user_values[8], user_values[9])
            date, time, weekday, sql_time = date_time_2()
            # print(user.get_weather_data()) this is here for diagnostic purposes
            if date != user_values[8]: # if current date is not equal to db listed date, make a new entry with updated date.
                print("if date != user_values[8]:")
                next_id = user_values[0] + 1 # Since this is a new date, we need to denote a new access for forecast data. Id needs to be updated since a unique entry will be made.
                new_date_entry = (next_id,user_values[1],user_values[2],user_values[3],user_values[4],user_values[5],user_values[6],user_values[7], date, time)
                sql_insert(con, new_date_entry)
                return user
            print("made it")
            return user
        else: # If current ip is not last db entry ip, make a new entry.
            print("# If current ip is not last db entry ip, make a new entry.")
            ip, latitude, longitude, gridX, gridY, office = get_ip_coords_points()
            name = "user"
            date, time, weekday, sql_time = date_time_2()
            next_id = user_values[0] + 1
            user_values = (next_id, name, ip, latitude, longitude, gridX, gridY, office, date, time)
            sql_insert(con, user_values) # Since the ip in the last db entry has changed, the user object info all has to change too.
            # calling the get_ip_coords_points(), name, date_time allows for a profile to be created for each location in the db, allowing for later
            # analysis based on location most frequented and such.
    con.close()

def data_pull(user_weather_data):
    weather_data = user_weather_data()
    sql_make_unformatted_tables(con) # This is the creation function for the raw data tables.
    sql_unformatted_add_test(con, weather_data) # This function intakes the weather data and stores it all.

def extend_hours(obj): #obj is a dict with 7 days worth of datapoints, separated by numbers (as the keys) starting from 0, ending in 6.
    dict_7_days = {} # This initializes what will be the final dictionary containing 7 dictionaries each with 24 datapoints (or close)
    dict_1_day = {} 
    day_counter = 0 # This will set the current key the data points are being saved to.
    sample = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]

    for i in sample:
        dict_7_days[str(i)] = dict_1_day.copy()

    for dataSet in obj:
        if day_counter == 7:
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
            try:
                extension_hours = int(point[2].split("PT")[1][0:-1])-1
                print(str(extension_hours)+"EXTENSION_HOURS")
            except IndexError:
                print("Has Day")
                extension_hours = -1
                try:
                    breakdown = point[2].split("P")[1].split("T")
                    days = int(breakdown[0][:-1]) # Goes to an algorithm.
                    print(days)
                    hours = int(breakdown[1][:-1])-1 # Waits until days are done and then goes into reg algo.
                    print(hours)
                    hours_total = (days * 24) + hours 
                    print(hours_total)
                    hours_left_of_current_day = 23 - current_hour
                    print(hours_left_of_current_day)
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

                        
                    
                except IndexError:
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
                
                    
            if extension_hours > 0 and (current_hour + extension_hours) <= 23: # 
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
                    print("SILLYBOBDWADWADDAWDADSADASDADDDDDDDDDDDDDDDDDDDDd")
                    item = [item for item in dict_7_days['6']]
                    print(str(item) + "ITEM")
                    day_counter += 1
                    continue
                
                     
            elif extension_hours > 0 and (current_hour + extension_hours) > 23:
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
                

            elif str(point[2][11:13]) == str(23):
                dict_7_days[str(day_counter)][str(current_hour)] = point.copy()
                day_counter += 1
                print("POINT ON 23")

            elif extension_hours == 0:
                if current_hour <= 9:
                    print("SPECIF")
                    new_hour = ("0" + str(current_hour))# Will just add each larger i to a copy of the base point hour.
                    dict_7_days[str(day_counter)][str(new_hour)] = point.copy()
                    
                elif current_hour > 10:
                    print("SPECELSE")
                    new_hour = str(current_hour)
                    dict_7_days[str(day_counter)][str(new_hour)] = point.copy()
                    
                elif current_hour == 0:
                    
                    continue
                print("ADDING POINT")
                print("else")
 
    return dict_7_days

def trim_dataset(obj): # This will be a simple func that takes the dictionary, orders it by date, grabs 7, junks the rest.
    pass

@functimer            
def data_list(user_weather_data, data_type, data_unit): # returns the lists of value pairs for each data type ( a list with lists[[datetime, value],[datetime,value]])
    data_pre_sort = [[data_type, data_unit, user_weather_data[i][0], str(user_weather_data[i][1])[0:4]] for i in range(int(len(user_weather_data )))]
    return data_pre_sort # I think this needs optimizing.

@functimer
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

def sort_week_from_today():
    date, time, weekday, sql_time = date_time_2()
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

def current_data(data_type, unit):
    current_datas = sql_unformatted_by_date(con, data_type) # Grabs all temp data for a week.
    data_standard_format = data_list(current_datas, data_type, unit) # Formats it right.
    data_by_day = sort_24(data_standard_format)
    print(str(len(data_by_day)) + "LENGTH")
    last_7 = int(len(data_by_day)) - 7 # This needs to be around here to get all.
    print(str(last_7)+ "LENGTH") 
    dict_of_dicts = {}
    dict_of_dicts.clear()
    for i in range(7):
        print(str(last_7 + i))
        dict_of_dicts[str(i)] = data_by_day[str(last_7 + i)]
        
    return dict_of_dicts # works :/

def catch_api_error(seven_days_unprocessed):
    dayNums = [seven_days_unprocessed[elt][0][2][8:10] for elt in seven_days_unprocessed] # list of keys
    print(dayNums)

def time_right_now():
    date, time, day, sql_time = date_time_2()
    print(time)
    hour = str(time.split(':')[0])
    return hour

def startup(): # This is a simulated main loop. This will actually go into the qt application via importing this file and calling startup there.
    user = user_startup() # __init__ user object
    data_pull(user.get_weather_data) # Pulls and stores data from current time

# precipPer_7days_24 = current_data('visibility', '%') 

# print(precipPer_7days_24['0'])
# print("\n")
# print(precipPer_7days_24['1'])
# print("\n")
# print(precipPer_7days_24['2'])
# print("\n")
# print(precipPer_7days_24['3'])
# print("\n")
# print(precipPer_7days_24['4'])
# print("\n")
# print(precipPer_7days_24['5'])
# print("\n")
# print(precipPer_7days_24['6'])
# print("\n") 

# precipPer_7days_24_extend = extend_hours(precipPer_7days_24)


# print(precipPer_7days_24_extend['0'])
# print("\n")
# print(precipPer_7days_24_extend['1'])
# print("\n")
# print(precipPer_7days_24_extend['2'])
# print("\n")
# print(precipPer_7days_24_extend['3'])
# print("\n")
# print(precipPer_7days_24_extend['4'])
# print("\n")
# print(precipPer_7days_24_extend['5'])
# print("\n")
# print(precipPer_7days_24_extend['6'])

# print(sql_unformatted_by_date(con, 'visibility'))


# time_rn = time_right_now()
# print(time_rn)

# week_list = sort_week_from_today()
# day_no = day_no = str(week_list.index('Thursday'))

# temp_rn = str(precipPer_7days_24_extend[day_no][time_rn][3] + "°")
# print(temp_rn)