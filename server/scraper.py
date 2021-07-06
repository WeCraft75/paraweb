# pip install requests beautifulsoup4
import requests
import re
import datetime
from bs4 import BeautifulSoup


def getCurrentWindInfo():
    url = "http://skytech.si/skytechsys/data.php"

    reqBody = {"c": "tabela"}

    soup = BeautifulSoup(requests.post(
        url, data=reqBody).text, features="html.parser").get_text()
    # print(soup.get_text())

    jumpPointData = []
    jumpPointName = "Kovk"

    for i in range(1, 6):
        piece_of_data = re.findall(
            jumpPointName+"\n(.*\n){"+str(i)+"}", string=soup)[0].strip()  # NAME\n(.*\n){i}
        jumpPointData.append(piece_of_data)

    jumpPointData[0] = float(jumpPointData[0].replace(" m/s", ""))
    jumpPointData[1] = float(jumpPointData[1].replace(" m/s", ""))
    jumpPointData[3] = float(jumpPointData[3].replace("°C", ""))
    jumpPointData[4] = datetime.datetime.strptime(
        jumpPointData[4], "%H:%M %d.%m.%Y")  # datetime.datetime.strptime, why is datetime neccesary twice ???
    # data = [wind speed, wind gust, wind direction, temperature, time and date]
    return jumpPointData
