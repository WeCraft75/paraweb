# pip install requests
# pip install beautifulsoup4
import requests
import re
from bs4 import BeautifulSoup

url = "http://skytech.si/skytechsys/data.php"
reqBody = {"c": "tabela"}

soup = BeautifulSoup(requests.post(
    url, data=reqBody).text, features="html.parser").get_text()
# print(soup.get_text())

jumpPointData = []
jumpPointName = "Kovk"

for i in range(1, 6):
    piece_of_data = re.findall(
        jumpPointName+"\n(.*\n){"+str(i)+"}", string=soup)[0].strip()
    jumpPointData.append(piece_of_data)

print(jumpPointData)
