function initMap() {
    var dublin = {lat: 53.349805, lng: -6.26031};
    var map = new google.maps.Map(document.getElementById('map'), {
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

  .then((data) => {stations = data; StationPing()
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
        });
    });
}