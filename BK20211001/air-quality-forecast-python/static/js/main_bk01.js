'use-strict'
//@prepros-prepend 'inc/main-map.js';

var weekday = new Array(7);
weekday[0] = "Chủ nhật";
weekday[1] = "Thứ hai";
weekday[2] = "Thứ ba";
weekday[3] = "Thứ tư";
weekday[4] = "Thứ năm";
weekday[5] = "Thứ sáu";
weekday[6] = "Thứ bảy";

function initNavDate() {
  var today = new Date()
  var dateRange = [];
  var past_count = 3;
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

  console.log(88888, dateRange);
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

$(function () {
  initMap();
  initNavDate();
  triggerGetData();
})

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
    getDataByDate($this.attr("data-value"));
  });
}

function getDataByDate(date) {
  console.log(8888, date)
  $.get("/get-product/all-dist/no2/" + date.split("-").reverse().join("-"), {})
    .done(function (data) {
      console.log(9999, data)
    });
}
