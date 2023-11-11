$(function () {
  $("#collect-dataset").not(".disabled").click(function () {
    $(this).addClass("disabled");
    $("#msg-collect-dataset").html('<i class="fas fa-cog fa-spin mr-2"></i>Đang lấy dữ liệu')
    $.get("collect-dataset", {})
      .done(function (res) {
        console.log(1111, res);
        if (res == '') {
          $("#msg-collect-dataset").html('<i class="fas fa-times mr-2"></i><span class="text-success">Some errors occures, contact your administrator to solve this problems.</span>')
        } else {
          $("#msg-collect-dataset").html('<span class="text-success"><i class="fas fa-check mr-2"></i>' + res + '</span>')
        }
      });
  })

  $("#collect-dataset-district").not(".disabled").click(function () {
    $(this).addClass("disabled");
    $("#msg-collect-dataset-district").html('<i class="fas fa-cog fa-spin mr-2"></i>Đang thêm Dataset vào 24 quận/huyện')
    $.get("collect-dataset-district", {})
      .done(function (res) {
        console.log(2222, res);
        if (res == '') {
          $("#msg-collect-dataset-district").html('<i class="fas fa-times mr-2"></i><span class="text-success">Some errors occures, contact your administrator to solve this problems.</span>')
        } else {
          $("#msg-collect-dataset-district").html('<span class="text-success"><i class="fas fa-check mr-2"></i>' + res + '</span>')
        }
      });
  })

  $("#add-district-to-db").not(".disabled").click(function () {
    $(this).addClass("disabled");
    $("#msg-add-district-to-db").html('<i class="fas fa-cog fa-spin mr-2"></i>Đang thêm dữ liệu vào Database')
    $.get("add-district-to-db", {})
      .done(function (res) {
        if (res == '') {
          $("#msg-add-district-to-db").html('<i class="fas fa-times mr-2"></i><span class="text-success">Some errors occures, contact your administrator to solve this problems.</span>')
        } else {
          $("#msg-add-district-to-db").html('<span class="text-success"><i class="fas fa-check mr-2"></i>' + res + '</span>')
        }
      });
  })

  $("#add-data-to-db").not(".disabled").click(function () {
    $(this).addClass("disabled");
    $("#msg-add-data-to-db").html('<i class="fas fa-cog fa-spin mr-2"></i>Đang thêm dữ liệu vào Database')
    $.get("add-data-to-db", {})
      .done(function (res) {
        if (res == '') {
          $("#msg-add-data-to-db").html('<i class="fas fa-times mr-2"></i><span class="text-success">Some errors occures, contact your administrator to solve this problems.</span>')
        } else {
          $("#msg-add-data-to-db").html('<span class="text-success"><i class="fas fa-check mr-2"></i>' + res + '</span>')
        }
      });
  })

  $("#add-data-predict-to-db").not(".disabled").click(function () {
    $(this).addClass("disabled");
    $("#msg-add-data-predict-to-db").html('<i class="fas fa-cog fa-spin mr-2"></i>Đang thêm dữ liệu vào Database')
    $.get("add-data-predict-to-db", {})
      .done(function (res) {
        if (res == '') {
          $("#msg-add-data-predict-to-db").html('<i class="fas fa-times mr-2"></i><span class="text-success">Some errors occures, contact your administrator to solve this problems.</span>')
        } else {
          $("#msg-add-data-predict-to-db").html('<span class="text-success"><i class="fas fa-check mr-2"></i>' + res + '</span>')
        }
      });
  })

})