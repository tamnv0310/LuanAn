let district_define={};function initMap(){const t=new google.maps.Map(document.getElementById("map"),{zoom:12,center:{lat:10.753286734865803,lng:106.66258600458359},zoomControl:!0,mapTypeControl:!1,scaleControl:!1,streetViewControl:!1,rotateControl:!1,fullscreenControl:!1,disableDefaultUI:!0});t.data.loadGeoJson("static/data/hcm-district/district_geo.json"),t.data.setStyle((function(t){const e=district_define[t.getProperty("AdminID")].clr;return t.getProperty("isColorful")&&(e="violet"),{fillColor:e,strokeColor:"gray",strokeWeight:1,fillOpacity:.7}})),t.set("styles",[{stylers:[{visibility:"off"}]},{featureType:"water",stylers:[{visibility:"on"},{color:"#d4d4d4"}]},{featureType:"landscape",stylers:[{visibility:"on"},{color:"#e5e3df"}]},{featureType:"administrative.country",elementType:"labels",stylers:[{visibility:"on"}]},{featureType:"administrative.country",elementType:"geometry",stylers:[{visibility:"on"},{weight:1.3}]}]);var e=new google.maps.InfoWindow;t.data.addListener("click",(function(a){let o="<b>"+district_define[a.feature.getProperty("AdminID")].distName+"</b>";e.setContent(o),e.setPosition(a.latLng),e.setOptions({pixelOffset:new google.maps.Size(0,-30)}),e.open(t)})),t.data.addListener("mouseover",(function(e){t.data.revertStyle(),t.data.overrideStyle(e.feature,{strokeWeight:1.4,fillOpacity:.8})})),t.data.addListener("mouseout",(function(e){t.data.revertStyle()})),console.log(8888888,t.data)}function handleMarker(t){console.log("click handleMarker",t,t.latLng.toJSON(),"Name ===>",t.domEvent)}$.getJSON("static/data/hcm-district/district_define.json",(function(t){district_define=t,console.log(t)}));var district_data=[];const product_list={no2:{id:"no2",label:"Nitrogen dioxide - NO₂",unit:"µmol/㎡",threshold:20},so2:{id:"so2",label:"Sulfur dioxide - SO₂",unit:"µmol/㎡",threshold:65},co:{id:"co",label:"Carbon monoxide - CO",unit:"µmol/㎡",threshold:1e4},hcho:{id:"hcho",label:"Formaldehyde - HCHO",unit:"µmol/㎡",threshold:20}};function customRange(t){if("todate"==t.id){var e=new Date($("#fromdate").val());return e.setDate(e.getDate()+1),{minDate:e}}return{}}function formatDateYYYYMMDD(t){var e=t.split("-");return e[2]+"-"+e[1]+"-"+e[0]}var ctx=null,my_chart=null;function initChart(){ctx=document.getElementById("my_chart").getContext("2d"),my_chart=new Chart(ctx,{type:"line",data:{labels:[],datasets:[]},options:{scales:{y:{suggestedMax:250,suggestedMin:0,beginAtZero:!0}},responsive:!0,plugins:{}}})}$((function(){for(var t in initMap(),$("#fromdate, #todate").datepicker({showOn:"both",beforeShow:customRange,dateFormat:"dd-mm-yy",regional:"vi"}),$("#fromdate").datepicker("setDate",-7),$("#todate").datepicker("setDate",5),product_list){var e=new Option(product_list[t].label,product_list[t].id);$(e).html(product_list[t].label),$("#selectProduct").append(e)}$.get("/get-district-all",{}).done((function(t){for(var e in district_data=JSON.parse(t)){var a=new Option(district_data[e].dist_name,district_data[e]._id);$(a).html(district_data[e].dist_name),$("#selectDistrict").append(a)}})),initChart(),$("#retriveData").click((function(){var t=$("#selectDistrict").find(":selected").val(),e=$("#selectProduct").find(":selected").val(),a=formatDateYYYYMMDD($("#fromdate").val()),o=formatDateYYYYMMDD($("#todate").val());t&&a&&o?$.get("/get-product/"+e+"/"+t+"/"+a+"/"+o,{}).done((function(t){res=JSON.parse(t),console.log("res data: ",res);var a=[],o=[],r=[];if(my_chart.data.datasets=[],res.data&&res.data.length||alert("Dữ liệu đang cập nhật..."),res.data&&res.data.length){console.log("res data: ",res.data);var i=res.data;for(var l in i)console.log("real value",i[l]),a.push(i[l].date),o.push(i[l].val);my_chart.data.datasets.push({label:"Giá trị thực tế",data:o,fill:!0,borderColor:"rgba(40, 167, 69, 0.7",backgroundColor:"rgba(40, 167, 69, 0.5",tension:.35,borderWidth:2,pointBorderWidth:1.23,pointRadius:1.5})}if(res.data_pred&&res.data_pred.length){console.log("res data predict: ",res.data_pred);var n=product_list[e].threshold,d=res.data_pred;for(var l in res.data)parseInt(l)==res.data.length-1?r.push(res.data[l].val):r.push(NaN);for(var l in d){console.log("predict",d[l]),a.push(d[l].date);var s=d[l].val_pred<n?0:d[l].val_pred;r.push(s)}my_chart.data.datasets.push({label:"Giá trị dự báo",data:r,fill:!0,borderColor:"rgba(20, 159, 255, 0.8)",backgroundColor:"rgba(20, 159, 255, 0.6)",tension:.35,borderWidth:2,pointBorderWidth:1.23,pointRadius:1.5}),console.log(r)}my_chart.data.labels=a,my_chart.options={plugins:{legend:{position:"top"},title:{display:!0,text:"Giá trị nồng độ "+product_list[e].label+" ("+product_list[e].unit+")",position:"top",font:{size:15},padding:{top:10,bottom:12}},tooltip:{titleFont:{size:14,lineHeight:1.5},bodyFont:{size:13.2,lineHeight:1.4},padding:10,caretPadding:5,callbacks:{beforeTitle:function(t){return product_list[e].label},title:function(t){return"Ngày: "+t[0].label},label:function(t){return" "+t.dataset.label+": "+t.formattedValue.toLocaleString("vi-VN")+" µmol/㎡"}}}}},my_chart.update()})):alert("Vui lòng nhập đầy đủ dữ liệu cần truy vấn!")}))}));
//# sourceMappingURL=statistic-dist.js.map