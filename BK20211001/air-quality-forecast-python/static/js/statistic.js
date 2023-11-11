'use-strict'

//@prepros-prepend 'inc/statistic-map.js';

var district_data = []

const product_list = {
  "no2": {
    id: "no2",
    label: "Nitrogen dioxide - NO₂",
    unit: "µmol/㎡",
    threshold: 20
  },
  "so2": {
    id: "so2",
    label: "Sulfur dioxide - SO₂",
    unit: "µmol/㎡",
    threshold: 65
  },
  "co": {
    id: "co",
    label: "Carbon monoxide - CO",
    unit: "µmol/㎡",
    threshold: 10000
  },
  "hcho": {
    id: "hcho",
    label: "Formaldehyde - HCHO",
    unit: "µmol/㎡",
    threshold: 20
  },
}

//CUSTOM RANGE DATEPICKER
function customRange(input) {
  if (input.id == 'todate') {
    var minDate = new Date($('#fromdate').val());
    minDate.setDate(minDate.getDate() + 1)

    return {
      minDate: minDate
    };
  }

  return {}
}

//format date string
function formatDateYYYYMMDD(data) {
  var _d = data.split("-");
  return _d[2] + "-" + _d[1] + "-" + _d[0]
}

//Init chart
var ctx = null, my_chart = null;
function initChart() {
  ctx = document.getElementById('my_chart').getContext('2d');
  my_chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: []
    },
    options: {
      scales: {
        y: {
          suggestedMax: 250,
          suggestedMin: 0,
          beginAtZero: true
        }
      },
      responsive: true,
      plugins: {
      }
    }
  });
}

$(function () {
  //init Map
  initMap();

  //init Date picker
  $('#fromdate, #todate').datepicker({
    showOn: "both",
    beforeShow: customRange,
    dateFormat: "dd-mm-yy",
    regional: "vi"
  });

  $("#fromdate").datepicker("setDate", -7);
  $("#todate").datepicker("setDate", 5);

  //init: set product to select
  for (var i in product_list) {
    var o = new Option(product_list[i]['label'], product_list[i]['id']);
    /// jquerify the DOM object 'o' so we can use the html method
    $(o).html(product_list[i]['label'],);
    $("#selectProduct").append(o);
  }

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

  //init chart
  initChart();

  //retrive data
  $("#retriveData").click(function () {
    var dist_id = $("#selectDistrict").find(":selected").val();
    var product_id = $("#selectProduct").find(":selected").val();
    var from_date = formatDateYYYYMMDD($("#fromdate").val());
    var to_date = formatDateYYYYMMDD($("#todate").val());

    if (!dist_id || !from_date || !to_date) {
      alert("Vui lòng nhập đầy đủ dữ liệu cần truy vấn!");
      return;
    }
    $.get("/get-product/" + product_id + "/" + dist_id + "/" + from_date + "/" + to_date + "", {})
      .done(function (data) {
        res = JSON.parse(data)
        console.log("res data: ", res)
        var _label = [];
        var _data = [];
        var _data_pred = [];
        my_chart.data.datasets = [];

        if (!res['data'] || !res['data'].length) {
          alert("Dữ liệu đang cập nhật...");
        }

        if (res['data'] && res['data'].length) {
          console.log("res data: ", res['data']);
          var resData = res['data'];
          for (var i in resData) {
            console.log("real value", resData[i])
            _label.push(resData[i]['date']);
            _data.push(resData[i]['val']);
          }
          my_chart.data.datasets.push({
            label: 'Giá trị thực tế',
            data: _data,
            fill: true,
            borderColor: 'rgba(40, 167, 69, 0.7',
            backgroundColor: 'rgba(40, 167, 69, 0.5',
            tension: 0.35, /*bo góc*/
            borderWidth: 2,
            pointBorderWidth: 1.23,
            pointRadius: 1.5
          })
        }

        if (res['data_pred'] && res['data_pred'].length) {
          console.log("res data predict: ", res['data_pred']);
          var threshold = product_list[product_id]['threshold'];
          var resData_pred = res['data_pred'];
          for (var i in res['data']) {
            if (parseInt(i) == res['data'].length - 1) {
              _data_pred.push(res['data'][i]['val']);
            } else {
              _data_pred.push(NaN);
            }
          }
          for (var i in resData_pred) {
            console.log("predict", resData_pred[i])
            _label.push(resData_pred[i]['date']);
            var val_pred = (resData_pred[i]['val_pred'] < threshold ? 0 : resData_pred[i]['val_pred']);
            _data_pred.push(val_pred);
          }
          my_chart.data.datasets.push({
            label: 'Giá trị dự báo',
            data: _data_pred,
            fill: true,
            borderColor: 'rgba(20, 159, 255, 0.8)',
            backgroundColor: 'rgba(20, 159, 255, 0.6)',
            tension: 0.35, /*bo góc*/
            borderWidth: 2,
            pointBorderWidth: 1.23,
            pointRadius: 1.5
          })
          console.log(_data_pred)
        }

        my_chart.data.labels = _label;

        my_chart.options = {
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Giá trị nồng độ ' + product_list[product_id]['label'] + ' (' + product_list[product_id]['unit'] + ')',
              position: 'top',
              font: {
                size: 15
              },
              padding: {
                top: 10,
                bottom: 12
              }
            },
            tooltip: {
              titleFont: {
                size: 14,
                lineHeight: 1.5
              },
              bodyFont: {
                size: 13.2,
                lineHeight: 1.4
              },
              padding: 10,
              caretPadding: 5,
              callbacks: {
                beforeTitle: function (tooltipItem) {
                  return  product_list[product_id]['label']
                },
                title: function (tooltipItem) {
                  return "Ngày: " + tooltipItem[0]['label']
                },
                label: function (tooltipItem) {
                  return " " + tooltipItem.dataset.label + ": " + tooltipItem.formattedValue.toLocaleString('vi-VN') + " µmol/㎡";
                },
              }
            }
          }
        };

        my_chart.update();
      });
  })
})
