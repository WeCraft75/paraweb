// FILL LIST OF MOCK FLIGHT POINTS
var jumpPointsList = null;
var leaflet = window.L;
var map = leaflet
  .map("mapid", { doubleClickZoom: false })
  .locate({ setView: true, maxZoom: 12 });

leaflet.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

function fillList() {
  var flightPointList = document.getElementById("flightList");
  jumpPointsObjectsMock.forEach((element) => {
    /* 
    Create structure from the following template:
      <li class="nav-item">
          <a class="nav-link">
              <span data-feather="${ICON}"></span>
              ${vzletisce}
          </a>
      </li>
    */
    var li = document.createElement("li");
    var a = document.createElement("a");
    var span = document.createElement("span");
    li.setAttribute("class", "nav-item");
    a.setAttribute("class", "nav-link");
    a.setAttribute("onclick", "zoomOnPoint(this.name)");
    a.setAttribute("name", element.name);

    span.setAttribute("data-feather", "cloud-off");
    a.appendChild(span);
    a.innerHTML += "\n" + element.name;
    li.appendChild(a);
    flightPointList.appendChild(li);
  });
}

function zoomOnPoint(name) {
  jumpPointsObjectsMock.forEach((element) => {
    if (name === element.name) {
      map.flyTo([element.x, element.y], 14);
    }
  });
}

function addPoints() {
  Object.keys(jumpPointsList).forEach((name) => {
    var pointName = name;
    var x = jumpPointsList[name].lon;
    var y = jumpPointsList[name].lat;
    console.log(`${pointName} ${x} ${y} ${typeof (y)}`);

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
    .addTo(map)
    .bindPopup(`Your location within a ${radius}m radius`);
}

function defaultMapDisplay() {
  //default to geographical center of Slovenia, zoom to fit whole country
  map.setView([46.119944, 14.815333], 9);
}

function getPoints() {
  var jumpPoints = {}
  try {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "http://192.168.1.95:5000/list", false);
    xmlHttp.send(null);
    jumpPoints = JSON.parse(xmlHttp.responseText);
  } catch (e) {
    console.error(e)
  }
  if (jumpPoints != {}) {
    //we got the jump points
    console.log(jumpPoints);
    jumpPointsList = jumpPoints;
  }
}

// Load app info
getPoints();
addPoints();
//fillList();

var feather = (function () {
  // feather icon integration
  feather.replace();
})();

// Set event listeners
map.on("locationfound", setMapToUserLocation);
map.on("locationerror", defaultMapDisplay);

// Searcbar filter sites
function searchElements() {
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById("srchbar");
  filter = input.value.toUpperCase();
  ul = document.getElementById("flightList");
  li = ul.getElementsByTagName("li");
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("a")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}
