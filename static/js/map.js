
var map_data = "/mapdata";

// reach data with D3
d3.json(map_data, function(data) {
  // Once we get a response, send the data.features object to the createFeatures function
  create_map(data);
  });


// create Function to create map
function create_map(response) {
    var map_data = response;
         

    var my_map = L.map("map", {
      center: [48, 65],
      zoom: 5
    });

    L.tileLayer(
        "https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?" +
        "access_token=pk.eyJ1Ijoic2luYW5jZW5naXoiLCJhIjoiY2ppZHVwMXZnMGZqaTNxcWw0NWxhN3YwNSJ9.RVV5UmzSmoeu4xd1Wh4iHA",{id: 'mapbox/satellite-v9'}
    ).addTo(my_map);
    my_map.touchZoom.disable();
    my_map.doubleClickZoom.disable();
    my_map.scrollWheelZoom.disable();
    
    var marker = L.marker([48, 65]).addTo(my_map);
    marker.bindPopup("Your City").openPopup();
    var marker = L.marker([51, 72]).addTo(my_map);
    marker.bindPopup("King Nursultan");
    var marker = L.marker([44, 52]).addTo(my_map);
    marker.bindPopup("King Tokayev");
    var marker = L.marker([43.5, 77.5]).addTo(my_map);
    marker.bindPopup("King of Almaty");
    var marker = L.marker([47, 52]).addTo(my_map);
    marker.bindPopup("King of Atyrau");
    var marker = L.marker([45, 66]).addTo(my_map);
    marker.bindPopup("King of Kizilorda");
    var marker = L.marker([50, 82]).addTo(my_map);
    marker.bindPopup("King of Oskemen");
    var marker = L.marker([50.22, 57]).addTo(my_map);
    marker.bindPopup("King of Aktobe");


   /* L.geoJSON(geo_json
    ).addTo(my_map);*/

    L.geoJSON(geo_json, {
        style: function(feature) {
            switch (feature.properties.side) {
                case 'Enemy': return {color: "red"};
                case 'Invaded':   return {color: "blue"};
            }
        }
    }).addTo(my_map);



  }