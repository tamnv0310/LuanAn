'use-strict'
//@prepros-prepend 'inc/main-map.js';

const weekday = new Array(7);
weekday[0] = "Chủ nhật";
weekday[1] = "Thứ hai";
weekday[2] = "Thứ ba";
weekday[3] = "Thứ tư";
weekday[4] = "Thứ năm";
weekday[5] = "Thứ sáu";
weekday[6] = "Thứ bảy";

//colorCodeRange: low to high
// const colorCodeRange = ['#3776bf', '#a7c6ed', '#40bdb1', '#e0da69', '#e1c63b', '#df7a4c', '#d14673', '#aa335c', '#631417', '#46080b', '#2b0002']
// const colorCodeRange = ['#3da570', '#44c359', '#55e93a', '#e0da69', '#e1c63b', '#df7a4c', '#d14673', '#aa335c', '#631417', '#46080b', '#2b0002']
const colorCodeRange = ["#739f1d", "#557e02", "#4c6e06", "#ffcc01", "#ff9900", "#ff6601", "#cc3300", "#cc0032", "#990033", "#d10000", "#f30101"];
// const colorrange = {
//   "no2": [
//     {
//       limit: 0,
//       color: "#293e56"/*dark*/
//     },
//     {
//       limit: 30,
//       color: "#8195ff"/*blue*/
//     },
//     {
//       limit: 60,
//       color: "purple"
//     },
//     {
//       limit: 90,
//       color: "#57c7c7"
//     },
//     {
//       limit: 120,
//       color: "green"
//     },
//     {
//       limit: 150,
//       color: "#d5cc3e"/*yellow*/
//     },
//     {
//       limit: 200,
//       color: "#cd4d42"/*red*/
//     }
//   ], "so2": [
//     {
//       limit: 0,
//       color: "#293e56"/*dark*/
//     },
//     {
//       limit: 1000,
//       color: "#8195ff"/*blue*/
//     },
//     {
//       limit: 2500,
//       color: "purple"
//     },
//     {
//       limit: 4000,
//       color: "#57c7c7"
//     },
//     {
//       limit: 5500,
//       color: "green"
//     },
//     {
//       limit: 6000,
//       color: "#d5cc3e"/*yellow*/
//     },
//     {
//       limit: 8000,
//       color: "#cd4d42"/*red*/
//     }
//   ], "co": [
//     {
//       limit: 0,
//       color: "#293e56"/*dark*/
//     },
//     {
//       limit: 30,
//       color: "#8195ff"/*blue*/
//     },
//     {
//       limit: 60,
//       color: "purple"
//     },
//     {
//       limit: 90,
//       color: "#57c7c7"
//     },
//     {
//       limit: 120,
//       color: "green"
//     },
//     {
//       limit: 150,
//       color: "#d5cc3e"/*yellow*/
//     },
//     {
//       limit: 200,
//       color: "#cd4d42"/*red*/
//     }
//   ], "hcho": [
//     {
//       limit: 0,
//       color: "#293e56"/*dark*/
//     },
//     {
//       limit: 30,
//       color: "#8195ff"/*blue*/
//     },
//     {
//       limit: 60,
//       color: "purple"
//     },
//     {
//       limit: 90,
//       color: "#57c7c7"
//     },
//     {
//       limit: 120,
//       color: "green"
//     },
//     {
//       limit: 150,
//       color: "#d5cc3e"/*yellow*/
//     },
//     {
//       limit: 200,
//       color: "#cd4d42"/*red*/
//     }
//   ],
// }

const product_list = {
  "no2": {
    id: "no2",
    label: "Nitrogen dioxide - NO₂",
    unit: "µmol/㎡",
    threshold: 20,
    max: 200
  },
  "so2": {
    id: "so2",
    label: "Sulfur dioxide - SO₂",
    unit: "µmol/㎡",
    threshold: 65,
    max: 8000
  },
  "co": {
    id: "co",
    label: "Carbon monoxide - CO",
    unit: "µmol/㎡",
    threshold: 10000,
    max: 80000
  },
  "hcho": {
    id: "hcho",
    label: "Formaldehyde - HCHO",
    unit: "µmol/㎡",
    threshold: 20,
    max: 800
  },
  "o3": {
    id: "o3",
    label: "Ozone - O3",
    unit: "µmol/㎡",
    threshold: 20,
    max: 280000
  }
}

$(function () {
  initMap();
  initNavDate();
  initSelectProduct();
  onChangeProduct();
  setColorLegend(colorCodeRange);
  triggerGetData();
})

$(window).load(function () {

});

function initNavDate() {
  var today = new Date()
  var dateRange = [];
  var past_count = 365;
  var future_count = 5;

  //past days
  for (var i = past_count; i > 0; i--) {
    const _d = new Date();
    _d.setDate(_d.getDate() - i);

    dateRange.push({
      date: formatDateDDMMYYYY(_d),
      wkday: weekday[_d.getDay()],
      class: (i == 1) ? "forecast" : "actual"
    })
  }

  //future days
  for (var i = 0; i < future_count + 1; i++) {
    const _d = new Date();
    _d.setDate(_d.getDate() + i);

    dateRange.push({
      date: formatDateDDMMYYYY(_d),
      wkday: weekday[_d.getDay()],
      class: (i == 0) ? "forecast current" : "forecast"
    })
  }

  console.log("Date range", dateRange);
  if (dateRange.length) {
    $navDate = $("#navDate");
    for (var i in dateRange) {
      element = '<li><a class="date ' + dateRange[i]['class'] + '" data-value="' + dateRange[i]['date'] + '"><h4>' + dateRange[i]['wkday'] + '</h4><label>' + dateRange[i]['date'] + '</label></a></li>';
      $navDate.append(element)
    }
    setTimeout(function () {
      $("a.date.current").trigger('click');
    }, 200)
  }
}

