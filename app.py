import copy
import json
from datetime import datetime
from os.path import exists
import requests

from bs4 import BeautifulSoup
from flask import Flask, Response, redirect, request
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config

import server.apiUtil as apiUtil
import server.weatherManager as wm

# http://api.positionstack.com/v1/?access_key=ebecf82f61b08e636501c15807b3c2e1&query={site}&country=SI
# settings
pw_host = "0.0.0.0"
pw_port = 5001
pw_sitelistFileName = "sitelist.json"

# OWM setup
configDict = get_default_config()
configDict["language"] = "sl"
# disabling ssl sped up the lookup for weather from 23s to 12s
configDict["connection"]["use_ssl"] = False
owm = OWM('fccbb7f106f4603371910d9b192f519e',
          config=configDict).weather_manager()

app = Flask(__name__, static_url_path='/static')


# hardcoded list of sites, needed for more accurate jump point data and ugodni_veter (good_wind_direction) data
sites = {"Ambrož pod Krvavcem": {"lat": 46.2752, "lon": 14.5279},
         "Donačka gora": {"lat": 46.2616, "lon": 15.7313},
         "Golte": {"lat": 46.3705, "lon": 14.9206},
         "Gozd": {"lat": 46.3395, "lon": 14.3313},
         "Kamšak": {"lat": 46.3579, "lon": 15.259},
         "Kobala": {"lat": 46.1806, "lon": 13.7791},
         "Kobariški Kuk - jug": {"lat": 46.1952, "lon": 13.6198},
         "Kobariški Stol": {"lat": 46.2727, "lon": 13.4732},
         "Konjiška gora": {"lat": 46.3347, "lon": 15.3466},
         "Kovk": {"lat": 45.8865, "lon": 13.9591},
         "Kranjska Gora": {"lat": 46.5044, "lon": 13.7954},
         "Kriška gora": {"lat": 46.3515, "lon": 14.3332},
         "Lijak": {"lat": 45.9636, "lon": 13.7236},
         "Mala Gora": {"lat": 46.3574, "lon": 15.3397},
         "Malič": {"lat": 46.1822, "lon": 15.2056},
         "Mangrt": {"lat": 46.4334, "lon": 13.6407},
         "Pohorje": {"lat": 46.5164, "lon": 15.58},
         "Ratitovec": {"lat": 46.2361, "lon": 14.0906},
         "Slivnica": {"lat": 45.7886, "lon": 14.4067},
         "Srednji vrh (Matajur)": {"lat": 46.209, "lon": 13.5663},
         "Velika planina": {"lat": 46.2946, "lon": 14.6395},
         "Vogar": {"lat": 46.2946, "lon": 13.8755},
         "Vogel": {"lat": 46.2518, "lon": 13.839},
         "Zavrh": {"lat": 45.903366, "lon": 14.353807},
         "Žusem": {"lat": 46.1519, "lon": 15.4909}}

# TODO: email notification for new site detected, so that i can manually add good wind? (i dont know how to get it automatically)
#       oh, and the api for location can offer you multiple locations, so its better to add (or verify) each one manually
#       or the api can offer you MULTIPLE LOCATIONS with NO DATA IN THEM (not even any data about what you requested from it), it was literally a list of empty lists, wtf?????


# autosetup code

def getRawFromAPI():
    url = "http://skytech.si/skytechsys/data.php"
    reqBody = {"c": "tabela"}
    rawReq = requests.post(url=url, data=reqBody)
    return rawReq.text


def getPointsFromAPI():
    # POST request
    url = "http://skytech.si/skytechsys/data.php"
    reqBody = {"c": "tabela"}
    rawReq = requests.post(url=url, data=reqBody)

    # parse html response, filter for site names, convert to strings and sort
    skytech = BeautifulSoup(rawReq.text, features="html.parser")
    lines = skytech.findAll("a", attrs={"id": "postaja-link"})
    linesText = [line.string for line in lines]
    linesText.sort()

    return linesText


def regenerateFile():
    with open(pw_sitelistFileName, "w") as f:
        global sites
        availabileSites = getPointsFromAPI()
        newSites = {}
        # remove all points that dont exist anymore
        for site in availabileSites:
            if site in sites:
                newSites[site] = sites[site]

        # get all new sites
        notinHardcodedSites = [site for site in availabileSites if site not in list(
            newSites.keys())]

        # get data for all new sites
        for site in notinHardcodedSites:
            url = f"http://api.positionstack.com/v1/forward?access_key=ebecf82f61b08e636501c15807b3c2e1&query={site}&country=SI"
            resp = requests.get(url)
            jsonified = resp.json()
            data = jsonified["data"]
            if len(data) > 0:
                # print(resp)
                if data[0] != []:
                    data = data[0]
                    new = {}
                    new["lon"] = data["longitude"]
                    new["lat"] = data["latitude"]
                    new["ok"] = []
                    newSites[site] = new
        f.write(json.dumps(newSites))
        f.close()
        sites = newSites | sites
        return


if not exists(pw_sitelistFileName):
    print(
        f"[WARNING] {pw_sitelistFileName} doesn't exist, recreating (takes ~60s)...")
    regenerateFile()
else:
    with open(pw_sitelistFileName, "r") as f:
        sites = json.loads(f.read())


# Flask code

@app.route("/list")
def getList():
    return Response(json.dumps(sites), mimetype="application/json")


@app.route('/full')
def allData():
    global sites
    tempSites = copy.deepcopy(sites)
    parsed = BeautifulSoup(getRawFromAPI(), features="html.parser")
    allRows = parsed.find_all("tr")
    for row in allRows:
        child = row.findChildren("td")
        siteData = []
        for c in child:
            # c.text == each cell of a row (1 row/<tr> is one jumpsite)
            siteData.append(c.text)
        # siteData = [name, wind speed, wind gust, wind direction, temperature, time and date of measurement]
        if not len(siteData) == 0:
            # filter out missing stations that we couldn't find location data for
            if siteData[0] in tempSites.keys():
                # copy already existing data
                temp = tempSites[siteData[0]]

                # add data from skytech
                temp["windSpeed"] = float(siteData[1].replace(" m/s", ""))
                temp["windGust"] = float(siteData[2].replace(" m/s", ""))
                temp["windDirection"] = siteData[3]
                temp["temperature"] = float(siteData[4].replace("°C", ""))
                temp["timeAndDate"] = str(
                    datetime.strptime(siteData[5], "%H:%M %d.%m.%Y"))

                # add data from manager
                observation = owm.weather_at_coords(lat=temp["lat"], lon=temp["lon"])
                temp["weather"] = observation.weather.status
                temp["detailedWeather"] = observation.weather.detailed_status

                tempSites[siteData[0]] = temp

    return Response(json.dumps(tempSites), mimetype="application/json")


@ app.route('/')
def hello():
    return redirect("static/index.html", code=302)


# app.run(host, port, debug)
# host - Hostname to listen on
# port - Default 5000
# debug - True if you want to use the flask debugger (hot reloads, debugging checkpoints)
if __name__ == "__main__":
    # for dev only
    xd = getPointsFromAPI()
    print("Link so that you can use geolocation: http://localhost:5001")

    # production
    app.run(pw_host, port=pw_port, debug=True)
    # TODO: generate certificate
