'use-strict'
item_list = {
    /*lat long: center distric to display icon*/
    "hcm": [10.7759, 106.7013, "Thành phố Hồ Chí Minh", "TP.HCM"],
    "binhduong": [11.3254, 106.4770, "Tỉnh Bình Dương", "Bình Dương"],
    "binhphuoc": [11.5473, 106.8832, "Tỉnh Bình Phước", "Bình Phước"],
    "dongnai": [11.0682, 107.1678, "Tỉnh Đồng Nai", "Đồng Nai"],
    "tayninh": [11.3352, 106.1099, "Tỉnh Tây Ninh", "Tây Ninh"],
    "vungtau": [10.5080, 107.1975, "Tỉnh Bà Rịa - Vũng Tàu", "Bà Rịa - Vũng Tàu"],
}

var province_define = null;
var provinceFeatures = [];
var districtFeatures = [];
var markers = null;
var geojson = null;
var map = null;
var info = null;

const fillOpacityDefault = 1;
const opacityDefault = 0.6;

function initMap() {
    markers = L.layerGroup();

    for (var i in item_list) {
        var icon = L.divIcon({
            iconSize:[150, 30],
            iconAnchor: [75, 30],/* width/2 */
            html:'<div class="map-label"><div class="map-label-content">'+item_list[i][3]+'</div></div>'
          });
        //(location, icon)
        // L.marker([dist_list[i][0], dist_list[i][1]], {icon: icon}).bindPopup(dist_list[i][2]).addTo(markers);
        L.marker([item_list[i][0], item_list[i][1]], {icon: icon}).addTo(markers);
    }

    var mbAttr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoidGFtdm4xNCIsImEiOiJjbG9vN283eHowMmQ2MmpxaXJ1ZTBtNHdpIn0.fL0XhDxrnTM7OJsAM-sw0A';

    var grayscale = L.tileLayer(mbUrl, { id: 'mapbox/light-v9', tileSize: 512, zoomOffset: -1, attribution: mbAttr }),
        streets = L.tileLayer(mbUrl, { id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, attribution: mbAttr });
        satellite = L.tileLayer(mbUrl, { id: 'mapbox/satellite-v9', tileSize: 512, zoomOffset: -1, attribution: mbAttr });

    map = L.map('map', {
        center: [11.10165037285805, 106.76075056221242],
        zoom: 9,
        layers: [grayscale],
    });

    map.attributionControl.setPosition('topright');

    var baseLayers = {
        "Grayscale": grayscale,
        "Satellite": satellite,
        "Streets": streets
    };

    var district_markers = {
        "Hiển thị tên địa điểm": markers
    };

    L.control.layers(baseLayers, district_markers).addTo(map);

    // control that shows state info on hover
    info = L.control();

    info.onAdd = function (map) {
        this._div = L.DomUtil.create('div', 'info');
        this.update();
        return this._div;
    };

    info.update = function (props) {
        debugger
        var dist_name = (props && props["name"]) ? item_list[props["name"]][2] : "";
        this._div.innerHTML = '<h4>Địa điểm</h4>' +
            (props ? '<p><b>' + dist_name + '</b></p><p>'
                +props.textType+ '<b><span class="circle color" style="background-color: ' + props.color + '"></span><span> ' + props.density + '</span></b> ' + props.unit + '</p><p style="text-align: right; margin-bottom: 0;"><i><small>' + props.date + '</small></i></p>'
                : '');
    };

    info.addTo(map);




    // // add text labels:
    // var loc = new L.LatLng(10.780612857979111,106.69929097226942);


    // var icon = L.divIcon({
    //     iconSize:null,
    //     html:'<div class="map-label"><div class="map-label-content">'+111222+'</div></div>'
    //   });

    // L.marker(loc,{icon: icon}).addTo(map);



    // var vietnam_define = null;
    // $.getJSON("static/data/province/vietnam_define.json", function (data) {
    //     vietnam_define = data;
    // });
    //
    // $.getJSON("static/data/province/vietnam.json", function (data) {
    //     var _province = data["features"];
    //     for (var i in _province) {
    //         var k = _province[i]["properties"]["slug"];
    //         //kiểm tra trong 63 tỉnh, tỉnh nào mình define thì mới them geometry vô
    //         if(vietnam_define[k]){
    //             var coordinates = _province[i]["geometry"]["coordinates"];
    //             var mergedCoordinates = [];
    //             for(var i in coordinates){
    //                 console.log(88899, coordinates[i][0]);
    //                 mergedCoordinates = mergedCoordinates.concat(coordinates[i][0])
    //             }
    //             console.log(999999, mergedCoordinates)
    //             vietnam_define[k]["geometry"] = {"coordinates": []};
    //             vietnam_define[k]["geometry"]["coordinates"].push(mergedCoordinates);
    //         }
    //     }
    //     debugger
    //     console.log("Vietnam tinh thanh list define: ", vietnam_define)
    //     for (const [key, value] of Object.entries(vietnam_define)) {
    //         var _geo = {
    //             "type": "Feature",
    //             "properties": {
    //                 "name": value["distId"],
    //                 "date": "...",
    //                 "textType": "...",
    //                 "density": "...",
    //                 "unit": "µmol/㎡",
    //                 "product": "...",
    //                 "alertMsg": "...",
    //                 "alertMsgColor": "#ffffff",
    //                 "color": "#fff",
    //                 "style": {
    //                     weight: 2.5,
    //                     dashArray: '3',
    //                     color: "#a6a6a6",
    //                     opacity: opacityDefault,
    //                     fillColor: "#a6a6a6",
    //                     fillOpacity: fillOpacityDefault
    //                 },
    //                 "show_on_map": true
    //             },
    //             "geometry": {
    //                 "type": "Polygon",
    //                 // "coordinates": [value["geometry"]["coordinates"]],
    //                "coordinates": [
    //                 [
    //                     [
    //                         106.58635813600004,
    //                         8.735319939000073
    //                     ],
    //                     [
    //                         106.58699194300009,
    //                         8.735887579000055
    //                     ],
    //                     [
    //                         106.587070345,
    //                         8.736490905000059
    //                     ],
    //                     [
    //                         106.58707298100003,
    //                         8.7371150770001
    //                     ],
    //                     [
    //                         106.58691776000008,
    //                         8.737479823000081
    //                     ],
    //                     [
    //                         106.58660532700007,
    //                         8.737741206000036
    //                     ],
    //                     [
    //                         106.58603073600005,
    //                         8.737795625
    //                     ],
    //                     [
    //                         106.58519421000003,
    //                         8.73769509500004
    //                     ],
    //                     [
    //                         106.58420069700006,
    //                         8.737543207000085
    //                     ],
    //                     [
    //                         106.583520494,
    //                         8.73733798600007
    //                     ],
    //                     [
    //                         106.58257770500006,
    //                         8.73682178300008
    //                     ],
    //                     [
    //                         106.58215812100008,
    //                         8.736459430000119
    //                     ],
    //                     [
    //                         106.58189574800005,
    //                         8.736200442
    //                     ],
    //                     [
    //                         106.5817773210001,
    //                         8.7359675630001
    //                     ],
    //                     [
    //                         106.58181442400007,
    //                         8.73564980500001
    //                     ],
    //                     [
    //                         106.58215329700003,
    //                         8.73531512600003
    //                     ],
    //                     [
    //                         106.58305786800001,
    //                         8.735145419000022
    //                     ],
    //                     [
    //                         106.58434691800008,
    //                         8.735045884000046
    //                     ],
    //                     [
    //                         106.58531627700009,
    //                         8.735033334000073
    //                     ],
    //                     [
    //                         106.58635813600004,
    //                         8.735319939000073
    //                     ]
    //                 ]
    //                 ]
    //             }
    //         }
    //         debugger
    //         provinceFeatures.push(_geo);
    //     }
    //
    //     geojson = L.geoJSON(provinceFeatures, {
    //         filter: function (feature, layer) {
    //             return feature.properties.show_on_map;
    //         },
    //         style: function (feature) {
    //             return feature.properties.style;
    //         },
    //         onEachFeature: onEachFeature
    //     }).bindPopup(function (layer) {
    //         return layer.feature.properties.popupContent;
    //     }).addTo(map);
    // });


    $.getJSON("static/data/province/province_define.json", function (data) {
        province_define = data;
    });

    $.getJSON("static/data/province/province_geo.json", function (data) {
        var _d = data["features"];
        for (var i in _d) {
            var k = _d[i]["properties"]["AdminID"];
            province_define[k]["geometry"] = _d[i]["geometry"];
        }

        console.log("District list define: ", province_define)
        for (const [key, value] of Object.entries(province_define)) {
            var _geo = {
                "type": "Feature",
                "properties": {
                    "name": value["distId"],
                    "date": "...",
                    "textType": "...",
                    "density": "...",
                    "unit": "℃",
                    "product": "...",
                    "color": "#fff",
                    "style": {
                        weight: 2.5,
                        dashArray: '3',
                        color: "#777777", //màu border
                        opacity: opacityDefault,
                        fillColor: "#a6a6a6", //mặc định là màu xám
                        fillOpacity: fillOpacityDefault
                    },
                    "show_on_map": true
                },
                "geometry": {
                    "type": "MultiPolygon",
                    // "coordinates": [value["geometry"]["coordinates"]],
                    "coordinates": [value["geometry"]["coordinates"]],
                }
            }
            districtFeatures.push(_geo);
        }

        geojson = L.geoJSON(districtFeatures, {
            filter: function (feature, layer) {
                return feature.properties.show_on_map;
            },
            style: function (feature) {
                return feature.properties.style;
            },
            onEachFeature: onEachFeature
        }).bindPopup(function (layer) {
            return layer.feature.properties.popupContent;
        }).addTo(map);
    });

    //Functions in init
    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: zoomToFeature
        });
    }

    function highlightFeature(e) {
        var layer = e.target;

        layer.setStyle({
            weight: 3,
            dashArray: '',
            opacity: 0.85,
            fillOpacity: 1
        });

        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }

        info.update(layer.feature.properties);

        $(".info.leaflet-control").toggleClass("show", true);
    }

    function resetHighlight(e) {
        // geojson.resetStyle(e.target);
        // info.update();
        var layer = e.target;

        layer.setStyle({
            weight: 1.25,
            dashArray: '3',
            fillOpacity: fillOpacityDefault,
            opacity: opacityDefault
        });
        info.update(null);
        $(".info.leaflet-control").toggleClass("show", false);
    }

    function zoomToFeature(e) {
        console.log("Zoom to: ", e.target.getBounds())
        map.fitBounds(e.target.getBounds(), { padding: [20, 10] });
    }
}
