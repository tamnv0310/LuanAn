'use-strict'
dist_list = {
    "q1": [10.780612857979111, 106.69929097226942, "Quận 1"],
    "q2": [10.783647660067732, 106.72673471144276, "Quận 2"],
    "q3": [10.782833128986498, 106.68617895544911, "Quận 3"],
    "q4": [10.766619604634025, 106.70496162697751, "Quận 4"],
    "q5": [10.755963008464605, 106.66749108555408, "Quận 5"],
    "q6": [10.746598181717706, 106.64917765698283, "Quận 6"],
    "q7": [10.73233643049728, 106.72664202853471, "Quận 7"],
    "q8": [10.740319883142194, 106.66541075067252, "Quận 8"],
    "q9": [10.83982108902878, 106.77095208740852, "Quận 9"],
    "q10": [10.767918838830244, 106.66659593804623, "Quận 10"],
    "q11": [10.763904275145594, 106.64342383825374, "Quận 11"],
    "q12": [10.86324605768756, 106.65438133369516, "Quận 12"],
    "qbthanh": [10.803446284783773, 106.69630236758046, "Quận Bình Thạnh"],
    "qbtan": [10.737193840613681, 106.61566486228712, "Quận Bình Tân"],
    "qgvap": [10.831931525946937, 106.66930567480965, "Quận Gò Vấp"],
    "qpnhuan": [10.795230097898482, 106.67533732496804, "Quận Phú Nhuận"],
    "qtbinh": [10.797934622453923, 106.64237067817248, "Quận Tân Bình"],
    "qtphu": [10.783538492749958, 106.63690663160116, "Quận Tân Phú"],
    "hbchanh": [10.689936987473937, 106.5841934376312, "Huyện Bình Chánh"],
    "hcgio": [10.411275219925006, 106.95473231899838, "Huyện Cần Giờ"],
    "hcchi": [10.973555815067174, 106.4938085691552, "Huyện Củ Chi"],
    "hhmon": [10.889499705704482, 106.59518769231617, "Huyện Hóc Môn"],
    "hnbe": [10.674384007461548, 106.73295641257327, "Huyện Nhà Bè"],
    "tptduc": [10.775752803095694, 106.7544347021429, "TP. Thủ Đức"],
}

var district_define = null;
var districtFeatures = [];
var markers = null;
var geojson = null;
var map = null;
var info = null;

const fillOpacityDefault = 1;

function initMap() {
    markers = L.layerGroup();

    for (var i in dist_list) {
        L.marker([dist_list[i][0], dist_list[i][1]]).bindPopup(dist_list[i][2]).addTo(markers);
    }

    var mbAttr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

    var grayscale = L.tileLayer(mbUrl, { id: 'mapbox/light-v9', tileSize: 512, zoomOffset: -1, attribution: mbAttr }),
        streets = L.tileLayer(mbUrl, { id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, attribution: mbAttr });

    var map = L.map('map', {
        center: [10.753286, 106.662586],
        zoom: 10,
        layers: [grayscale]
    });

    var baseLayers = {
        "Grayscale": grayscale,
        "Streets": streets
    };

    var district_markers = {
        "district_markers": markers
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
        var dist_name = (props&&props["name"])?dist_list[props["name"]][2] : "";
        this._div.innerHTML = '<h4>Thành phố Hồ Chí Minh</h4>' +
         (props ?'<p><b>' + dist_name + '</b></p><p><b>'+props.product+'</b><br/>' 
            + props.density + ' ' + props.unit +'</p><p style="text-align: right; margin-bottom: 0;"><i><small>'+props.date+'</small></i></p>'
            : '');
    };

    info.addTo(map);

    $.getJSON("static/data/hcm-district/district_define.json", function (data) {
        district_define = data;
    });

    $.getJSON("static/data/hcm-district/district_geo.json", function (data) {
        var _d = data["features"];
        for (var i in _d) {
            var k = _d[i]["properties"]["AdminID"];
            district_define[k]["geometry"] = _d[i]["geometry"];
        }

        console.log("District list define: ", district_define)
        for (const [key, value] of Object.entries(district_define)) {
            var _geo = {
                "type": "Feature",
                "properties": {
                    "name": value["distId"],
                    "date": "...",
                    "density": "...",
                    "unit": "µmol/㎡",
                    "product": "...",
                    "style": {
                        weight: 2.5,
                        dashArray: '3',
                        color: "#777",
                        opacity: 0.6,
                        fillColor: "#fff",
                        fillOpacity: fillOpacityDefault
                    },
                    "show_on_map": true
                },
                "geometry": {
                    "type": "MultiPolygon",
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
            fillOpacity: 1
        });
    
        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
    
        info.update(layer.feature.properties);
    }
    
    function resetHighlight(e) {
        // geojson.resetStyle(e.target);
        // info.update();
        var layer = e.target;
    
        layer.setStyle({
            weight: 1.25,
            dashArray: '3',
            fillOpacity: fillOpacityDefault
        });
    
    }
    
    function zoomToFeature(e) {
        console.log(e.target.getBounds())
        map.fitBounds(e.target.getBounds(), { padding: [20, 10] });
    }
}
