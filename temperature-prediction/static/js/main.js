'use-strict'
//@prepros-prepend 'inc/main-map.js';

var district_data = [];
var future_count = 5;
var dataStartDate = "01/10/1981";
var dumpDate = "10/03/2023";
const weekday = new Array(7);
weekday[0] = "Chủ nhật";
weekday[1] = "Thứ hai";
weekday[2] = "Thứ ba";
weekday[3] = "Thứ tư";
weekday[4] = "Thứ năm";
weekday[5] = "Thứ sáu";
weekday[6] = "Thứ bảy";

var playStatus = 0;
/*
-1: Pause => ready to play;
1: Playing => ready to pause
*/

//colorCodeRange: low to high
// const colorCodeRange = ['#3776bf', '#a7c6ed', '#40bdb1', '#e0da69', '#e1c63b', '#df7a4c', '#d14673', '#aa335c', '#631417', '#46080b', '#2b0002']
// const colorCodeRange = ['#3da570', '#44c359', '#55e93a', '#e0da69', '#e1c63b', '#df7a4c', '#d14673', '#aa335c', '#631417', '#46080b', '#2b0002']
const colorCodeRange = ['#1d10ff', '#3f66ff', '#b1d2f4', '#5dd5d1', '#258200', '#9fcf00', '#f9cf00', '#f66401', '#f70000','#660000'];


const product_list = {
  "temperature": {
    id: "temperature",
    label: "°C",
    unit: "°C",
    unitConvert: "°C",
    threshold: 20,
    max: 45
  },
}

var dateSwiper;

$(function () {
  initMap();
  initSelectDistrict();
  onChangeDistrict();
  initSelectProduct();
  onChangeProduct();
  setColorLegend(colorCodeRange);
  triggerGetData();
  triggerPlay();
  initDateInput();
  initDateSwiper();
})

function initSelectDistrict() {
  //get 24 district info, init select district
  $.get("/get-district-all", {})
    .done(function (data) {
      district_data = JSON.parse(data)
      for (var i in district_data) {
        var o = new Option(district_data[i]['dist_name'], district_data[i]['_id']);
        /// jquerify the DOM object 'o' so we can use the html method
        $(o).html(district_data[i]['dist_name'],);
        $("#selectDistrict").append(o);
      }
    });
}

function onChangeDistrict() {
  $("#selectDistrict").on("change", function (e) {
    console.log("Zoom to district", e, $(this).val());
    var selectedVal = $(this).val();
    for (var i in geojson._layers) {
      if (geojson._layers[i]["feature"]["properties"]["name"] == selectedVal) {
        var bounds = geojson._layers[i]["_bounds"];
        map.fitBounds(bounds, { padding: [20, 10] });
      }
    }
  })
}

function initDateInput() {
  $("#date").datepicker({
    showOn: "both",
    dateFormat: "dd-mm-yy",
    regional: "vi"
  }).on("change", function () {
    var date = $(this).val();
    var $slideElement = $("a.date[data-value=" + date + "]");
    $slideElement.click();
  });;

  $("#date").datepicker("setDate", new Date(dumpDate));
  var maxDate = new Date();
  maxDate.setDate(maxDate.getDate() + future_count);
  $('#date').datepicker('option', 'minDate', new Date(dataStartDate));
  $('#date').datepicker('option', 'maxDate', maxDate);
}

function initDateSwiper() {
  dateSwiper = new Swiper('.dateSwiper', {
    slidesPerView: "auto",
    spaceBetween: 15,
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    on: {
      init: function () {
        console.log('swiper initialized');
      },
      afterInit: function () {
        console.log('after initialized', dateSwiper);
        var dateRange = getAvailableDate();
        console.log("Date range", dateRange);
        if (dateRange.length) {
          var slides = []
          for (var i = dateRange.length - 1; i > 0; i--) {
            element = '<a class="swiper-slide date ' + dateRange[i]['class'] + '" data-value="' + dateRange[i]['date'] + '" data-index="' + i + '"><h4>' + dateRange[i]['wkday'] + '</h4><label>' + dateRange[i]['date'] + '</label></a>';
            slides.push(element);
          }
          setTimeout(function () {
            dateSwiper.prependSlide(slides);
          }, 1500)

          //bấm vô ngày hiện tại
          setTimeout(function () {
            $("a.date.current").trigger('click');
          }, 1500)
        }
      },
      slidesLengthChange: function () {
        $("a.date.current").trigger('click');
      }
    },
  });

}