function formatDateDDMMYYYY(date) {
  var d = new Date(date),
    month = '' + (d.getMonth() + 1),
    day = '' + d.getDate(),
    year = d.getFullYear();

  if (month.length < 2)
    month = '0' + month;
  if (day.length < 2)
    day = '0' + day;

  return [day, month, year].join('-');
}

function triggerGetData() {
  $(document).on("click", 'a.date', { 'param': 1 }, function (event) {
    event.preventDefault();
    var $this = $(this)
    $("a.date").removeClass("selected");
    $this.addClass("selected");
    getDataByDate($this.attr("data-value"), $("#selectProduct").val(), $this.hasClass("forecast"));
  });
}

function getDataByDate(date, product, isForecast) {
  var part_url = isForecast ? "get-product-forecast" : "get-product";
  var part_url_date = date.split("-").reverse().join("-");
  $.get(part_url + "/all-dist/" + product + "/" + part_url_date, {})
    .done(function (data) {
      console.log("Data on ", date, JSON.parse(data));
      var res = JSON.parse(data);

      var waitingMap = setInterval(function () {
        console.log("GEO JSON NE: ", geojson)
        if (geojson) {
          //Update layers features
          for (var i in districtFeatures) {
            var dist_id = districtFeatures[i]["properties"]["name"];
            var density_val = (isForecast ? "<b>Dự báo: </b>" : "<b>Sentinel-5P: </b>") + parseFloat(res["data"][dist_id]).toFixed(2);
            var product_id = res["product_id"];
            var query_date = res["query_date"];
            districtFeatures[i]["properties"]["density"] = density_val;
            districtFeatures[i]["properties"]["product"] = product_list[product_id]["label"];
            districtFeatures[i]["properties"]["date"] = weekday[new Date(query_date).getDay()] + ", " + formatDateDDMMYYYY(query_date);
          }

          console.log("Layer districtFeatures: ", districtFeatures);

          geojson.setStyle(function (feature) {
            var dist_id = feature["properties"]["name"];
            console.log("==> value", dist_id, res["data"][dist_id]);
            var val = res["data"][dist_id];
            var product_id = res['product_id'];
            var max = product_list[product_id]['max'];
            return {
              fillColor: getColor(val, max, colorCodeRange),
              color: '#ffffff' /*Border color*/
            }
          })
          clearInterval(waitingMap);
        }
      }, 250)



    });
}

function getColor(val, max, colorCodeRange) {
  var _colorCode;
  for (var i in colorCodeRange) {
    if (val >= (max / colorCodeRange.length) * i) {
      _colorCode = colorCodeRange[i];
    } else {
      break;
    }
  }

  return _colorCode;
}

function initSelectProduct() {
  //init: set product to select
  for (var i in product_list) {
    var o = new Option(product_list[i]['label'], product_list[i]['id']);
    /// jquerify the DOM object 'o' so we can use the html method
    $(o).html(product_list[i]['label'],);
    $("#selectProduct").append(o);
  }
}

function onChangeProduct() {
  $("#selectProduct").on("change", function (e) {
    console.log("Change product", e);
    geojson.resetStyle();
    setColorLegend(colorCodeRange);
  })
}

function setColorLegend(colorCodeRange) {
  $("#colorLegend ul").find(".value").remove();
  var product_id = $("#selectProduct").val();
  var max = product_list[product_id]['max'];
  for (var i = (colorCodeRange.length - 1); i >= 0; i--) {
    var _limit = (max / (colorCodeRange.length - 1)) * i;
    var _clr = colorCodeRange[i];
    var element = '<li class="value" style="background-color: ' + _clr + '; color: ' + invertColor(_clr, true) + '";>' + nFormatter(_limit, 1) + '</li>';
    $("#colorLegend ul").append(element)
  }
}

//invert color: input: #colorcodehex , isBlackWhite = True/False
function invertColor(hex, bw) {
  if (hex.indexOf('#') === 0) {
    hex = hex.slice(1);
  }
  // convert 3-digit hex to 6-digits.
  if (hex.length === 3) {
    hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
  }
  if (hex.length !== 6) {
    throw new Error('Invalid HEX color.');
  }
  var r = parseInt(hex.slice(0, 2), 16),
    g = parseInt(hex.slice(2, 4), 16),
    b = parseInt(hex.slice(4, 6), 16);
  if (bw) {
    // http://stackoverflow.com/a/3943023/112731
    return (r * 0.299 + g * 0.587 + b * 0.114) > 186
      ? '#000000'
      : '#FFFFFF';
  }
  // invert color components
  r = (255 - r).toString(16);
  g = (255 - g).toString(16);
  b = (255 - b).toString(16);
  // pad each with zeros and return
  return "#" + padZero(r) + padZero(g) + padZero(b);
}

//number format 1000 => 1K
function nFormatter(num, digits) {
  var si = [
    { value: 1, symbol: "" },
    { value: 1E3, symbol: "K" },
    { value: 1E6, symbol: "M" },
    { value: 1E9, symbol: "G" },
    { value: 1E12, symbol: "T" },
    { value: 1E15, symbol: "P" },
    { value: 1E18, symbol: "E" }
  ];
  var rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
  var i;
  for (i = si.length - 1; i > 0; i--) {
    if (num >= si[i].value) {
      break;
    }
  }
  return (num / si[i].value).toFixed(digits).replace(rx, "$1") + si[i].symbol;
}