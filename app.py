import copy
import json
from datetime import datetime
from os.path import exists

import requests
from bs4 import BeautifulSoup
from flask import Flask, Response, redirect, request

import server.apiUtil as apiUtil
import server.weatherManager as wm

# http://api.positionstack.com/v1/?access_key=ebecf82f61b08e636501c15807b3c2e1&query={site}&country=SI
# settings
pw_host = "0.0.0.0"
pw_port = 5001
pw_sitelistFileName = "sitelist.json"


app = Flask(__name__, static_url_path='/static')


# hardcoded list of sites, needed for more accurate jump point data and ugodni_veter (good_wind_direction) data
sites = {
    "Gozd": {
        "lon": 46.3395,
        "lat": 14.3313,
        "ok": ["JZ", "J", "JV"]
    },
    "Ratitovec": {
        "lon": 46.2361,
        "lat": 14.0906,
        "ok": ["J", "JV"]
    },
    "Vogar": {
        "lon": 46.2946,
        "lat": 13.8755,
        "ok": ["JZ", "J", "JV"]
    },
    "Vogel": {
        "lon": 46.2518,
        "lat": 13.839,
        "ok": ["JV", "V", "SV"]
    },
    "Kranjska Gora": {
        "lon": 46.5044,
        "lat": 13.7954,
        "ok": ["J"]
    },
    "Ambrož pod Krvavcem": {
        "lon": 46.2752,
        "lat": 14.5279,
        "ok": ["JZ", "J", "JV"]
    },
    "Kriška gora": {
        "lon": 46.3515,
        "lat": 14.3332,
        "ok": ["JZ", "J", "JV"]
    },
    "Velika planina": {
        "lon": 46.2946,
        "lat": 14.6395,
        "ok": ["J", "JV"]
    },
    "Mangrt": {
        "lon": 46.4334,
        "lat": 13.6407,
        "ok": ["JZ", "J", "JV", "V", "Z"]
    },
    "Kobala": {
        "lon": 46.1806,
        "lat": 13.7791,
        "ok": ["JZ", "J", "JV", "V", "Z"]
    },
    "Kovk": {
        "lon": 45.8865,
        "lat": 13.9591,
        "ok": ["JZ", "J", "JV"]
    },
    "Kobariški Stol": {
        "lon": 46.2727,
        "lat": 13.4732,
        "ok": ["JZ", "J", "JV", "V", "Z"]
    },
    "Srednji vrh (Matajur)": {
        "lon": 46.209,
        "lat": 13.5663,
        "ok": ["SV", "S"]
    },
    "Kobariški Kuk - jug": {
        "lon": 46.1952,
        "lat": 13.6198,
        "ok": ["JZ", "J", "JV"]
    },
    "Lijak": {
        "lon": 45.9636,
        "lat": 13.7236,
        "ok": ["JZ", "J", "JV", "V", "Z"]
    },
    "Slivnica": {
        "lon": 45.7886,
        "lat": 14.4067,
        "ok": ["JZ", "J", "JV", "Z"]
    },
    "Slivnica": {
        "lon": 45.7886,
        "lat": 14.4067,
        "ok": ["JZ", "J", "JV", "Z"]
    },
    "Kamšak": {
        "lon": 46.3579,
        "lat": 15.259,
        "ok": ["JZ", "J"]
    },
    "Konjiška gora": {
        "lon": 46.3347,
        "lat": 15.3466,
        "ok": ["JZ", "J"]
    },
    "Mala Gora": {
        "lon": 46.3574,
        "lat": 15.3397,
        "ok": ["JZ", "V", "SV"]
    },
    "Malič": {
        "lon": 46.1822,
        "lat": 15.2056,
        "ok": ["J", "JV"]
    },
    "Donačka gora": {
        "lon": 46.2616,
        "lat": 15.7313,
        "ok": ["JZ", "J", "JV"]
    },
    "Žusem": {
        "lon": 46.1519,
        "lat": 15.4909,
        "ok": ["V", "SV", "S"]
    },
    "Pohorje": {
        "lon": 46.5164,
        "lat": 15.58,
        "ok": ["SV", "S", "SZ"]
    },
    "Golte": {
        "lon": 46.3705,
        "lat": 14.9206,
        "ok": ["J", "JV", "V"]
    },
    "Golte": {
        "lon": 46.3705,
        "lat": 14.9206,
        "ok": ["J", "JV", "V"]
    },
    "Zavrh": {
        "lon": 45.903366,
        "lat": 14.353807,
        "ok": []
    }
}

# TODO: email notification for new site detected, so that i can manually add good wind? (i dont know how to get it automatically)
#       oh, and the api for location can offer you multiple locations, so its better to add (or verify) each one manually


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
            if len(data) != 0:
                # print(resp)
                if data[0] != []:
                    data = data[0]
                    new = {}
                    # lat and lon is switched around bc when they were creating the original "sites" dict, they did a fucking boo boo :(
                    # TODO: fuck... fucking fuck, why ;_; ... i will make a program that fixes this no way i'm doing it manually
                    new["lon"] = data["latitude"]
                    new["lat"] = data["longitude"]
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
    # returns sites dict without good wind ("ok")
    sitelist = {}
    for name in sites.keys():
        filtered = {}
        filtered["lat"] = sites[name].get("lat")
        filtered["lon"] = sites[name].get("lon")
        sitelist[name] = filtered
    return Response(json.dumps(sitelist), mimetype="application/json")


@app.route("/data")
def getData():
    # returns data for given name
    name = request.args["jumpPoint"]
    if name not in sites.keys():
        return {"error": "pointNotFound", "message": "Jump point requested was not found"}, 404

    args = sites.get(name)
    util = apiUtil.start(name, args["lon"], args["lat"], args["ok"])
    jumpPointData = {
        "windSpeed": util.getWindSpeed(),
        "windGust": util.getWindGust(),
        "windDirection": util.getWindDirection(),
        "temperature": util.getTemperature(),
        "timeAndDate": util.getTimestamp(),
        "isWindGood": util.isWindGood(),
        "weather": util.getWeather(),
        "detailedWeather": util.getDetailedWeather(),
        "humidity": util.getHumidity(),
        "pressure": util.getPressure()
    }
    return Response(json.dumps(jumpPointData), mimetype="application/json")


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
            # c.text == each cell of a row (which is one jumpsite)
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
                weatherAPI = wm.manager(temp["lat"], temp["lon"])
                temp["weather"] = weatherAPI.getWeather()
                temp["detailedWeather"] = weatherAPI.getDetailedWeather()
                temp["humidity"] = weatherAPI.getHumidity()
                temp["pressure"] = weatherAPI.getPressure()["press"]
                tempSites[siteData[0]] = temp

    # print(tempSites)
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
