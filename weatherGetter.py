import requests
import json
import sqlite3
import datetime
import time

con = sqlite3.connect("meteorlite.db") # This is the very first runtime task. Next step is to check if there's any information inthe db.

def sql_table(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE user(id integer PRIMARY KEY, name text, ipv4 text, latitude integer, longitude integer, gridX integer, gridY integer, office text, date text")
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
    cursorObj.execute('create table if not exists user(name text, ipv4 text, latitude integer, longitude integer, gridX integer, gridY integer, office text, date text, time text)')
    con.commit()

def sql_datadump(con, data_type, user_data):
    cursorObj = con.cursor()
    cursorObj.execute(f'create table if not exists {data_type}(name text, unit text, date date,value integer)')
    con.commit()
    cursorObj.execute(f'INSERT INTO {data_type}(name, unit, date, value) VALUES(?, ?, ?, ?,)', user_data)

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

def get_date_time(ip):
    date_time_response = requests.get(f"https://timeapi.io/api/Time/current/ip?ipAddress={ip}")
    date_time_info = json_converter(date_time_response.text)
    year = date_time_info["year"]
    month = date_time_info["month"]
    day = date_time_info["day"]
    hour = date_time_info["hour"]
    minute = date_time_info["minute"]
    second = date_time_info["seconds"]
    date = (f"{year}-{month}-{day}")
    time = (f"{hour}:{minute}:{second}")
    return date, time
    
def startup(): # Startup will check
    con = sqlite3.connect("meteorlite.db") # This is the very first runtime task. Next step is to check if there's any information in the db.
    sql_startup(con) # This function makes a table only if it does not already exist.
    if sql_get_last(con) == None:
        print("if") # If no db entry exists, then no user object data exists. That data and user object is initialized and documented in db.
        ip, latitude, longitude, gridX, gridY, office = get_ip_coords_points()
        name = "user"
        date, time = get_date_time(ip)
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
            date, time = get_date_time(current_ip)
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
            date, time = get_date_time(ip)
            next_id = user_values[0] + 1
            user_values = (next_id, name, ip, latitude, longitude, gridX, gridY, office, date, time)
            sql_insert(con, user_values) # Since the ip in the last db entry has changed, the user object info all has to change too.
            # calling the get_ip_coords_points(), name, date_time allows for a profile to be created for each location in the db, allowing for later
            # analysis based on location most frequented and such.
    con.close()


def extend_hours(obj):
        dict24 = {}
        hours_to_fill = abs(int(obj[0][2][11:13])-24+1) # gets number of total entries from this day to have at the end.
        i = 0
        try:
            while i < hours_to_fill: # i is the it0erator for the total number of db entries for that period.
                current_hour = obj[i][2][11:13] # Gets the hour of the data point we're processing.
                extension_hours = int(obj[i][2].split("T")[2][0:-1])-1# Gets the PT##H ## from the data point we're operating on.
                dict24[current_hour] = obj[i] # makes a dict key-value pair. Key = hour of dp value = the dp
                current_obj = obj[i]
                for x in range(int(extension_hours)): # iterates once for the number of hours to be extended.
                    mt_list = [] # 
                    mt_list.append(current_obj) # = [[x,y,z]]
                    base_hour = mt_list[0][2][11:13] # gets hour number from element
                    print(str(base_hour) + "Base Hour")
                    hour_post_extension = (int(base_hour) + (1)) # x is the iteration number which is the extension number. new is the base hour plus the extension.
                    print(str(hour_post_extension) + "hour-post-extension")
                    mt_list[0][2] = mt_list[0][2][0:11] + str(hour_post_extension) + mt_list[0][2][13:28] + (str(extension_hours-x+1) + "H")
                    dict24[hour_post_extension] = mt_list[0] # dictionary entry extension is the same data but with an hour added for each iteration.
                i += 1
            return dict24
        except IndexError:
            print("IndexError")
            return dict24
            
                    
               
def data_list(user_weather_data, data_type): # returns the lists of value pairs for each data type ( a list with lists[[datetime, value],[datetime,value]])
    data_by_type = user_weather_data['properties'][data_type]['values'] # grabs all of the datetime, value lists
    try: 
        data_unit = user_weather_data['properties'][data_type]['uom'].split(':')[1] # gets the unit for the values
    except KeyError:
        data_unit = None
    listLength = len(data_by_type)
    data_time = [data_by_type[i]["validTime"] for i in range(listLength)]
    data_values = [str(data_by_type[i]['value'])[0:4] for i in range(listLength)]
    data_pre_sort = [[data_type, data_unit, data_time[i], data_values[i]] for i in range(listLength)] #List of lists [name, unit, date, value]
    return data_pre_sort

def sort_24(obj): # This is here to split the week long data sets into days for further processing in extend_hours()
    x = 0
    placeholderList = []
    daysDict = {}
    for i in range(len(obj)-1):
        if obj[i][2][9:10] == obj[i+1][2][9:10]: # If the dates are the same, add the x to the beginning of a 3 part [date,value,unit] list. 
            print("if")
            placeholderList.append([obj[i][0], obj[i][1],obj[i][2], obj[i][3]])
        else:
            print("else")
            placeholderList.append([obj[i][0], obj[i][1], obj[i][2], obj[i][3]]) # each element gets appended to the empty list until you
            daysDict[str(x)] = [elt for elt in placeholderList] # have all the elements of a single day, which the list gets added to a dict keyed for that day
            placeholderList.clear() # list is cleared to start again.
            x += 1
    return daysDict # This will return a dictionary coded from 0:7 that will store all of the individual days of data for a data type.
                

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


def main(): # This is a simulated main loop. This will actually go into the qt application via importing this file and calling startup there.
    user = startup()
    data_by_type = data_list(user.get_weather_data(), 'temperature') 
    data_dict = sort_24(data_by_type) # sort_24 is being passed a LIST OF LISTS 
    print(str(data_dict['0'])+ "\n")
    test_extend = extend_hours(data_dict['1'])
    print(test_extend)
main()       

    # after calling startup the user object will exist within the main loop and its methods can be called.
    # next I need to parse the weather data function into a usable set of variables, set up a new function to make a table for it
    # then make every weather call compare dates with the last user db table entry. If there is not an equal number of entries on both sides, it makes a new one.
    # This may not be the best way to go about it and I can 1000% change my mind after more thinking.
    # Basically, I need to find a way to make one forecast entry per user entry and the forecast must match the table entry of that day.
    # Then, its all about async and calling the user.get_weather_data() to update the forecast whenever a new table entry is made.
    


# Then, in the future, the idea is to add more widgets and data analysis and fun factoids. Then, the arduino code for meteorLite sensoring.
# Then, write code that takes sensor data from arduino and uploads it to a server, which then gives info about ################