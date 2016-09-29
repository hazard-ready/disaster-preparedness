$( document ).ready(function() {
  $(document).foundation();

  // convenience function to extract url parameters
  function getURLParameter(name) {
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    } else {
       return results[1] || 0;
    }
  }

  // grab the position, if possible
  var query_lat = getURLParameter('lat');
  var query_lng = getURLParameter('lng');

  // set up the map
  var map = L.map('map');
  if (query_lat && query_lng) {
    zoom = 15;
    map.setView([query_lat, query_lng], zoom);
  } else { // use the data bounds if we don't have a position in the query string
    map.fitBounds(mapBounds);
  }
  map.scrollWheelZoom.disable();

  var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
  var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
  var layer = new L.TileLayer(osmUrl, {attribution: osmAttrib}).addTo(map);
  layer.setOpacity(0.6);

  document.getElementById('map').style.cursor='default';
  if (query_lat && query_lng) {
    var icon = new L.Icon.Default;
    icon.options.iconUrl = "static/img/marker-icon.png";
    var marker = L.marker([query_lat, query_lng], {
      icon: icon,
      clickable: false,
      keyboard: false
    }).addTo(map);
    layer.setOpacity(1);
  }

  // Make a click on the map submit the location
  map.on('click', function(e) {
    location_query_text = "";
    $("#location-text").val(location_query_text);  // clear query text
    submitLocation(e.latlng.lat, e.latlng.lng);
  });

  // grab and set any previously entered query text
  var loc = getURLParameter('loc');
  var location_query_text = (loc) ? decodeURIComponent(loc) : query_lat + "," + query_lng;
  if (!query_lat || !query_lng)
    location_query_text = "";
  $("#location-text").val(location_query_text);

  // // hitting enter key in the textfield will trigger submit
  $("#location-text").keydown(function(event) {
    if (event.keyCode == 13) {
      $('#location-submit').trigger('click');
      return false;
    }
  });

  // submit location text
  $("#location-submit").click(function() {
    // grab the query value, ignoring it if it's empty
    location_query_text = $("#location-text").val();
    if (location_query_text.length == 0) return;
    disableForm();

    // request geocoding from google CLIENT SIDE!
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode( { 'address': location_query_text}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        var lat = results[0].geometry.location.lat();
        var lon = results[0].geometry.location.lng();
        submitLocation(lat,lon);
      } else {
        $(".geocode-error-message").html($('p').text("We had a problem finding that location."));
      }
    });
  });

  // auto location
  $(".auto-location-submit").click(function() {
    location_query_text = "";
    disableForm();
    var geoOptions = { timeout: 8000 };
    var geoSuccess = function(position) {
      var lat = position.coords.latitude;
      var lng = position.coords.longitude;
      // success! onwards to view the content
      submitLocation(lat, lng);
    };
    var geoError = function(error) {
      console.log('Error occurred. Error code: ' + error.code);
      enableForm();
    };
    navigator.geolocation.getCurrentPosition(geoSuccess, geoError, geoOptions);
  });

  // during api calls, disable the form
  function disableForm() {
    $("#location-text").prop("disabled", true);
    $("#location-submit").addClass("disabled");
    $(".auto-location-submit").addClass("disabled");
    $(".loading").show();
  }

  // if a search fails or a restart, enable the form
  function enableForm() {
    $("#location-text").prop("disabled", false);
    $("#location-submit").removeClass("disabled");
    $(".auto-location-submit").removeClass("disabled");
    $(".loading").hide();
  }

  function submitLocation(lat,lng) {
    // reload the page with the lat,lng
    document.location =  encodeURI(document.location.hash + "?lat=" + lat + "&lng=" + lng + "&loc=" + location_query_text);
  }

});
