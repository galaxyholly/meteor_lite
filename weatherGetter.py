from bs4 import BeautifulSoup
import requests

URL = 'https://www.google.com/search?channel=fs&client=ubuntu&q=weather+nixa+mo'
r = requests.get(URL)
bs4Text = r.text
weatherPage = BeautifulSoup(bs4Text, "lxml")


mainChild = weatherPage.find_all("div", id="main")
print(type(mainChild))
child_div = mainChild[0]
print(len(child_div.find_all("div")))