function getAvailableDate() {
  var today = new Date(dumpDate)
  var startDate = new Date(2022,10,10);
  const diffTime = Math.abs(today - startDate);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) - 1;
  var dateRange = [];
  var past_count = diffDays;

  //past days
  for (var i = past_count + 1; i > 0; i--) {
    const _d = new Date(dumpDate);
    _d.setDate(_d.getDate() - i);

    dateRange.push({
      date: formatDateDDMMYYYY(_d),
      wkday: weekday[_d.getDay()],
      class: (i == 0) ? "forecast" : "actual" //dự báo và thực tế
    })
  }

  //future days
  for (var i = 0; i < future_count + 1; i++) {
    const _d = new Date(dumpDate);
    _d.setDate(_d.getDate() + i);

    dateRange.push({
      date: formatDateDDMMYYYY(_d),
      wkday: weekday[_d.getDay()],
      class: (i == 0) ? "forecast current" : "forecast"
    })
  }

  return dateRange;
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
    console.log("On click button!!!!!!")
    var $this = $(this)
    $("a.date").removeClass("selected");
    $this.addClass("selected");
    var pos = parseInt($this.attr("data-index")) - 1;
    var dt = $this.attr("data-value");
    $('#date').datepicker("setDate", dt);
    dateSwiper.slideTo(pos);
    getDataByDate($this.attr("data-value"), $("#selectProduct").val(), $this.hasClass("forecast"));
  });
}

//tham số date, sản phẩm: temperature, có phải là dự báo không (ngày tương lai của hiện tại thì true)
function getDataByDate(date, product, isForecast) {
  //api lấy data....
  //đây là data giả
  let res = {
    "product_id": "temperature",
    "query_date": "2023-11-12",
    "data": {
      "vungtau": 29,
      "dongnai": 31,
      "binhphuoc": 32,
      "tayninh": 32,
      "hcm": 32,
      "binhduong": 32,
    }
  }

  console.log("Data on ", date, res);

  var max = 50; //50 độ C
  var query_date = res["query_date"];

  var waitingMap = setInterval(function () {
    if (geojson) {
      //Update layers features
      for (var i in districtFeatures) {
        var dist_id = districtFeatures[i]["properties"]["name"];
        var density_tmp = parseFloat(res["data"][dist_id]).toFixed(2);
        var density_val = Number(density_tmp).toLocaleString('vi-VN');
        console.log("density_val: ", density_val)
        districtFeatures[i]["properties"]["textType"] = isForecast ? "<b>Dự báo: </b>" : "<b>POWER NASA: </b>";
        districtFeatures[i]["properties"]["density"] = density_val;
        districtFeatures[i]["properties"]["color"] = getColor(density_tmp, max, colorCodeRange);
        districtFeatures[i]["properties"]["date"] = weekday[new Date(query_date).getDay()] + ", " + formatDateDDMMYYYY(query_date);
      }

      geojson.setStyle(function (feature) {
        var dist_id = feature["properties"]["name"];
        var val = res["data"][dist_id];
        return {
          fillColor: getColor(val, max, colorCodeRange),
          color: '#ffffff' /*Border color*/
        }
      })
      clearInterval(waitingMap);
    }
  }, 250)
}

function getColor(val, max, colorCodeRange) {
  var _colorCode = "#a6a6a6";
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
    console.log("Change product", e, $(this).val());
    geojson.resetStyle();
    setColorLegend(colorCodeRange);
    $("a.date.current").click();
  })
}

function setColorLegend(colorCodeRange) {
  $("#colorLegend ul").find(".value").remove();
  const product_id = $("#selectProduct").val();
  const max = product_list[product_id]['max'];
  const unit = product_list[product_id]['unit'];
  $("#product-unit.unit").html(unit);
  for (var i = (colorCodeRange.length - 1); i >= 0; i--) {
    var _limit = (max / (colorCodeRange.length - 1)) * i;
    var _clr = colorCodeRange[i];
    var plusSymbol = (colorCodeRange.length - 1) === i ? '+' : '';
    var element = '<li class="value" style="background-color: ' + _clr + '; color: ' + invertColor(_clr, true) + '";>' + nFormatter(_limit, 1) + plusSymbol + '</li>';
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

function triggerPlay() {
  var looping;
  var playStatus = 1;
  var $currentBtn = null;

  $(".control-date ul li a").click(function (e) {
    e.preventDefault();
    var type = $(this).attr("data-type");
    console.log("type = ", type)
    switch (type) {
      case "prev":
        console.log("Click previous!");
        $currentBtn = $("a.date.selected");
        var $prevBtn = $currentBtn.prev();
        if ($prevBtn.length) {
          $prevBtn.trigger("click");
        }
        break;

      case "next":
        console.log("Click next!");
        $currentBtn = $("a.date.selected");
        var $nextBtn = $currentBtn.next();
        if ($nextBtn.length) {
          $nextBtn.trigger("click");
        }
        break;

      default:
        if ($(this).hasClass("readyToStop")) {
          playStatus = -1;
          $(this).removeClass("readyToStop");
        } else {
          playStatus = 1;
          $(this).addClass("readyToStop");
        }

        if (!playStatus) {
          clearInterval(looping)
        } else {
          looping = setInterval(function () {
            if (playStatus == 1) {
              $currentBtn = $("a.date.selected");
              var $nextBtn = $currentBtn.next();
              if ($nextBtn.length) {
                $nextBtn.trigger("click");
              }
            } else {
              clearInterval(looping)
            }
          }, 2000)
        }
    }
  })
}

//format date string
function formatDateYYYYMMDD(data) {
  var _d = data.split("-");
  return _d[2] + "-" + _d[1] + "-" + _d[0]
}
