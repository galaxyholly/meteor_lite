import requests
import json



# This is the user class. Functionality of the app will be based off of information stored in this class. A single user is defined, 
# the name and ip are taken and stored. This class will contain the methods used to obtain the coordinates associated with the user's ip.
# This will auto update on startup, possibly upon moving, although that is only if there is funding for the app and associated services needed.
# A refresh button will be added. Name may be stored between sessions, ip address is as well to limit the use of the ip website.
class User:
    def __init__(self, name, ip_coords_points):
        self.name = name
        self.IPv4 = ip_coords_points[0]
        self.latitude = ip_coords_points[1]
        self.longitude = ip_coords_points[2]
        self.gridX = ip_coords_points[3]
        self.gridY = ip_coords_points[4]
        self.office = ip_coords_points[5]

    def get_weather():
        print("nothing")

def json_converter(content):
    info = json.loads(content)
    print("json converted")
    return info

def get_ip():
    ipv4 = requests.get('https://api.ipify.org').content.decode('utf8')
    ipv4 = str(ipv4)
    print("ip from pull: " + ipv4)
    try:
        with open('config.txt', 'r') as reader:
            configList = reader.readlines()
            test = configList[0].split(" ")[-1]
            print(f"ip from config.txt: {test}")          
            if configList == []: # If the config file exists, but is empty.
                print("if")
                print(configList)
                with open('config.txt', 'w') as writer:
                    writer.write(f"IPv4 Found: {ipv4}")
                ipv4_instruct = [ipv4, 1]
                return ipv4_instruct
            elif str(test) == str(f"IPv4 Found: {ipv4}"): # If the ip listed in config is equal to the ip just requested.
                print("elif")
                print(configList)
                ipv4_instruct = [ipv4, 0]
                return ipv4_instruct
            else:
                print("else")
                print(configList)
                with open('config.txt', 'w') as writer:
                    writer.writelines([f"IPv4 Found: {ipv4}\n{configList[1]}{configList[2]}"])
                print(configList)
                ipv4_instruct = [ipv4, 0]
                print(configList)
                return ipv4_instruct
    except FileNotFoundError: 
        with open('config.txt', 'w') as writer:
            writer.write(f"IPv4 Found: {ipv4}")
            print("FileNotFoundErrorExcept")
            ipv4_instruct = [ipv4, 0]
            return ipv4_instruct
            
def get_ip_coords():
    ip, status = get_ip()
    if status == 1:
        print("status 1")
        location_data = requests.get(f"http://api.ipstack.com/{ip}?access_key=0b85fa09f8ce75a20932950f1f3a25e6")
        print(f"converting {ip} into coordinates")
        user_coordinate_dictionary = json_converter(location_data.text)
        latitude = user_coordinate_dictionary["latitude"][0:5]
        longitude = user_coordinate_dictionary["longitude"][0:5]
        ip_coords = [ip, latitude, longitude]
        with open('config.txt','w') as writer:
            writer.writelines([f"IPv4 Found: {ip}", f"Latitude: {latitude}", f"Longitude: {longitude}"])
        return ip_coords
    elif status == 0:
        print("status 0")
        with open('config.txt', 'r') as reader:
            configList = reader.readlines()
            print(str(configList))
            print(str(configList[0].split(" ")[-1]))
            ip_coords = [configList[0].split(" ")[-1], configList[1].split(" ")[-1], configList[2].split(" ")[-1]]
            return ip_coords


def get_ip_coords_points():
    ip_coords = get_ip_coords()
    points_request = requests.get(f"https://api.weather.gov/points/{ip_coords[1]},{ip_coords[2]}")
    points_python = json_converter(points_request.text)
    gridX = points_python["properties"]["gridX"]
    gridY = points_python["properties"]["gridY"]
    office = points_python["properties"]["cwa"]
    print(gridX, gridY, office)
    ip_coords_points= [ip_coords[0], ip_coords[1], ip_coords[2], gridX, gridY, office]
    return ip_coords_points

def get_weather_data(office, gridX, gridY):
    forecast = requests.get(f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast")
    print(forecast.text)

user = User("Holly", get_ip_coords_points())
print(user.gridX)
# get_weather_data(user.gridX, user.gridY)
# points_json = user.get_points()
# points_python = json.loads(points_json)
# gridX = points_python["properties"]["gridX"]
# gridY = points_python["properties"]["gridY"]
# office = points_python["properties"]["cwa"]
# print(gridX, gridY, office)

# 'https://www.timeapi.io/api/Time/current/coordinate?latitude=38.9&longitude=-77.03'
# gets year month day hour minute seconds milliseconds date timezone time dayofweek

# with open('config.txt', 'x') as writer:
    #     ipv4 = requests.get('https://api.ipify.org').content.decode('utf8')
    #     writer.write(f"IPv4 Found: {ipv4}")
    #     print("File 'config.txt' created and IPv4 configured")
    #     return ipv4

        # begins with opening config file. If it exists and is blank, the first if statement is executed. It simply does a GET request,
        # then opens a writer for the text file and writes a formatted message containing the ipv4.

    #     with open('config.txt', 'r') as reader:
    #         configList = reader.readlines()
    #         if configList == []:
    #             ipv4 = requests.get('https://api.ipify.org').content.decode('utf8')
    #             with open('config.txt', 'x') as writer:
    #                 writer.write(f"IPv4 Address: {ipv4}")
    #                 print("IPv4 written to config.txt")
    #                 return ipv4
    #         else: # If the file contains the IP, it's read into returning the ipv4 variable. Need to add a clause that takes care of wrong IP.
    #             ipv4 = configList[0].split(" ")[-1] 
    #             print(f"IPv4 read from config.txt {ipv4}")
    #             return ipv4
    # except FileNotFoundError: #If file is not found it writes a new one.
    #    
