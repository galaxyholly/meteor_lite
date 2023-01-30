import requests
import json
import sqlite3

from timeit import default_timer as timer
from datetime import datetime

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

def functimer(func): # This is just a decorator function I can use to measure a functions runtime.
    def wrapper(*args, **kwargs):
        start = timer()
        obj = func(*args)
        end = timer()
        time_elapsed = end - start
        print(str(time_elapsed) + " - Time Elapsed")
        return obj
    return wrapper

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
    cursorObj = con.cursor()
    cursorObj.execute(f"SELECT * from {dtype} where validTime < date('now','7 days')") # Don't change these days
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

@functimer
def date_time_2():
    weekday_map = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    time_now = datetime.now()
    year = time_now.year
    month = time_now.month
    day = time_now.day
    hour = time_now.hour
    minute = time_now.minute
    second = time_now.second
    date = (f"{year}-{month}-{day}")
    time = (f"{hour}:{minute}:{second}")
    weekday = time_now.weekday()
    weekday_name = weekday_map[weekday]
    return date, time, weekday_name

def user_startup(): # Startup will check
    con = sqlite3.connect("meteorlite.db") # This is the very first runtime task. Next step is to check if there's any information in the db.
    sql_startup(con) # This function makes a table only if it does not already exist.
    if sql_get_last(con) == None:
        print("if") # If no db entry exists, then no user object data exists. That data and user object is initialized and documented in db.
        ip, latitude, longitude, gridX, gridY, office = get_ip_coords_points()
        name = "user"
        date, time, weekday = date_time_2()
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
            date, time, weekday = date_time_2()
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
            date, time, weekday = date_time_2()
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

    for dataSet in obj:
        dict_7_days[str(day_counter)] = dict_1_day.copy() # setup dictionaries so I can use index/slice notation to append to dicts.
        working_datapoint_set = obj[dataSet]
        print(str(working_datapoint_set) + "WORKING_DATAPOINT_SET")
        first_hour = str(obj[dataSet][0][2][11:13]) # Day -> First datapoint -> date_time -> hour 
        print(first_hour + "FIRST_HOUR")
        dict_7_days[str(day_counter)][first_hour] = working_datapoint_set[0].copy()

        for point in working_datapoint_set: # ['probabilityOfPrecipitation', '%', '2023-02-02T12:00:00+00:00/PT12H', '7'] - for reference
            print(str(point)+"POINT")
            extension_hours = int(point[2].split("T")[2][0:-1])-1
            print(str(extension_hours)+"EXTENSION_HOURS")
            current_hour = str(point[2][11:13])
            print(current_hour + "CURRENT_HOUR")
            if extension_hours > 0 and (int(current_hour) + extension_hours) <= 23:
                print("if")
                working_point = point.copy()
                working_point_date_time = working_point[2]
                print(str(working_point_date_time) + "WORKING_POINT_DATE_TIME")
                dict_7_days[str(day_counter)][current_hour] = working_point
                for i in range(1, extension_hours + 1):
                    # We have to take the working point and build a new one using parts, and use i to change the deets. + 1 hour, -1 extn hour. 
                    # Will just add each larger i to a copy of the base point hour.
                    old_hour = int(working_point_date_time[11:13])
                    if old_hour + i <= 9:
                        new_hour = "0" + str(old_hour + i) # Will just add each larger i to a copy of the base point hour.
                    else:
                        new_hour = str(old_hour + i) # Will just add each larger i to a copy of the base point hour.
                    new_extension_count = int(working_point_date_time.split("T")[2][0:-1])-i # This is the PT##H at the end. Splits and takes after the T [-1]. Subtracts i.
                    build_point = working_point_date_time[0:11] + str(new_hour) + working_point_date_time[13:28] + str(new_extension_count) + "H"
                    print(build_point + "BUILD POINT")
                    dict_7_days[str(day_counter)][str(new_hour)] = [working_point[0], working_point[1], build_point, working_point[3]] #appends to dict.
                    if str(dict_7_days[str(day_counter)][str(new_hour)][2][11:13]) == str(23):
                        print("SILLYBOBDWADWADDAWDADSADASDADDDDDDDDDDDDDDDDDDDDd")
                        day_counter += 1
                        continue
            hour_rn = str(dict_7_days[str(day_counter)][str(point[2][11:13])][2][11:13])
            # print(hour_rn + "HOUR_RN")
            if hour_rn == str(23):
                print("SILLYBOBDWADWADDAWDADSADASDADDDDDDDDDDDDDDDDDDDDd")
                day_counter += 1
                continue
                    
            elif extension_hours > 0 and (int(current_hour) + extension_hours) > 23:
                print("elif")
                hours_to_carry_over = extension_hours - (23 - int(current_hour)) # This grabs the extra off the end of the hours to use for the next days set.
                extension_hours_trimmed = extension_hours - hours_to_carry_over
                working_point = point.copy()
                working_point_date_time = working_point[2]
                for i in range(1, extension_hours_trimmed):
                    old_hour = int(working_point_date_time[11:13])
                    if old_hour < 10:
                        new_hour = "0" + str(old_hour + i) # Will just add each larger i to a copy of the base point hour.
                    else:
                        new_hour = str(old_hour + i) # Will just add each larger i to a copy of the base point hour.
                    new_extension_count = int(working_point_date_time.split("T")[2][0:-1])-1-i # This is the PT##H at the end. Splits and takes after the T [-1]. Subtracts i.
                    build_point = working_point_date_time[0:11] + str(new_hour) + working_point_date_time[13:28] + str(new_extension_count) + "H"
                    dict_7_days[str(day_counter)][str(new_hour)] = [working_point[0], working_point[1], build_point, working_point[3]]
                day_counter += 1
                dict_7_days[str(day_counter)] = dict_1_day.copy()
                working_point_next_day_base = working_point.copy() # Need to change the date now and reset time to 00:00, set ## in PT##H to hours_to_carry_over
                old_date = int(working_point_next_day_base[2][9:10])
                if old_date < 10:
                    new_date = "0" + str(old_date + 1)
                else:
                    new_date = str(old_date + 1)
                time_reset = "00"
                working_point_next_day = [working_point_next_day_base[0], working_point_next_day_base[1], (working_point_next_day_base[2][0:8] + new_date + "T" + time_reset + working_point_next_day_base[2][13:28] + str(hours_to_carry_over) + "H"), working_point_next_day_base[3]]
                working_point_next_day_date_time = working_point_next_day[2]
                for i in range(1, hours_to_carry_over):
                    old_hour = int(working_point_next_day_date_time[11:13])
                    if old_hour < 10:
                        new_hour_int = old_hour + i
                        new_hour2 = "0" + str(new_hour_int)# Will just add each larger i to a copy of the base point hour.
                    else: #old_hour > 10:
                        new_hour2 = str(old_hour + i)
                    new_extension_count = int(working_point_next_day_date_time.split("T")[2][0:-1])-1-i # This is the PT##H at the end. Splits and takes after the T [-1]. Subtracts i.
                    build_point = working_point_next_day_date_time[0:11] + str(new_hour) + working_point_next_day_date_time[13:28] + str(new_extension_count) + "H"
                    dict_7_days[str(day_counter)][str(new_hour2)] = [working_point_next_day[0], working_point_next_day[1], build_point, working_point_next_day[3]]
                continue
            else:
                print("else")
                continue
            continue
    return dict_7_days


