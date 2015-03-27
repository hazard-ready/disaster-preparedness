$( document ).ready(function() {
  
  // app constants
  var google_api_key = "AIzaSyBSZGyycuPZO0BBfJqO-RBFeKM7_icZUnk";

  var mapbox_access_token = "pk.eyJ1IjoibWVlc3RlcnN0dW1wIiwiYSI6IkdGVVFTSkkifQ.8_WCPGKmIImxpNy4dEWU1A";
  var mapbox_map = "meesterstump.8bf4e389";
  var mapbox_pin_color = "08B";
  var mapbox_zoom_level = "15";
  var mapbox_image_size = "970x300";  
  var mapbox_initial_lon = "-120.5";
  var mapbox_initial_lat = "44.1";
  var mapbox_initial_zoom_level = "6";
  

  /********** HOME VIEW (input form) **********/
  
  // hitting enter key in the textfield will trigger submit
  $("#location-text").keydown(function(event) {
    if (event.keyCode == 13) {
      $('#location-submit').trigger('click');
      return false;
    }
  });
  
  // submit location text 
  $("#location-submit").click(function() {
    // grab the query value, ignoring it if it's empty
    var selection = $("#location-text").val();
    if (selection.length == 0) return;
    disableForm();
    // call google!
    geocodeSend(selection);
  });
  
  // auto location
  $("#auto-location-submit").click(function() {
    disableForm();
    var geoOptions = { timeout: 8000 };
    var geoSuccess = function(position) {
      var lat = position.coords.latitude;
      var lon = position.coords.longitude;
      // success! onwards to view the content
      updateViewWithNewLocation(lat, lon);
    };
    var geoError = function(error) {
      console.log('Error occurred. Error code: ' + error.code);
      enableForm();
    };
    navigator.geolocation.getCurrentPosition(geoSuccess, geoError, geoOptions);
  });
  
  // during api calls, disable the form
  // TODO: add animation to show action is happening?
  function disableForm() {
    $("#location-submit").addClass("disabled");
    $("#auto-location-submit").addClass("disabled");
  }
  
  // if a search fails or a restart, enable the form
  function enableForm() {
    $("#location-submit").removeClass("disabled");
    $("#auto-location-submit").removeClass("disabled");
  }
  
  // request geocoding from google
  function geocodeSend(query) {
    // call google api!
    $.getJSON('https://maps.googleapis.com/maps/api/geocode/json?address=' + query + '&key=' + google_api_key, geocodeResponseHandler);
  }
  
  // handle google's json response
  function geocodeResponseHandler(data) {
    // only proceed if we have a location
    if (data.status != "OK") {
      enableForm();
      return;
    }
    // save the lat and lon
    var lat = data.results[0].geometry.location.lat;
    var lon = data.results[0].geometry.location.lng;
    // success! onwards to view the content
    updateViewWithNewLocation(lat, lon);
  }

  function updateViewWithNewLocation(lat,lon) {
    // build the mapbox image url
    var image_url = "http://api.tiles.mapbox.com/v4/" + mapbox_map + "/pin-s+" + mapbox_pin_color + "(" + lon + "," + lat + ")/" + lon + "," + lat + "," + mapbox_zoom_level + "/" + mapbox_image_size + ".png64?access_token=" + mapbox_access_token;
    // request the new map image
    $("#map-image").attr("src", image_url); 
  }
  
  // initially load a map of all of oregon
  var image_url = "http://api.tiles.mapbox.com/v4/" + mapbox_map + "/" + mapbox_initial_lon + "," + mapbox_initial_lat + "," + mapbox_initial_zoom_level + "/" + mapbox_image_size + ".png64?access_token=" + mapbox_access_token;
  $("#map-image").attr("src", image_url);

});