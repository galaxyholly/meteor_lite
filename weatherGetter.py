import requests
import json

lat = 37.0505
lon = -93.3001

class User:
    def __init__(self, name, ip):
        self.IPv4 = ip
        self.name = name

        # This function runs the users public IPv4 address through ipstack.com's api to GET the user's longitudinal and latitudinal location.
    def convert_coordinates(self):
        ip = self.IPv4
        location_data = requests.get(f"http://api.ipstack.com/{ip}?access_key=0b85fa09f8ce75a20932950f1f3a25e6")
        print(f"converting {self.IPv4} into coordinates")
        return location_data.text

    def get_points(self):
        points_request = requests.get(f"https://api.weather.gov/points/{lat},{lon}")
        return points_request.text
            
def get_ip():
    try:
        with open('config.txt', 'r') as reader:
            configList = reader.readlines()
            if configList == []:
                ipv4 = requests.get('https://api.ipify.org').content.decode('utf8')
                with open('config.txt', 'x') as writer:
                    writer.write(f"IPv4 Address: {ipv4}")
                    print("IPv4 written to config.txt")
                    return ipv4
            else:
                ipv4 = configList[0].split(" ")[-1] 
                print(f"IPv4 read from config.txt {ipv4}")
                return ipv4

    except FileNotFoundError: 
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