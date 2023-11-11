let district_define = {};
$.getJSON("static/data/hcm-district/district_define.json", function (data) {
  district_define = data;
  console.log(data)
});

// Initialize and add the map
function initMap() {
    // The location of HCM 
    const hcm = { lat: 10.753286734865803, lng: 106.66258600458359 };
    // The map, centered at HCM
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: hcm,
        zoomControl: true,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,
        fullscreenControl: false,
        disableDefaultUI: true,
    });

    //polygon
    map.data.loadGeoJson('static/data/hcm-district/district_geo.json');
    // Color each letter gray. Change the color when the isColorful property
    // is set to true.
    map.data.setStyle(function (feature) {
        const color = district_define[feature.getProperty("AdminID")]["clr"];
        if (feature.getProperty('isColorful')) {
            color = 'violet';
        }
        return /** @type {!google.maps.Data.StyleOptions} */({
            fillColor: color,
            strokeColor: 'gray',
            strokeWeight: 1,
            fillOpacity: 0.7
        });
    });

    map.set("styles", [
        {
            stylers: [{ visibility: "off" }],
        },
        {
            featureType: "water",
            stylers: [{ visibility: "on" }, { color: "#d4d4d4" }],
        },
        {
            featureType: "landscape",
            stylers: [{ visibility: "on" }, { color: "#e5e3df" }],
        },
        {
            featureType: "administrative.country",
            elementType: "labels",
            stylers: [{ visibility: "on" }],
        },
        {
            featureType: "administrative.country",
            elementType: "geometry",
            stylers: [{ visibility: "on" }, { weight: 1.3 }],
        },
    ])

    // When the user clicks, set 'isColorful', changing the color of the letters.
    //clickable map
    var infowindow = new google.maps.InfoWindow();
    map.data.addListener('click', function (event) {
        // event.feature.setProperty('isColorful', true);
        // console.log("district geojson", event.feature.g.g[0].g)
        // console.log("lat: ", event.latLng.lat(), " lng: ", event.latLng.lng())
        const distName = district_define[event.feature.getProperty("AdminID")]["distName"];
        let html = '<b>' + distName + '</b>'; // combine state name with a label
        infowindow.setContent(html); // show the html variable in the infowindow
        infowindow.setPosition(event.latLng); // anchor the infowindow at the marker
        infowindow.setOptions({ pixelOffset: new google.maps.Size(0, -30) }); // move the infowindow up slightly to the top of the marker icon
        infowindow.open(map);
    });

    // When the user hovers, tempt them to click by outlining the letters.
    // Call revertStyle() to remove all overrides. This will use the style rules
    // defined in the function passed to setStyle()
    map.data.addListener('mouseover', function (event) {
        map.data.revertStyle();
        map.data.overrideStyle(event.feature, { strokeWeight: 1.4, fillOpacity: 0.8 });

    });

    map.data.addListener('mouseout', function (event) {
        map.data.revertStyle();
    });

    console.log(8888888, map.data)
}

//handle map marker
function handleMarker(e) {
    console.log("click handleMarker", e, e.latLng.toJSON(), "Name ===>", e.domEvent);
}