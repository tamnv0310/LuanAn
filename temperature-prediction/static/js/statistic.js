'use-strict'

var product_dist_data = [];

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
          min: 0,   // Giá trị tối thiểu
          max: 50,  // Giá trị tối đa
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

function LoadArea() {
  var data = [
    { value: 'hcm', text: 'Thành phố Hồ Chí Minh' },
    { value: 'binhduong', text: 'Bình Dương' },
    { value: 'vungtau', text: 'Bà Rịa - Vũng Tàu' },
    { value: 'dongnai', text: 'Đồng Nai' },
    { value: 'tayninh', text: 'Tây Ninh' },
    { value: 'binhphuoc', text: 'Bình Phước' }
  ];
  for (var i in data) {
    var o = new Option(data[i]['text'], data[i]['value']);
    /// jquerify the DOM object 'o' so we can use the html method
    $(o).html(data[i]['text'],);
    $("#selectLocation").append(o);
  }
}

$(function () {
  $("#exportChartToCSV").hide();
  //init Date picker
  $('#fromdate, #todate').datepicker({
    showOn: "both",
    beforeShow: customRange,
    dateFormat: "dd-mm-yy",
    regional: "vi"
  });

  $("#fromdate").datepicker("setDate", -7);
  $("#todate").datepicker("setDate", 5);

  // //init: set product to select
  // for (var i in product_list) {
  //   var o = new Option(product_list[i]['label'], product_list[i]['id']);
  //   /// jquerify the DOM object 'o' so we can use the html method
  //   $(o).html(product_list[i]['label'],);
  //   $("#selectProduct").append(o);
  // }

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
    $("#exportChartToCSV").show();
    var province_id = $("#selectLocation").find(":selected").val();
    // var product_id = $("#selectProduct").find(":selected").val();
    var from_date = formatDateYYYYMMDD($("#fromdate").val());
    var to_date = formatDateYYYYMMDD($("#todate").val());

    if (!province_id || !from_date || !to_date) {
      alert("Vui lòng nhập đầy đủ dữ liệu cần truy vấn.");
      return;
    }
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
     

      _label.push(formattedDate)


      currentDate.setDate(currentDate.getDate() + 1);
    }
    let url = '/get-temperature/' + province_id + '/' + from_date + '/' + to_date
    $.get(url, {})
      .done(function (response) {
        debugger
        console.log("Response:", response)
        const data = JSON.parse(response);
        data.forEach(item => {
          if (item.isForecast) {
            // _data_pred.push(Math.round(item.val));
            _data_pred.push(item.val);
          } else {
            // _data.push(Math.round(item.val));
            _data.push(item.val);
            _data_pred.push('NaN');
          }
        });
        // Check if _data_pred contains NaN and _data has elements
        if (_data_pred.includes('NaN') && _data.length > 0) {
          // Remove the first occurrence of NaN from _data_pred
          _data_pred.splice(_data_pred.indexOf('NaN'), 1);

          // Add the last element of _data at the end of the NaN values in _data_pred
          let lastIndexOfNaN = _data_pred.lastIndexOf('NaN');
          _data_pred.splice(lastIndexOfNaN + 1, 0, _data[_data.length - 1]);
        }
        console.log(_data_pred)
        console.log(_data)
        my_chart.data.datasets.push({
          label: 'Giá trị thực tế',
          data: _data,
          fill: true,
          borderColor: '#ff4d4d',
          backgroundColor: 'rgba(0, 0, 0, 0)',
          tension: 0.35,
          borderWidth: 2,
          pointBorderWidth: 1.23,
          pointRadius: 1.5
        });

        my_chart.data.datasets.push({
          label: 'Giá trị dự báo',
          data: _data_pred,
          fill: true,
          borderColor: '#95adbe',
          backgroundColor: 'rgba(0, 0, 0, 0)',
          tension: 0.35,
          borderWidth: 2,
          pointBorderWidth: 1.23,
          pointRadius: 1.5
        });

        my_chart.data.labels = _label;

        my_chart.options = {
          scales: {
            yAxes: [{
              ticks: {
                Min: 0,
                Max: 50
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
                  return 'Nhiệt độ';
                },
                title: function (tooltipItem) {
                  return "Ngày: " + tooltipItem[0]['label'];
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
      }).fail(function (error) {
        console.error("Error in AJAX request: ", error);
      });

  })
  // function loadDataChart(_data, _data_pred, _label) {
  //   console.log(_data)
  //   console.log(_data_pred)

   $("#exportChartToCSV").click(function (){
     alert("exportChartToCSV")
      var province_id = $("#selectLocation").find(":selected").val();
    // var product_id = $("#selectProduct").find(":selected").val();
    var from_date = formatDateYYYYMMDD($("#fromdate").val());
    var to_date = formatDateYYYYMMDD($("#todate").val());

    if (!province_id || !from_date || !to_date) {
      alert("Vui lòng nhập đầy đủ dữ liệu cần truy vấn.");
      return;
    }
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


      _label.push(formattedDate)


      currentDate.setDate(currentDate.getDate() + 1);
    }
    let url = '/export-temperature/' + province_id + '/' + from_date + '/' + to_date
    $.get(url, {})
      .done(function (response) {
        debugger
        console.log("Response:", response)
        // Create a Blob from the response
        // Process the blob data and initiate the download
        var filename = "export_temperature_data_" + province_id + "_" +  from_date + "_" + to_date + ".csv"; // Replace with your desired filename
        var blob = new Blob([response], { type: 'application/octet-stream' });

        var a = document.createElement('a');
        a.href = window.URL.createObjectURL(blob);
        a.download = filename;

        // Programmatically trigger a click event to initiate the download
        a.click();

        // Clean up after the download is initiated
        window.URL.revokeObjectURL(a.href);

    // Release the blob URL
    URL.revokeObjectURL(downloadUrl);

    xhr.send();

      }).fail(function (error) {
        console.error("Error in AJAX request: ", error);
      });
   })
  // }
  //triggerDownloadChartImg
  triggerDownloadChartImg();

  //tooltip
  $("[data-toggle='tooltip']").tooltip();
})


