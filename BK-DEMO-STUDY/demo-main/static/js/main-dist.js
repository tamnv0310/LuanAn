const disList=[["Quận 1",10.787436068902563,106.69960973395696,1],["Quận 2",10.78574978589337,106.75642964757539,1],["Quận 3",10.78274697952383,106.68387064781815,1],["Quận 4",10.75906294493157,106.70373781246386,1],["Quận 5",10.756513620593799,106.66844919549033,1],["Quận 6",10.74690320573997,106.63524508658222,1],["Quận 7",10.73521837192968,106.72765540680004,1],["Quận 8",10.731818859883173,106.64074272782443,1],["Quận 9",10.82887178380493,106.81877509870857,1],["Quận 10",10.774150491814002,106.66728219808635,1],["Quận 11",10.764258170326938,106.6475260620237,1],["Quận 12",10.879929961982896,106.65417819234524,1],["Quận Bình Thạnh",10.807835270496955,106.69998814295555,1],["Quận Bình Tân",10.765773913031648,106.5975783552529,1],["Quận Tân Bình",10.812649270622119,106.65172898232998,1],["TP. Thủ Đức",10.853585336549742,106.74183355224741,1],["Huyện Bình Chánh",10.713090120649863,106.56077339239506,1],["Huyện Cần Giờ",10.542352609110127,106.84971274721454,1],["Huyện Nhà Bè",10.693760867615097,106.73837162338681,1],["Huyện Củ Chi",11.00712372932034,106.5002687761377,1],["Huyện Hóc Môn",10.886796911702286,106.57289357971491,1]];let markers=[];function initMap(){const n=new google.maps.Map(document.getElementById("map"),{zoom:12,center:{lat:10.753286734865803,lng:106.66258600458359},zoomControl:!0,mapTypeControl:!1,scaleControl:!1,streetViewControl:!1,rotateControl:!1,fullscreenControl:!1}),t={coords:[1,1,1,20,18,20,18,1],type:"poly"};for(let l=0;l<disList.length;l++){const o=disList[l];var e=new google.maps.Marker({position:{lat:o[1],lng:o[2]},map:n,shape:t,title:o[0],zIndex:o[3]});markers.push(e)}for(let n=0;n<markers.length;n++){let t=markers[n];t.addListener("click",(function(n){let e=n.latLng.toJSON().lat,l=n.latLng.toJSON().lng;$(".district-name").html(t.getTitle()),$(".no2-value").html("Đang dò..."),$(".lat-value").html(e),$(".lon-value").html(l),$.get("/get-no2?lat="+e+"&lon="+l,(function(n){$(".no2-value").html(Math.round(100*n)/100+" µmol/m²")}))}))}}function handleMarker(n){console.log("click handleMarker",n,n.latLng.toJSON(),"Name ===>",n.domEvent)}$((function(){initMap()}));
//# sourceMappingURL=main-dist.js.map