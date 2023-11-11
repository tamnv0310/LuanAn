'use-strict'

var district_data = [];
var product_dist_data = [];
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
  "o3": {
    id: "o3",
    label: "Ozone - O3",
    unit: "µmol/㎡",
    threshold: 0
  },
  "pm25": {
    id: "pm25",
    label: "Bụi mịn PM2.5",
    unit: "µg/m³",
    threshold: 20,
    max: 500
  }
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
  ctx.fillStyle = 'white';
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

//Trigger download chart IMG
function triggerDownloadChartImg() {
  $('#btn-download-chart').click(function () {
    var from_date = $("#fromdate").val();
    var to_date = $("#todate").val();
    var dist_id = $("#selectDistrict").find(":selected").val();
    var product_id = $("#selectProduct").find(":selected").val();
    // Trigger the download
    var a = document.createElement('a');
    a.href = getChartImgBase64(my_chart);
    a.download = product_id + '_' + dist_id + '_' + from_date + '_' + to_date + '.png';
    console.log(a);
    a.click();
  });
}

//Export chart to IMG
function getChartImgBase64(my_chart) {
  return my_chart.toBase64Image();
}

//triggerDownloadExcel
function triggerDownloadExcel() {
  $('#btn-download-excel').click(function () {
    console.log("Export Excel File",product_dist_data);
    var data = [];
    var dist = product_dist_data["dist"]["_id"];
    var from_date = $("#fromdate").val();
    var to_date = $("#todate").val();
    var dist_id = $("#selectDistrict").find(":selected").val();
    var product_id = $("#selectProduct").find(":selected").val();

    if(product_dist_data["data"]&&product_dist_data["data"].length){
      var _d = product_dist_data["data"];
      for(var i in _d){
        var obj = {
            "Location": dist,
            "Date": _d[i]["date"],
            "Value" :parseFloat(_d[i]["val"]).toFixed(2),
            "Forecast" : "",
        }
        data.push(obj);
      }
    }

    if(product_dist_data["data_pred"]&&product_dist_data["data_pred"].length){
      var _d = product_dist_data["data_pred"];
      for(var i in _d){
        var obj = {
            "Location": dist,
            "Date": _d[i]["date"],
            "Value" : "",
            "Forecast" :parseFloat(_d[i]["val_pred"]).toFixed(2),
        }
        data.push(obj);
      }
    }
    console.log("Excel data: ",data)
    var title = product_id + '_' + dist_id + '_' + from_date + '_' + to_date;
    JSONToCSVConvertor(data, title , true);
  });
}

//JSONToCSVConvertor
function JSONToCSVConvertor(JSONData, ReportTitle, ShowLabel) {
  //If JSONData is not an object then JSON.parse will parse the JSON string in an Object
  var arrData = typeof JSONData != 'object' ? JSON.parse(JSONData) : JSONData;

  var CSV = 'sep=,' + '\r\n\n';

  //This condition will generate the Label/Header
  if (ShowLabel) {
    var row = "";

    //This loop will extract the label from 1st index of on array
    for (var index in arrData[0]) {

      //Now convert each value to string and comma-seprated
      row += index + ',';
    }

    row = row.slice(0, -1);

    //append Label row with line break
    CSV += row + '\r\n';
  }

  //1st loop is to extract each row
  for (var i = 0; i < arrData.length; i++) {
    var row = "";

    //2nd loop will extract each column and convert it in string comma-seprated
    for (var index in arrData[i]) {
      row += '"' + arrData[i][index] + '",';
    }

    row.slice(0, row.length - 1);

    //add a line break after each row
    CSV += row + '\r\n';
  }

  if (CSV == '') {
    alert("Invalid data");
    return;
  }

  //Generate a file name
  var fileName = "";
  //this will remove the blank-spaces from the title and replace it with an underscore
  fileName += ReportTitle.replace(/ /g, "_");

  //Initialize file format you want csv or xls
  var uri = 'data:text/csv;charset=utf-8,' + escape(CSV);

  // Now the little tricky part.
  // you can use either>> window.open(uri);
  // but this will not work in some browsers
  // or you will not get the correct file extension    

  //this trick will generate a temp <a /> tag
  var link = document.createElement("a");
  link.href = uri;

  //set the visibility hidden so it will not effect on your web-layout
  link.style = "visibility:hidden";
  link.download = fileName + ".csv";

  //this part will append the anchor tag and remove it after automatic click
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

$(function () {
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

    if (!dist_id || !from_date || !to_date || !product_id) {
      alert("Vui lòng nhập đầy đủ dữ liệu cần truy vấn.");
      return;
    }
    if (from_date > to_date) {
      alert("Ngày bắt đầu phải bé hơn ngày kết thúc.");
      return;
    }
    $.get("/get-product/" + product_id + "/" + dist_id + "/" + from_date + "/" + to_date + "", {})
      .done(function (data) {
        res = JSON.parse(data);
        product_dist_data = res;
        console.log("res data: ", res)
        var _label = [];
        var _data = [];
        var _data_pred = [];
        my_chart.data.datasets = [];

        if (!res['data'] || !res['data'].length) {
          alert("Dữ liệu không tồn tại hoặc đang cập nhật...");
          $(".btn-export").fadeOut();
        } else {
          $(".btn-export").fadeIn();
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
                  return product_list[product_id]['label']
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

  //triggerDownloadChartImg
  triggerDownloadChartImg();

  //triggerDownloadExcel
  triggerDownloadExcel();

  //tooltip
  $("[data-toggle='tooltip']").tooltip();
})
