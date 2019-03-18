require("normalize.css/normalize.css");
require("slick-carousel/slick/slick.css");
require("slick-carousel/slick/slick-theme.css");
require("leaflet/dist/leaflet.css");
require("../style/app.scss");

var boundaryShape = require("./boundary.json");

require("../img/favicon.ico");
require("../img/marker-icon.png");
require("../img/marker-shadow.png");
require("../img/thinking.gif");
require("../img/logo.png");
require("../img/logo-no-text.png");
require("../img/icon-search.png");

require("./users");
require("slick-carousel");

// This is the base repository Mapquest key. Get your own Mapquest key for a new app!
var MAPQUEST_KEY = "b3ZxSWOID7jOlLLGb8KvPxbF4DGBMEHy";
var osmUrl =
  "//{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=3a70462b44dd431586870baee15607e4";
var osmAttrib =
  'Map data © <a href="//openstreetmap.org">OpenStreetMap</a> contributors';

var boundaryStyle = {
  color: "rgb(253, 141, 60)",
  weight: 4,
  opacity: 1,
  fillColor: "#ffffff",
  fillOpacity: 0.7
};

$(document).ready(function() {
  // convenience function to extract url parameters
  function getURLParameter(name) {
    var results = new RegExp("[?&]" + name + "=([^&#]*)").exec(
      window.location.href
    );
    return results === null ? null : results[1] || 0;
  }

  // grab the position, if possible
  var query_lat = getURLParameter("lat");
  var query_lng = getURLParameter("lng");

  // set up the map
  var map = new L.Map("map", {
    scrollWheelZoom: false
  });
  if (query_lat && query_lng) {
    zoom = 14;
    map.setView([query_lat, query_lng], zoom);
  } else {
    // use the data bounds if we don't have a position in the query string
    map.fitBounds(mapBounds);
  }

  var layer = L.tileLayer(osmUrl, { attribution: osmAttrib }).addTo(map);
  layer.setOpacity(0.6);

  var boundaryLayer = L.geoJson(boundaryShape, {
    style: boundaryStyle
  }).addTo(map);

  document.getElementById("map").style.cursor = "default";
  if (query_lat && query_lng) {
    var icon = new L.Icon.Default();
    // these may be in ../static/img if you translate/localize, due to the URL language prefix.
    icon.options.iconUrl = "marker-icon.png";
    icon.options.shadowUrl = "marker-shadow.png";
    var marker = L.marker([query_lat, query_lng], {
      icon: icon,
      clickable: false,
      keyboard: false
    }).addTo(map);
    layer.setOpacity(1);
  }

  // Make a click on the map submit the location
  map.on("click", function(e) {
    location_query_text = "";
    $locationInput.val(location_query_text); // clear query text
    submitLocation(e.latlng.lat, e.latlng.lng);
  });

  // Set up input box
  var $locationInput = $("#location-text");
  var $locationSubmit = $("#location-submit");
  var $autoLocationButton = $(".auto-location-submit");

  // grab and set any previously entered query text
  var loc = getURLParameter("loc");
  var location_query_text = loc
    ? decodeURIComponent(loc)
    : query_lat + "," + query_lng;
  if (!query_lat || !query_lng) location_query_text = "";
  $locationInput.val(location_query_text);

  // Set up autocomplete when someone clicks in the input field
  $locationInput.one("click", function() {
    var input = document.getElementById("location-text");
    $locationInput.prop("placeholder", "");
    placeSearch({
      key: MAPQUEST_KEY,
      container: input,
      useDeviceLocation: true
    });
    $locationInput.focus();
  });

  // hitting enter key in the textfield will trigger submit
  $locationInput.keydown(function(event) {
    if (event.keyCode == 13) {
      $locationSubmit.trigger("click");
      return false;
    }
  });

  // submit location text
  $locationSubmit.click(function() {
    // grab the query value, ignoring it if it's empty
    location_query_text = $locationInput.val();
    if (location_query_text.length == 0) return;
    disableForm();

    // Geocode our location text
    $.ajax({
      type: "GET",
      url: "https://www.mapquestapi.com/geocoding/v1/address",
      data: {
        key: MAPQUEST_KEY,
        location: location_query_text,
        outFormat: "json",
        thumbMaps: false,
        boundingBox: mapBounds
      },
      error: function(error) {
        console.log("error", error);
        $(".geocode-error-message").html(
          $("p").text("We had a problem finding that location.")
        );
      },
      success: function(result) {
        if (result.info.statuscode === 0) {
          var lat = result.results[0].locations[0].latLng.lat;
          var lon = result.results[0].locations[0].latLng.lng;
          submitLocation(lat, lon);
        } else {
          console.log("Geocoding error messages", result.info.messages);
          $(".geocode-error-message").html(
            $("p").text("We had a problem finding that location.")
          );
        }
      }
    });
  });

  // auto location
  $autoLocationButton.click(function() {
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
      console.log("Error finding your location: " + error.message);
      enableForm();
    };
    navigator.geolocation.getCurrentPosition(geoSuccess, geoError, geoOptions);
  });

  // during api calls, disable the form
  function disableForm() {
    $locationInput.prop("disabled", true);
    $locationSubmit.addClass("disabled");
    $autoLocationButton.addClass("disabled");
    $(".loading").show();
  }

  // if a search fails or a restart, enable the form
  function enableForm() {
    $locationInput.prop("disabled", false);
    $locationSubmit.removeClass("disabled");
    $autoLocationButton.removeClass("disabled");
    $(".loading").hide();
  }

  function submitLocation(lat, lng) {
    // reload the page with the lat,lng
    document.location = encodeURI(
      document.location.pathname +
        "?lat=" +
        lat +
        "&lng=" +
        lng +
        "&loc=" +
        location_query_text
    );
  }

  // Set up slick photo slideshow
  function loadGallery() {
    var currentSlideElement = $(".disaster-content.active .past-photos");
    currentSlideElement.slick({
      slidesToShow: 1,
      variableWidth: true,
      prevArrow: '<button type="button" class="slick-prev"></button>',
      nextArrow: '<button type="button" class="slick-next"></button>'
    });
    return currentSlideElement;
  }

  // Initialize the slide gallery on the open disaster tab
  var slideContainer = loadGallery();

  // Open a new image gallery when a new tab is opened
  $(".disaster-tabs").on("toggled", function() {
    slideContainer.slick("unslick");
    slideContainer = loadGallery();
  });
});
