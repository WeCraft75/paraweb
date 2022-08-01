// FILL LIST OF MOCK FLIGHT POINTS
var jumpPointsList = null;
var leaflet = window.L;
var onlyOneMatchedBefore = false;
var map = leaflet.map("mapid", { doubleClickZoom: false }).locate({ setView: true, maxZoom: 12 });
leaflet.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);


function fillList() {
  var sitelist = document.getElementById("sitelist");
  Object.keys(jumpPointsList).sort().forEach((name) => {
    var point = document.createElement("div");
    point.className = "jumppoint";
    var foggy = ["Mist", "Fog", "Haze", "Smoke"];
    var iconName = "cloud-off";
    switch (jumpPointsList[name]["weather"]) {
      case "Clouds":
        iconName = "cloud";
        break;
      case "Rain":
        iconName = "cloud-rain";
        break;
      case "Thunderstorm":
        iconName = "cloud-lightning";
        break;
      case "Clear":
        iconName = "sun";
        break;
      case "Snow":
        iconName = "cloud-snow";
        break;
      case "Drizzle":
        iconName = "cloud-drizzle";
        break;
      default:
        if (foggy.includes(jumpPointsList[name]["weather"])) {
          iconName = "menu";
        }
    }
    point.innerHTML = `${name} <div data-feather="${iconName}" class="weathericon"></div>`;
    point.setAttribute("name", name);
    point.setAttribute("onclick", "zoomOnPoint(this)");
    // TODO: this is only text, it would be better to translate this info into an infographic style format
    sitelist.appendChild(point);
  });
}

function zoomOnPoint(toFind) {
  Object.keys(jumpPointsList).forEach((name) => {
    if (toFind.getAttribute("name") == name) {
      var point = jumpPointsList[name];
      map.flyTo([point.lon, point.lat], 14);
    }
  });
}

function addPoints() {
  Object.keys(jumpPointsList).forEach((name) => {
    var singlepoint = jumpPointsList[name];
    var text = `<div class="popupheader">${name}</div>`;
    // check if the jumppoint data contains all the info required to display in the popup
    if (Object.keys(singlepoint).length > 2) {
      // add info to popup
      var slovenianWindDir = singlepoint["windDirection"].replace("S", "J").replace("E", "V").replace("W", "Z").replace("N", "S");
      text += `Veter piha v smeri ${slovenianWindDir} s hitrostjo ${singlepoint["windSpeed"]} m/s, ter sunki do ${singlepoint["windGust"]} m/s`;
      text += `<br/>Temperatura na vzletišču: ${singlepoint["temperature"]}°C`;
      text += `<br/>Trenutno vreme: ${singlepoint["detailedWeather"]}`;

    } else {
      text += "<br/>Podatkov ni bilo mogoče pridobiti."
    }

    var x = jumpPointsList[name].lat;
    var y = jumpPointsList[name].lon;

    // create weather info popup
    // TODO: make it pretty
    leaflet.marker([x, y]).addTo(map).bindPopup(`${text}`);
  });
}

function setMapToUserLocation(e) {
  var radius = e.accuracy;
  if (radius > 2000) {
    // filter for inaccurate location search
    defaultMapDisplay();
    return;
  }
  leaflet
    .marker(e.latlng)
    .addTo(map)
    .bindPopup(`Vaša lokacija z natančnostjo na ${radius.toFixed(2)}m`);

  leaflet
    .circle(e.latlng, radius, { color: "#ff2919", opacity: "0.4" })
    .addTo(map);
}

function defaultMapDisplay() {
  //default to geographical center of Slovenia, zoom to fit whole country
  map.setView([46.119944, 14.815333], 9);
}

function getPoints() {
  var jumpPointsFromAPI = {}
  try {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", `${window.location.origin}/list`, false);
    xmlHttp.send(null);
    jumpPointsFromAPI = JSON.parse(xmlHttp.responseText);
  } catch (e) {
    console.error(e)
  }
  if (jumpPointsFromAPI != {}) {
    jumpPointsList = jumpPointsFromAPI;
  }
  else {
    alert("There was an error loading the list of jump points.");
  }
}

async function getWeatherForPoint(jumpPointName) {
  return new Promise(resolve => {
    var response = {};
    try {
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open("GET", `${window.location.origin}/data?jumpPoint=${jumpPointName}`, false);
      xmlHttp.send(null);
      response = xmlHttp;
    } catch (e) {
      console.error(e)
    }
    if (response.status == 200) {
      response = JSON.parse(xmlHttp.responseText);
    } else {
      response = {};
    }
    resolve(response)
  });
}

async function getWeather(callback) {
  var pointlist = Object.keys(jumpPointsList);
  for (let i = 0; i < pointlist.length; i++) {
    let dataForPoint = await getWeatherForPoint(pointlist[i]);
    Object.keys(dataForPoint).forEach((key) => {
      jumpPointsList[pointlist[i]][key] = dataForPoint[key];
      jumpPointsList[pointlist[i]]["timeAndDate"] = Date.parse(pointlist[i]["timeAndDate"]);
    });
  }
  callback();
}

function getAllData() {
  var jumpPointsFromAPI = {}
  try {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", `${window.location.origin}/full`, false);
    xmlHttp.send(null);
    jumpPointsFromAPI = JSON.parse(xmlHttp.responseText);
  } catch (e) {
    console.error(e)
  }
  if (jumpPointsFromAPI != {}) {
    jumpPointsList = jumpPointsFromAPI;
  }
  else {
    alert("There was an error loading jump point data.");
  }
}

var afterWeather = () => {
  fillList();
  addPoints();
  // feather icon integration
  feather.replace();
}

/*  LEGACY
// Load app info
getPoints();
getWeather(afterWeather);

*/

// Load site info
getAllData()
//console.log(jumpPointsList)
afterWeather()

// Set event listeners
map.on("locationfound", setMapToUserLocation);
map.on("locationerror", defaultMapDisplay);

// Searchbar filter for sites
function searchElements(inputElement) {
  var toFind = inputElement.value;
  var jumpPoints = document.getElementsByClassName("jumppoint");
  var matching = [];
  // if we find a matching part (of the word), display="", else display="none"
  for (let i = 0; i < jumpPoints.length; i++) {
    var current = jumpPoints[i].getAttribute("name");
    if (current.toLowerCase().indexOf(toFind) > -1) {
      jumpPoints[i].setAttribute("style", "");
      matching.push(jumpPoints[i]);
    }
    else {
      jumpPoints[i].setAttribute("style", "display:none");
    }
  }
  // if we matched exactly one and we didnt before, zoom on that point
  if (matching.length == 1 && !onlyOneMatchedBefore) {
    onlyOneMatchedBefore = true;
    zoomOnPoint(matching[0]);
  }
  // else if we matched more than one, reset matchingBefore
  // do not reset if none matching, or if previously matched 0,
  // this will zoom on point for each letter (zoom only once/dont if we already matched)
  else if (matching.length > 1) {
    onlyOneMatchedBefore = false;
  }
  // if we matched exactly one and we didnt before, zoom on that point
  if (matching.length == 1 && !onlyOneMatchedBefore) {
    onlyOneMatchedBefore = true;
    zoomOnPoint(matching[0]);
  }
  // else if we matched more than one, reset matchingBefore
  // do not reset if none matching, or if previously matched 0,
  // this will zoom on point for each letter (zoom only once/dont if we already matched)
  else if (matching.length > 1) {
    onlyOneMatchedBefore = false;
  }
}
