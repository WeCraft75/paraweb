import requests
import re
from bs4 import BeautifulSoup


class start:

    def __init__(self, name, lon, lat, ok):
        self.name = name
        self.data = []
        self.lon = lon
        self.lat = lat
        self.ok = ok

        # scraping magic
        soup = BeautifulSoup(requests.post("http://skytech.si/skytechsys/data.php",
                             data={"c": "tabela"}).text, features="html.parser").get_text()
        # go through data piece by piece
        for i in range(1, 6):
            piece_of_data = re.findall(
                name+"\n(.*\n){"+str(i)+"}", string=soup)[0].strip()
            self.data.append(piece_of_data)

    # get current wind speed
    def getWindSpeed(self):
        return self.data[0]

    # get current wind gust
    def getWindGust(self):
        return self.data[1]

    # get current wind direction
    def getWindDirection(self):
        return self.data[2]

    # get current wind temperature
    def getTemperature(self):
        return self.data[3]

    # get current time and date
    def getTimeAndDate(self):
        return self.data[4]

    # get Longitude
    def getLongitude(self):
        return self.lon

    # get Latitude
    def getLatitude(self):
        return self.lat

    # get optimal wind speeds
    def getGoodWind(self):
        return self.ok

    # returns true if wind is optimal, else false
    def isWindGood(self):
        return (self.data[2] in self.ok)
