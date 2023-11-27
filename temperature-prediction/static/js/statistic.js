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
          suggestedMax: 50,
          suggestedMin: 0,
          beginAtZero: true
        }
      },
      responsive: true,
      plugins: {
        export: {
      // Tùy chọn của plugin xuất khẩu
      enabled: true,
      // Các tùy chọn khác của plugin xuất khẩu
    }
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

function LoadArea() {
  var data = [
  { value: 'hcm', text: 'Thành phố Hồ Chí Minh' },
  { value: 'binhduong', text: 'Bình Dương' },
  { value: 'bariavungtau', text: 'Bà Rịa - Vũng Tàu' },
  { value: 'dongnai', text: 'Đồng Nai' },
  { value: 'tayninh', text: 'Tây Ninh' },
  { value: 'binhphuoc', text: 'Bình Phước' },
  { value: 'binhthuan', text: 'Bình Thuận' }
];
  for (var i in data) {
        var o = new Option(data[i]['text'], data[i]['value']);
        /// jquerify the DOM object 'o' so we can use the html method
        $(o).html(data[i]['text'],);
        $("#selectDistrict").append(o);
      }
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
  // $.get("/get-district-all", {})
  //   .done(function (data) {
  //     district_data = JSON.parse(data)
  //     for (var i in district_data) {
  //       var o = new Option(district_data[i]['dist_name'], district_data[i]['_id']);
  //       /// jquerify the DOM object 'o' so we can use the html method
  //       $(o).html(district_data[i]['dist_name'],);
  //       $("#selectDistrict").append(o);
  //     }
  //   });
  LoadArea()
  //init chart
  initChart();

  //retrive data
  $("#retriveData").click(function () {
    // var dist_id = $("#selectDistrict").find(":selected").val();
    // var product_id = $("#selectProduct").find(":selected").val();
    var from_date = formatDateYYYYMMDD($("#fromdate").val());
    var to_date = formatDateYYYYMMDD($("#todate").val());

    // if (!dist_id || !from_date || !to_date || !product_id) {
    //   alert("Vui lòng nhập đầy đủ dữ liệu cần truy vấn.");
    //   return;
    // }
    if (from_date > to_date) {
      alert("Ngày bắt đầu phải bé hơn ngày kết thúc.");
      return;
    }
    console.log(from_date)
    var _label = [];
    var _data = [];
    var _data_pred = [];
    my_chart.data.datasets = [];
    var currentDate = new Date(from_date);
    var endDate = new Date(to_date);
    while (currentDate <= endDate) {
      var formattedDate = currentDate.toLocaleDateString('en-US', { day: 'numeric', month: 'numeric', year: 'numeric' });
      var temperature = Math.random() * 4 + 28; // Giá trị ngẫu nhiên trong khoảng từ 28 đến 31
      var temperaturePred = Math.random() * 3 + 28; // Giá trị ngẫu nhiên trong khoảng từ 28 đến 31

      _label.push(formattedDate)
      // if (currentDate.getDate() === 3) {
      //     _data.push(temperature.toFixed(0));
      //     _data_pred.push(temperature.toFixed(0));
      // } else {
      //     _data.push(temperature.toFixed(0));
      //     if (currentDate.getDate() > 3) {
      //       _data_pred.push(temperaturePred.toFixed(0));
      //     }
      // }

      currentDate.setDate(currentDate.getDate() + 1);
    }

    var jsonData = JSON.stringify(_data);
    var jsonData2 = JSON.stringify(_data_pred);

    console.log('_data', jsonData)
    console.log('_data_pred', jsonData2)

    _data = [
  24,
  25,
  24,
  24,
  23,
  23,
  23,
  23,
  24,
  24,
  25,
  25,
  26,
  26,
  26,
  25,
  25,
  25,
  24,
  24,
  26,
  27,
  27,
  26,
  24,
  25,
  26,
  24,
  23,
  23,
  25
];
    // _data_pred = [NaN,"31","30","29","31","29","28","29","30"]
    my_chart.data.datasets.push({
            label: 'Giá trị thực tế',
            data: _data,
            fill: true,
            borderColor: '#ff4d4d',
            backgroundColor: 'rgba(0, 0, 0, 0)',
            tension: 0.35, /*bo góc*/
            borderWidth: 2,
            pointBorderWidth: 1.23,
            pointRadius: 1.5
          })

    my_chart.data.datasets.push({
            label: 'Giá trị dự báo',
            data: _data_pred,
            fill: true,
            borderColor: '#95adbe',
            backgroundColor: 'rgba(0, 0, 0, 0)',
            tension: 0.35, /*bo góc*/
            borderWidth: 2,
            pointBorderWidth: 1.23,
            pointRadius: 1.5
          })

    my_chart.data.labels = _label;

    my_chart.options = {
      scales: {
        yAxes: [{
          ticks: {
            suggestedMin: 0,
            suggestedMax: 50
          }
        }]
      },
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Nhiệt độ không khí tầm 2 mét',
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
              return 'Nhiệt độ'
            },
            title: function (tooltipItem) {
              return "Ngày: " + tooltipItem[0]['label']
            },
            label: function (tooltipItem) {
              return " " + tooltipItem.dataset.label + ": " + tooltipItem.formattedValue.toLocaleString('vi-VN') + " °C";
            },
          }
        },
        export: {
          // Tùy chọn của plugin xuất khẩu
          enabled: true,
        }
      }
    };

    my_chart.update();

  })

  //triggerDownloadChartImg
  triggerDownloadChartImg();

  //triggerDownloadExcel
  triggerDownloadExcel();

  //tooltip
  $("[data-toggle='tooltip']").tooltip();
})
