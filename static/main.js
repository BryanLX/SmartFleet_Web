var pageList = ['dashboard','vehicle','workers', 'taskassignment'];
var nav = ['nav1','nav2','nav3','nav4'];
var panelName=['All tasks','Vehicle List','Worker List','Task assignment'];
var apiLink = 'https://d1841083.ngrok.io'


var workers = null;
var tasks = null;
var vehicles = null;
var intervalID = null;
// In the following example, markers appear when the user clicks on the map.
// The markers are stored in an array.
// The user can then click an option to hide, show or delete the markers.
var map;
var markers = [];

function initMap() {
  var haightAshbury = {lat: 43.642567, lng: -79.387054};

  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    center: haightAshbury,
    mapTypeId: 'terrain'
  });

  // This event listener will call addMarker() when the map is clicked.
  map.addListener('click', function(event) {
    addMarker(event.latLng);
  });

  // Adds a marker at the center of the map.
  addMarker(haightAshbury);
}

// Adds a marker to the map and push to the array.
function addMarker(location) {
  deleteMarkers();

  var marker = new google.maps.Marker({
    position: location,
    map: map
  });

  // $.getJSON(apiLink+'/destination/'+location.lat.toString()+'/'+location.lng.toString(), function(data){
  //     console.log(data);
  //     $('#panelName').text();
  // })




  console.log(location.lat);
  console.log(location.lat.toString());
  var finallink = apiLink+'/destination?lat='+location.lat.toString()+'&lng='+location.lng.toString();
  console.log(finallink);
  console.log('huhuhu')
  // var finallink =  apiLink.concat("/destination?lat=",location.lat.toString() );
  finallink = finallink.concat("&lng=",location.lng.toString());
  console.log(finallink);
  var testlink = 'https://d1841083.ngrok.io/destination?lat=43.642567&lng=-79.387054';
  // $.get(testlink,function(data){
  //     console.log(data);
  // })
  //
  // $.ajax({url: testlink, success: function(result){
  //   console.log(result)
  // }});
  markers.push(marker);


}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
  setMapOnAll(null);
}

// Shows any markers currently in the array.
function showMarkers() {
  setMapOnAll(map);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  clearMarkers();
  markers = [];
}





function setUp(){
    loadDashboard();
}



//
// function initMap() {
//   // The location of Uluru
//   var uluru = {lat: -25.344, lng: 131.036};
//   // The map, centered at Uluru
//   var map = new google.maps.Map(
//       document.getElementById('map'), {zoom: 4, center: uluru});
//   // The marker, positioned at Uluru
//   var marker = new google.maps.Marker({position: uluru, map: map});
// }


function changepage(pageid) {
  for (i = 0; i < pageList.length; i++) {
      var temp = document.getElementById(pageList[i]);
      if (i==pageid) {
        temp.style.display = 'block';
      } else {
        temp.style.display = 'none';
      }
  }
  for (i=0;i<4;i++){
    var tempnav = document.getElementById(nav[i]);
    if (i!=pageid) {
      tempnav.classList.remove('active');
      tempnav.classList.remove('inactive');
      tempnav.classList.add('inactive');
    } else {
      tempnav.classList.remove('active');
      tempnav.classList.remove('inactive');
      tempnav.classList.add('active');
    }
  }
  $('#panelName').text(panelName[pageid]);
  loadPageDetails(i);
}

function loadPageDetails(i){
  switch(i) {
  case 0:
    loadDashboard();
    break;
  case 1:
    loadVehicle();
    break;
  case 2:
    loadWorkers();
    break;
  case 3:
    loadTaskAssignment();
    break;
  default:
    // code block
  }
}

function loadDashboard(){
  changepage(0);
  // getTasksList();
}

function loadVehicle(){


}
function loadWorkers(){


}

function addTask(){
  changepage(0);

  var html = `
  <div class="card border-dark mb-3" style="width: 18rem;">
    <div class="card-body">
      <h5 class="card-title">Deliver Apple to Markham</h5>
      <br>
      <h6 class="card-subtitle mb-2 "><b>Assigned worker:</b> Steve </h6>
      <h6 class="card-subtitle mb-2 "><b>Assigned vehicle:</b> BMW 323i </h6>
      <h6 class="card-subtitle mb-2 "><b>Status:</b> Not Started</h6>
      <h6 class="card-subtitle mb-2 "><b>Start time:</b> <time>10:00</time> </h6>
      <h6 class="card-subtitle mb-2 "><b>Estimate finish time:</b> <time>12:00</time> </h6>
      <p class="card-text">Deliver 100 Apple to Markham in 10 mins, be care for with apple</p>

    </div>
  </div>
  `
  $("#tasksList").append(html)

}
function loadTaskAssignment(){

  console.log("loading Task Assignment page")
  // In the following example, markers appear when the user clicks on the map.
  // Each marker is labeled with a single alphabetical character.
  var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var labelIndex = 0;

  function initialize() {
  var bangalore = { lat: 12.97, lng: 77.59 };
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    center: bangalore
  });

  // This event listener calls addMarker() when the map is clicked.
  google.maps.event.addListener(map, 'click', function(event) {
    addMarker(event.latLng, map);
  });

  // Add a marker at the center of the map.
  addMarker(bangalore, map);
  }

  // Adds a marker to the map.
  function addMarker(location, map) {
  // Add the marker at the clicked location, and add the next-available label
  // from the array of alphabetical characters.
  var marker = new google.maps.Marker({
    position: location,
    label: labels[labelIndex++ % labels.length],
    map: map
  });
  }

  google.maps.event.addDomListener(window, 'load', initialize);
}

function helperMethod(html,json){


}

function getTasksList(){
  // $('#tasksList').empty();
  $.getJSON("http://localhost:8080/dashboard",
     function(data) {
        console.log(data);
      });
}
function getVehicles(){
    id = "";
    alert("tryget")
    $.getJSON("http://localhost:8080/vehicles",
       function(data) {
          console.log(data);
        });

}


function frequentCheck(){
    updateVehicleById();
    intervalID = setInterval(updateVehicleById, 10000);
}

function updateVehicleById(){
    $.getJSON("http://localhost:8080/vehicle/943b8f4c-4137-4f0e-9883-f2d353f2d61a/location",
       function(data) {
          $("#trueLocation").text(data)
        });
    $.getJSON("http://localhost:8080/vehicle/943b8f4c-4137-4f0e-9883-f2d353f2d61a/odometer",
       function(data) {
          $("#truemileage").text(data.data.distance)
        });
}

function lockCar(){
  $.getJSON("http://localhost:8080/vehicle/943b8f4c-4137-4f0e-9883-f2d353f2d61a/lock",
     function(data) {
        alert("lock successful")
      });

}

function unlockCar(){
  $.getJSON("http://localhost:8080/vehicle/943b8f4c-4137-4f0e-9883-f2d353f2d61a/unlock",
     function(data) {
        alert("unlock successful")
      });
}
