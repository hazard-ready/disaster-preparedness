$( document ).ready(function() {
  
  // app constants
  var google_api_key = "AIzaSyDIoSOu6JLsf3uZ4YPbti6fG-glvVMO4_M";
  var google_bounds = "46.308136,-124.575575|41.974902,-116.456679";

  var mapbox_access_token = "pk.eyJ1IjoibWVlc3RlcnN0dW1wIiwiYSI6IkdGVVFTSkkifQ.8_WCPGKmIImxpNy4dEWU1A";
  var mapbox_map = "meesterstump.8bf4e389";
  var mapbox_pin_color = "558";
  var mapbox_zoom_level = "15";
  var mapbox_image_size = "1280x300";  
  var mapbox_initial_lng = "-120.5";
  var mapbox_initial_lat = "44.1";
  var mapbox_initial_zoom_level = "6";
  // Default to a map of all of Oregon.
  var image_url = "http://api.tiles.mapbox.com/v4/" + mapbox_map + "/" + mapbox_initial_lng + "," + mapbox_initial_lat + "," + mapbox_initial_zoom_level + "/" + mapbox_image_size + ".png64?access_token=" + mapbox_access_token;
    
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
  var lat = getURLParameter('lat');
  var lng = getURLParameter('lng');
  
  // Check if HTML is specifying a default map (like on an error screen).  If not, use provided lat/lng.
  if ($("#map-image.default").length === 0 && (lat && lng)) {
    // TODO: better validation of lat/lon values
    image_url = image_url = "http://api.tiles.mapbox.com/v4/" + mapbox_map + "/pin-m+" + mapbox_pin_color + "(" + lng + "," + lat + ")/" + lng + "," + lat + "," + mapbox_zoom_level + "/" + mapbox_image_size + ".png64?access_token=" + mapbox_access_token;
  }
  $("#map-image").attr("src", image_url);
  

  // grab and set any previously entered query text
  var loc = getURLParameter('loc');
  var location_query_text = (loc) ? decodeURIComponent(loc) : "";
  $("#location-text").val(location_query_text);

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
    location_query_text = $("#location-text").val();
    if (location_query_text.length == 0) return;
    disableForm();
    // call google!
    geocodeSend(location_query_text);
  });
  
  // auto location
  $("#auto-location-submit").click(function() {
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
    $("#auto-location-submit").addClass("disabled");
    $(".loading").show();
  }
  
  // if a search fails or a restart, enable the form
  function enableForm() {
    $("#location-text").prop("disabled", false);
    $("#location-submit").removeClass("disabled");
    $("#auto-location-submit").removeClass("disabled");
    $(".loading").hide();
  }
  
  // request geocoding from google
  function geocodeSend(query) {
    // call google api!
    $.getJSON('https://maps.googleapis.com/maps/api/geocode/json?address=' + query + '&bounds=' + google_bounds + '&key=' + google_api_key, geocodeResponseHandler);
  }
  
  // handle google's json response
  function geocodeResponseHandler(data) {
    // only proceed if we have a location
    if (data.status != "OK") {
      enableForm();
      return;
    }
    // save the lat and lng
    var lat = data.results[0].geometry.location.lat;
    var lng = data.results[0].geometry.location.lng;
    // success! onwards to view the content
    submitLocation(lat, lng);
  }

  function submitLocation(lat,lng) {
    // reload the page with the lat,lng
    document.location =  encodeURI(document.location.hash + "?lat=" + lat + "&lng=" + lng + "&loc=" + location_query_text);
  }
  
  // revealing the geek box content
  $("#geek-bar a").click(function() {
    $("#geek-bar").addClass("down-arrow");
    $("#geek-content").removeClass("hide").slideDown();
    return false;
  });
  
  function openSocialPopup(siteName, event) {
    var url = '',
      title = '',
      width = 500,
      height = 300,
      left = (screen.width / 2) - (width / 2),
      top = (screen.height / 2) - (height / 2);
    switch (siteName) {
      case 'facebook':
        url = 'https://www.facebook.com/sharer/sharer.php?app_id=390011161186648&sdk=joey&u=http%3A%2F%2Fopb.org%2Faftershock&display=popup&ref=plugin&src=share_button';
        break;
      case 'twitter':
        url = 'https://twitter.com/intent/tweet?text=How%20will%20a%209.0%20earthquake%20impact%20you%3F%20Find%20out%20with%20the%20new%20Aftershock%20app.%20http%3A%2F%2Ftiny.cc%2Fgjerxx%20%23UnpreparedNW%20%40OPB%20%40stickyco';
        break;
      default:
        return;
    }
    window.open(url, title,'width=' + width + ', height=' + height + ', left=' + left + ', top=' + top + "'");
  }
  
  $('.social-icon').click(function(event) {
    var dest = $(this).data('site');
    openSocialPopup(dest, event);
  });
  

});