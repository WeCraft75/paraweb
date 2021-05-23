// FILL LIST OF MOCK FLIGHT POINTS
var jumpPointsObjectsMock = [];
var leaflet = window.L;
var map = leaflet
  .map("mapid", { doubleClickZoom: false })
  .locate({ setView: true, maxZoom: 12 });

leaflet
  .tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png")
  .addTo(map);

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
  jumpPointsObjectsMock.forEach((element) => {
    var pointName = element.name;
    var x = element.x;
    var y = element.y;

    // create popup
    // TODO make a pretty weather popup
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
  /*
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", "http://wecraft75.ddns.net:5000/list", false);
  xmlHttp.send(null);
  var jumpPoints = JSON.parse(xmlHttp.responseText);
  console.log(jumpPoints);
  */

  for (let i = 0; i < 3; i++) {
    const element = {
      name: `test ${i}`,
      x: 45.8861046 + i / 100,
      y: 13.9599347 + i / 100
    };
    jumpPointsObjectsMock.push(element);
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

// Search list elements
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
