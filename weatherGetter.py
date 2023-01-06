import requests
import json

# This is just test data for my current position. Used in conjunction with forecasts down below to get weather data in .json form
lat = 37.0505
lon = -93.3001

# This is the user class. Functionality of the app will be based off of information stored in this class. A single user is defined, 
# the name and ip are taken and stored. This class will contain the methods used to obtain the coordinates associated with the user's ip.
# This will auto update on startup, possibly upon moving, although that is only if there is funding for the app and associated services needed.
# A refresh button will be added. Name may be stored between sessions, ip address is as well to limit the use of the ip website.
class User:
    def __init__(self, name, ip):
        self.IPv4 = ip
        self.name = name

        # This function runs the users public IPv4 address through ipstack.com's api to GET the user's longitudinal and latitudinal location.
        # LIMIT USE, 100 maximum uses per month.
    def convert_coordinates(self):
        ip = self.IPv4
        location_data = requests.get(f"http://api.ipstack.com/{ip}?access_key=0b85fa09f8ce75a20932950f1f3a25e6")
        print(f"converting {self.IPv4} into coordinates")
        return location_data.text

        #This method converts the latitude and longitude of the user's IP to get the grid points of the weather station in the area.
    def get_points(self):
        points_request = requests.get(f"https://api.weather.gov/points/{lat},{lon}")
        return points_request.text

# This function will run on startup in order to either determine a new IP or read it from file. If file is not present if will automatically
# create a config file of its own.            
def get_ip():
    
    try:
        # begins with opening config file. If it exists and is blank, the first if statement is executed. It simply does a GET request,
        # then opens a writer for the text file and writes a formatted message containing the ipv4.
        with open('config.txt', 'r') as reader:
            configList = reader.readlines()
            if configList == []:
                ipv4 = requests.get('https://api.ipify.org').content.decode('utf8')
                with open('config.txt', 'x') as writer:
                    writer.write(f"IPv4 Address: {ipv4}")
                    print("IPv4 written to config.txt")
                    return ipv4
            else: # If the file contains the IP, it's read into returning the ipv4 variable. Need to add a clause that takes care of wrong IP.
                ipv4 = configList[0].split(" ")[-1] 
                print(f"IPv4 read from config.txt {ipv4}")
                return ipv4

    except FileNotFoundError: #If file is not found it writes a new one.
        with open('config.txt', 'x') as writer:
            ipv4 = requests.get('https://api.ipify.org').content.decode('utf8')
            writer.write(f"IPv4 Found: {ipv4}")
            print("File 'config.txt' created and IPv4 configured")
            return ipv4


            

user = User("Holly", get_ip())
# user_coordinate_dictionary = user.convert_coordinates()
# user_latitude = user_coordinate_dictionary["latitude"]
# user_longitude = user_coordinate_dictionary["longitude"]     
points_json = user.get_points()
points_python = json.loads(points_json)
gridX = points_python["properties"]["gridX"]
gridY = points_python["properties"]["gridY"]
office = points_python["properties"]["cwa"]
print(gridX, gridY, office)

forecast = requests.get(f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast")
print(forecast.text)







# weather = requests.get(f'http://api.ipstack.com/{ipv4}?access_key=0b85fa09f8ce75a20932950f1f3a25e6')
# print(weather.text)       