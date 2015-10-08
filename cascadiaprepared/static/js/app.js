$( document ).ready(function() {

  // Initial map values for Oregon overview
  var lat = "44.1";
  var lng = "-120.5";
  var zoom = "6";

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
  if (query_lat && query_lng) {
    lat = query_lat;
    lng = query_lng;
    zoom = 15;
  }

  // set up the map
  var map = L.map('map', {
    zoomControl: false,
    dragging: false,
    touchZoom: false,
    scrollWheelZoom: false,
    doubleClickZoom: false,
    boxZoom:false,
    tap: false,
    keyboard: false,
    attributionControl: false
  }).setView([lat,lng], zoom);
  L.esri.basemapLayer('Terrain').addTo(map);
  var layer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png').addTo(map);
  layer.setOpacity(0.6);

  document.getElementById('map').style.cursor='default';
  if (zoom > 10) {
    var icon = new L.Icon.Default;
    icon.options.iconUrl = "http://opb-news-interactives.s3-website-us-west-2.amazonaws.com/aftershock/img/marker-icon.png";
    var marker = L.marker([lat,lng], {
      icon: icon,
      clickable: false,
      keyboard: false
    }).addTo(map);
    layer.setOpacity(1);
  }

  // grab and set any previously entered query text
  var loc = getURLParameter('loc');
  var location_query_text = (loc) ? decodeURIComponent(loc) : lat + "," + lng;
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
    // call google!
    geocodeSend(location_query_text);
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

  // request geocoding from google CLIENT SIDE!
  var geocoder = new google.maps.Geocoder();

  function geocodeSend(query) {
      geocoder.geocode( { 'address': query}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          var lat = results[0].geometry.location.lat();
          var lon = results[0].geometry.location.lng();
          // var position = results[0].geometry.location;
          submitLocation(lat,lon);

          console.log(results);
          // console.log(position);


        } else {
          console.log('Geocode was not successful for the following reason: ' + status);
        }
      });
  }

  function submitLocation(lat,lng) {
    // reload the page with the lat,lng
    document.location =  encodeURI(document.location.hash + "?lat=" + lat + "&lng=" + lng + "&loc=" + location_query_text);
  }

  // revealing the geek box content
  // $("#geek-bar a").click(function() {
  //   $("#geek-bar").addClass("down-arrow");
  //   $("#geek-content").removeClass("hide").slideDown();
  //   return false;
  // });

  // function openSocialPopup(siteName, event) {
  //   var url = '',
  //     title = '',
  //     width = 500,
  //     height = 300,
  //     left = (screen.width / 2) - (width / 2),
  //     top = (screen.height / 2) - (height / 2);
  //   switch (siteName) {
  //     case 'facebook':
  //       url = 'https://www.facebook.com/sharer/sharer.php?app_id=390011161186648&sdk=joey&u=http%3A%2F%2Fopb.org%2Faftershock&display=popup&ref=plugin&src=share_button';
  //       break;
  //     case 'twitter':
  //       url = 'https://twitter.com/intent/tweet?text=How%20will%20a%209.0%20earthquake%20impact%20you%3F%20Find%20out%20with%20Aftershock.%20www.opb.org%2Faftershock%20%23UnpreparedNW%20%40OPB%20%40stickyco';
  //       break;
  //     default:
  //       return;
  //   }
  //   window.open(url, title,'width=' + width + ', height=' + height + ', left=' + left + ', top=' + top + "'");
  // }
  //
  // $('.social-icon').click(function(event) {
  //   var dest = $(this).data('site');
  //   openSocialPopup(dest, event);
  // });


});