# abc = ['probabilityOfPrecipitation', '%', ['probabilityOfPrecipitation', '%', '2023-018T00:00:00+00:00/PT17H', '0']
# print(abc[2][8:10])        






        











        # print(obj)
        # dict24 = {}
        # hours_missing = abs(int(obj[0][2][11:13])-24+1) # gets number of total entries from this day to have at the end.
        # non_extension_hours = len(obj) - 1
        # extension_total = hours_missing - non_extension_hours
        # i = 0
        # try:
        #     for i in range(extension_total): # i is the iterator for the total number of db entries for that period.
        #         current_hour = obj[i][2][11:13] # Gets the hour of the data point we're processing.
        #         extension_hours = int(obj[i][2].split("T")[2][0:-1])-1# Gets the PT##H ## from the data point we're operating on.
        #         extensions_left = extension_total - len(dict24)
        #         if extension_hours > extensions_left:
        #             extension_hours = extensions_left
        #         dict24[current_hour] = obj[i] # makes a dict key-value pair. Key = hour of dp value = the dp
        #         current_obj = dict24[current_hour].copy()
        #         for x in range(extension_hours): # iterates once for the number of hours to be extended.
        #             mt_list = []
        #             mt_list.clear()
        #             mt_list.append(current_obj) # = [[x,y,z]]
        #             base_hour = mt_list[0][2][11:13] # gets hour number from element
        #             hour_post_extension = (int(base_hour) + (1)) # x is the iteration number which is the extension number. new is the base hour plus the extension.
        #             if len(str(hour_post_extension)) == 1:
        #                 hour_post_extension = "0" + str(hour_post_extension)
        #                 mt_list[0][2] = mt_list[0][2][0:11] + str(hour_post_extension) + mt_list[0][2][13:28] + 3
        #                 dict24[str(hour_post_extension)] = mt_list[0].copy() # dictionary entry extension is the same data but with an hour added for each iteration.
        #                 print("you have reached the core")
        #                 i += 1
        #                 print(i)
        #                 continue
        #             mt_list[0][2] = mt_list[0][2][0:11] + str(hour_post_extension) + mt_list[0][2][13:28] + (str(extension_hours-x) + "H")
        #             dict24[str(hour_post_extension)] = mt_list[0].copy() # dictionary entry extension is the same data but with an hour added for each iteration.
        #             print("you have reached the non-core")
        #             i += 1
        #     return dict24
        # except IndexError:
        #     print("IndexError")
        #     return dict24

# abc = ['probabilityOfPrecipitation', '%', '2023-01-27T11:00:00+00:00/PT7H', '1']
# print(abc[2][11:13])
# print(int(abc[2].split("T")[2][0:-1])-1)
# print(len(sql_unformatted_by_date(con, 'temperature')))

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
    return daysDict # This will return a dictionary coded from 0:7 that will store all of the individual days of data for a data type.

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
    date, time, day = date_time_2()
    print(time)
    hour = int(time.split(':')[0])
    if hour < 10:
        time_rn = "0" + str(hour)
        return time_rn
    else: 
        time_rn = str(int(time.split(':')[0]))
        return time_rn

def startup(): # This is a simulated main loop. This will actually go into the qt application via importing this file and calling startup there.
    user = user_startup() # __init__ user object
    data_pull(user.get_weather_data) # Pulls and stores data from current time

