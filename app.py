import server.apiUtil as apiUtil
from flask import Flask, request, redirect
import json
import requests
from bs4 import BeautifulSoup
from os.path import exists

# http://api.positionstack.com/v1/?access_key=ebecf82f61b08e636501c15807b3c2e1&query='{site} Slovenija'
# settings
pw_host = "0.0.0.0"
pw_port = 5001
pw_sitelistFileName = "sitelist.json"


app = Flask(__name__, static_url_path='/static')


# hardcoded list of sites, could get list from scraping
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
    }
}

# TODO: if we encounter a new jump site, add it to the file with coordinates attached
#       coordinates should be pulled from an api, such as https://positionstack.com
# TODO: remove old sites from file
# TODO: email notification for good wind? (i dont know how to get it automatically)

# autosetup code


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
        availabileSites = getPointsFromAPI()
        newSites = {}
        # remove all points that dont exist anymore
        for site in availabileSites:
            if site in sites:
                newSites[site] = sites[site]

        # get all new sites
        notinSites = [site for site in availabileSites if site not in list(
            newSites.keys())]

        # get data for all new sites
        for site in notinSites:
            url = f"http://api.positionstack.com/v1/forward?access_key=ebecf82f61b08e636501c15807b3c2e1&query={site}&country=SI"
            resp = requests.get(url).json()["data"]
            if len(resp) != 0:
                resp = resp[0]
                new = {}
                new["lon"] = resp["longitude"]
                new["lat"] = resp["latitude"]
                newSites[site] = new
        f.write(json.dumps(newSites))
        f.close()
        return


def addPointToFile(jumpPointName):

    return


if not exists(pw_sitelistFileName):
    print("[WARNING] sitelist.json doesn't exist, recreating...")
    regenerateFile()


# Flask


@app.route("/list")
def getList():
    list = {}
    for name in sites.keys():
        filtered = {}
        filtered["lat"] = sites[name].get("lat")
        filtered["lon"] = sites[name].get("lon")
        list[name] = filtered
        # returns sites dict without good wind ("ok")
    return json.dumps(list)


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
    return json.dumps(jumpPointData)


@app.route('/full')
def allData():
    # check if point is not in file
    return ""


@app.route('/')
def hello():
    return redirect("static/index.html", code=302)


# app.run(host, port, debug)
# host - Hostname to listen on
# port - Default 5000
# debug - True if you want to use the flask debugger (hot reloads, debug server)
if __name__ == "__main__":
    # for dev only
    xd = getPointsFromAPI()
    print("Link so that you can use geolocation: http://localhost:5001")
    # production
    app.run(pw_host, port=pw_port, debug=True)
    # TODO: generate certificate
