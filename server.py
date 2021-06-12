import requests
import re
from bs4 import BeautifulSoup


class start:

    def __init__(self, name, lon, lat, ok):  # name = name of the awesome paraStart
        self.name = name
        self.data = []
        self.lon = lon
        self.lat = lat
        self.ok = ok

        # scraping magic
        soup = BeautifulSoup(requests.post("http://skytech.si/skytechsys/data.php",
                             data={"c": "tabela"}).text, features="html.parser").get_text()
        # extract data piece by piece
        # data = [wind speed, wind gust, wind direction, temperature, time of observation]
        for i in range(1, 6):
            piece_of_data = re.findall(
                name+"\n(.*\n){"+str(i)+"}", string=soup)[0].strip()
            self.data.append(piece_of_data)

    def getWindSpeed(self):
        return self.data[0]

    def getWindBust(self):
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

    def getLongitude(self):
        return self.lon

    def getLatitude(self):
        return self.lat

    # get optimal wind directions
    def getGoodWind(self):
        return self.ok

    # returns true if wind is optimal, else false
    def isWindGood(self):
        return (self.data[2] in self.ok)


listOfSites = {
    'Gozd': {
        'lon': 46.3395,
        'lan': 14.3313,
        'ok': ('JZ', 'J', 'JV')
    },
    'Ratitovec': {
        'lon': 46.2361,
        'lan': 14.0906,
        'ok': {'J', 'JV'}
    },
    'Vogar': {
        'lon': 46.2946,
        'lan': 13.8755,
        'ok': {'JZ', 'J', 'JV'}
    },
    'Vogel': {
        'lon': 46.2518,
        'lan': 13.839,
        'ok': {'JV', 'V', 'SV'}
    },
    'Kranjska Gora': {
        'lon': 46.5044,
        'lan': 13.7954,
        'ok': {'J'}
    },
    'Ambrož pod Krvavcem': {
        'lon': 46.2752,
        'lan': 14.5279,
        'ok': {'JZ', 'J', 'JV'}
    },
    'Kriška gora': {
        'lon': 46.3515,
        'lan': 14.3332,
        'ok': {'JZ', 'J', 'JV'}
    },
    'Velika planina': {
        'lon': 46.2946,
        'lan': 14.6395,
        'ok': {'J', 'JV'}
    },
    'Mangrtsko Sedlo': {
        'lon': 46.4334,
        'lan': 13.6407,
        'ok': {'JZ', 'J', 'JV', 'V', 'Z'}
    },
    'Kobala': {
        'lon': 46.1806,
        'lan': 13.7791,
        'ok': {'JZ', 'J', 'JV', 'V', 'Z'}
    },
    'Kovk': {
        'lon': 45.8865,
        'lan': 13.9591,
        'ok': {'JZ', 'J', 'JV'}
    },
    'Kobariški Stol': {
        'lon': 46.2727,
        'lan': 13.4732,
        'ok': {'JZ', 'J', 'JV', 'V', 'Z'}
    },
    'Srednji vrh - Matajur': {
        'lon': 46.209,
        'lan': 13.5663,
        'ok': {'SV', 'S'}
    },
    'Kobariški Kuk - jug': {
        'lon': 46.1952,
        'lan': 13.6198,
        'ok': {'JZ', 'J', 'JV'}
    },
    'Lijak': {
        'lon': 45.9636,
        'lan': 13.7236,
        'ok': {'JZ', 'J', 'JV', 'V', 'Z'}
    },
    'Slivnica': {
        'lon': 45.7886,
        'lan': 14.4067,
        'ok': {'JZ', 'J', 'JV', 'Z'}
    },
    'Slivnica': {
        'lon': 45.7886,
        'lan': 14.4067,
        'ok': {'JZ', 'J', 'JV', 'Z'}
    },
    'Kamšak': {
        'lon': 46.3579,
        'lan': 15.259,
        'ok': {'JZ', 'J'}
    },
    'Konjiška gora': {
        'lon': 46.3347,
        'lan': 15.3466,
        'ok': {'JZ', 'J'}
    },
    'Mala Gora': {
        'lon': 46.3574,
        'lan': 15.3397,
        'ok': {'JZ', 'V', 'SV'}
    },
    'Malič': {
        'lon': 46.1822,
        'lan': 15.2056,
        'ok': {'J', 'JV'}
    },
    'Donačka gora': {
        'lon': 46.2616,
        'lan': 15.7313,
        'ok': {'JZ', 'J', 'JV'}
    },
    'Žusem': {
        'lon': 46.1519,
        'lan': 15.4909,
        'ok': {'V', 'SV', 'S'}
    },
    'Pohorje': {
        'lon': 46.5164,
        'lan': 15.58,
        'ok': {'SV', 'S', 'SZ'}
    },
    'Golte': {
        'lon': 46.3705,
        'lan': 14.9206,
        'ok': {'J', 'JV', 'V'}
    }
}
