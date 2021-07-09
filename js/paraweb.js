// FILL LIST OF MOCK FLIGHT POINTS
var jumpPointsList = null;
var leaflet = window.L;
var map = leaflet.map("mapid", { doubleClickZoom: false }).locate({ setView: true, maxZoom: 12 });
leaflet.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);


function fillList() {
  var sitelist = document.getElementById("sitelist");
  Object.keys(jumpPointsList).forEach((name) => {
    var point = document.createElement("div");
    point.className = "jumppoint";
    point.innerHTML = name;
    point.setAttribute("name", name.toLowerCase());
    point.setAttribute("onclick", "zoomOnPoint(this)");
    // TODO: this is only text, make it remotely beautiful
    sitelist.appendChild(point);
  });
}

function zoomOnPoint(toFind) {
  Object.keys(jumpPointsList).forEach((name) => {
    if (toFind.getAttribute("name") == name.toLowerCase()) {
      var point = jumpPointsList[name];
      map.flyTo([point.lon, point.lat], 14);
    }
  });
}

function addPoints() {
  Object.keys(jumpPointsList).forEach((name) => {
    var pointName = name;
    var x = jumpPointsList[name].lon;
    var y = jumpPointsList[name].lat;

    // create weather info popup
    // TODO make it pretty
    leaflet.marker([x, y]).addTo(map).bindPopup(`${pointName}`);
  });
}

function setMapToUserLocation(e) {
  var radius = e.accuracy;
  leaflet
    .marker(e.latlng)
    .addTo(map)
    .bindPopup(`Your location within a ${radius}m radius`);

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
    xmlHttp.open("GET", "http://192.168.1.95:5000/list", false);
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

// Load app info
getPoints();
addPoints();
fillList();

var feather = (function () {
  // feather icon integration
  feather.replace();
})();

// Set event listeners
map.on("locationfound", setMapToUserLocation);
map.on("locationerror", defaultMapDisplay);

// Searchbar filter sites
function searchElements(inputElement) {
  var toFind = inputElement.value;
  var jumpPoints = document.getElementsByClassName("jumppoint");
  var matching = [];
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
  if (matching.length == 1) {
    zoomOnPoint(matching[0]);
  }
}
