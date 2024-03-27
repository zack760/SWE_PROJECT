let map;
let markers = []

function initMap() {
    var dublin = {lat: 53.349805, lng: -6.26031};
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: dublin
    });
}




fetch("data.json")
  .then((response) => {
    console.log(response);
    if (!response.ok) {
      if (response.status >= 400 && response.status < 500) {
        console.error("Client-side error");
      } else if (response.status >= 500) {
        console.error("Server-side error");
      }
    }

    return response.json();
  })

  .then((data) => {
    stations = data; 
    initMap(); 
    StationPing();
  })

  .catch((error) => console.error("Network error: ", error));

function StationPing() {
    stations.forEach(station => {
        var marker = new google.maps.Marker({
            position: {
                lat: station.position_lat,
                lng: station.position_lng,
            },
            map: map,
            title: station.name,
            station_number: station.number,
            icon: {
              url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
              scaledSize: new google.maps.Size(30,30),
            },
        });
      
        markers.push(marker);
        marker.addListener("click", function() {
          var infoWindow = new google.maps.InfoWindow({
            content: "Station Name: " + station.name + '<br>' + "Station Number: " + station.number
          });
          infoWindow.open(map, marker);
        });

    });
}

function findRoute() {
  var start = document.getElementById("start").value;
  var end = document.getElementById("end").value;

  var directionsService = new google.maps.DirectionsService();
  var directionsDisplay = new google.maps.DirectionsRenderer();
  var polyline = new google.maps.Polyline({
    path: [],
    geodesic: true,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 2
  })

  directionsDisplay.setMap(map); 

  removeMarkers();

  var request = {
    origin: start,
    destination: end, 
    // travelMode: "BICYCLING"
    travelMode: "DRIVING"
  };

  directionsService.route(request, function(result, status) {
    if (status == "OK") {
      directionsDisplay.setDirections(result);
      var route = result.routes[0].overview_path;
      for (var i = 0; i < route.length; i++) {
        polyline.getPath().push(route[i]);
      }
      polyline.setMap(map);
  
    } else {
      console.error("Directions request failed due to " + status);
    }
  });
}

function removeMarkers() {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
}

function findClosestStation(address) {
  var geocoder = new google.maps.Geocoder();
  geocoder.geocode({ address: address }, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      var location = results[0].geometry.location;
      var closestStation;
      var minDistance = Infinity;
      var closestStation = null;

      stations.forEach(station => {
        var stationLocation = new google.maps.LatLng(station.position_lat, station.position_lng);
        var distance = google.maps.geometry.spherical.computeDistanceBetween(location, stationLocation);
        if (distance < minDistance) {
          minDistance = distance;
          closestStation = station;
        }
      });  
      console.log("Nearest station: ", closestStation);
    } else {
      console.error("Geocoding failed due to: " + status);
    }
  });
}

function findBestRoute(A, B) {
  var directionsService = new google.maps.DirectionsService();
  var directionsDisplay = new google.maps.DirectionsRenderer();

  directionsDisplay.setMap(map);

  var request = {
    origin: A,
    destination: B,
    travelMode: "BICYCLING"
  };

  directionsService.route(request, function(result, status) {
    if (status == "OK") {
      directionsDisplay.setDirections(result);
    
      var stationA = findClosestStation(A);
      var stationB = findClosestStation(B);

      drawRoute(A, stationA, "#FF0000");
      drawRoute(B, stationB, "#0000FF");

    } else {
      console.error("Directions request failed due to " + status);
    }
  });
}

function drawRoute(origin, dest, color) {
  var request = {
    origin: origin,
    destination: dest,
    travelMode: "BICYCLING"
  };

  var directionsService = new google.maps.DirectionsService();
  directionsService.route(request, function(result, status) { 
    if (status == "OK") {
      var DirectionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
        directions: result,
        polylineOptions: {
          strokeColor: color,
          strokeOpacity: 1.0,
          strokeWeight: 4
        }
      });
    } else {
      console.error("Directions request failed due to " + status)
    }
  })
}