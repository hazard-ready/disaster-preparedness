require("normalize.css/normalize.css");
require("leaflet/dist/leaflet.css");
require("../style/app.scss");

var boundaryShape = require("./boundary.json");

require("../img/favicon.ico");
require("../img/marker-icon.png");
require("../img/marker-icon-2x.png");
require("../img/marker-shadow.png");
require("../img/thinking.gif");
require("../img/logo.png");
require("../img/logo-no-text.png");
require("../img/icon-search.png");
require("../img/caret.svg");
require("../img/language.svg");
require("../img/locate-me.svg");

require("./users");
require("./sections");

if (!String.prototype.includes) {
  String.prototype.includes = function(search, start) {
    "use strict";
    if (typeof start !== "number") {
      start = 0;
    }

    if (start + search.length > this.length) {
      return false;
    } else {
      return this.indexOf(search, start) !== -1;
    }
  };
}

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

var location_query_text = "";
var input_lat;
var input_lng;
var $locationInput;

// grab the position, if possible
var query_lat = getURLParameter("lat");
var query_lng = getURLParameter("lng");

// convenience function to extract url parameters
function getURLParameter(name) {
  var results = new RegExp("[?&]" + name + "=([^&#]*)").exec(
    window.location.href
  );
  return results === null ? null : results[1] || 0;
}

// Reload the current page, with the specified parameters (to show a location on the map and its information)
function loadPageWithParameters(lat, lng, queryText) {
  var query = "?lat=" + lat + "&lng=" + lng;
  if (queryText) {
    query += "&loc=" + queryText;
  }
  document.location = encodeURI(document.location.pathname + query);
}

function showGeocodeError() {
  $(".geocode-error-message").removeClass("hide");
}

function hideGeocodeError() {
  $(".geocode-error-message").addClass("hide");
}

function submitLocation(lat, lng, queryText) {
  if (!queryText) {
    // if we don't have text for the location, reverse geocode to get it
    $.ajax({
      type: "GET",
      url: "https://www.mapquestapi.com/geocoding/v1/reverse",
      data: {
        key: MAPQUEST_KEY,
        location: lat + "," + lng,
        outFormat: "json",
        thumbMaps: false
      }
    })
      .then(function(result) {
        // We have at least one result and nothing went wrong
        if (result.info.statuscode === 0 && result.results.length > 0) {
          var address = result.results[0].locations[0];
          queryText =
            address.street +
            ", " +
            address.adminArea5 +
            ", " +
            address.adminArea3 +
            " " +
            address.postalCode;
        } else {
          console.log("Reverse geocoding error messages", result.info.messages);
        }
      })
      .catch(function(error) {
        console.log("reverse geocoding error", error);
      })
      .always(function() {
        loadPageWithParameters(lat, lng, queryText);
      });
  } else {
    loadPageWithParameters(lat, lng, queryText);
  }
}

function setUpMap() {
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
    $locationInput.val(""); // clear query text
    submitLocation(e.latlng.lat, e.latlng.lng, "");
  });
}

function setStopHeight(heroContainer) {
  var headerHeight = $("header").outerHeight();
  var informationHeight = heroContainer.outerHeight();
  return headerHeight + informationHeight - 20;
}

function lazyLoadVideos() {
  $(".video").each(function(idx) {
    var self = $(this);
    var embedCode = self.data("embed");
    // Load the video preview thumbnails asynchronously
    var preview = new Image();
    preview.src = "https://img.youtube.com/vi/" + embedCode + "/sddefault.jpg";
    $(preview).on('load', function() {
      self.append(preview);
    });

    self.click(function() {
      var iframe = $(document.createElement("iframe"));

      iframe.attr("frameborder", 0);
      iframe.attr("allowfullscreen", "");
      iframe.attr(
        "src",
        "https://www.youtube.com/embed/" +
          embedCode +
          "?rel=0&showinfo=0&autoplay=1"
      );

      // Swap out the static image and the play button for the video when someone clicks on it.
      self.empty();
      self.append(iframe);
    });
  });
}

$(document).ready(function() {
  var infoContainer = $(".information-container--found-content");
  var heroContainer = $(".hero-container");
  var contentContainer = $(".content-container");

  // if we are on the found content page, stick the hero container and lazy load our videos.
  if (infoContainer.length) {
    var stopHeight = setStopHeight(heroContainer);

    var stickMenu = function() {
      if ($(document).scrollTop() >= stopHeight) {
        heroContainer.addClass("sticky");
        contentContainer.css({ "padding-top": stopHeight + 100 + "px" });
      } else {
        heroContainer.removeClass("sticky");
        contentContainer.css({ "padding-top": "" });
      }
    };

    $(document).scroll(stickMenu);

    $(window).resize(function() {
      stopHeight = setStopHeight(heroContainer);
    });

    lazyLoadVideos();
  }

  // Set up input box
  $locationInput = $("#location-text");
  var $locationSubmit = $("#location-submit");
  var $autoLocationButton = $(".auto-location-submit");
  if (document.getElementById("map")) {
    setUpMap();
  }

  // grab and set any previously entered query text
  var loc = getURLParameter("loc");
  var location_query_text = loc
    ? decodeURIComponent(loc)
    : query_lat + "," + query_lng;
  if (!query_lat || !query_lng) location_query_text = "";
  $locationInput.val(location_query_text);

  // Hide a geocoding error message every time, if there is one
  $locationInput.on("click", hideGeocodeError);

  // Set up autocomplete when someone clicks in the input field
  $locationInput.one("click", function() {
    var input = document.getElementById("location-text");
    $locationInput.prop("placeholder", "");
    var autocomplete = placeSearch({
      key: MAPQUEST_KEY,
      container: input,
      useDeviceLocation: !!navigator.geolocation
    });
    $locationInput.focus();

    autocomplete.on("change", function(event) {
      input_lat = event.result.latlng.lat;
      input_lng = event.result.latlng.lng;
    });
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
    if (location_query_text.trim().length == 0) return;
    disableForm();

    if (input_lat && input_lng) {
      submitLocation(input_lat, input_lng, location_query_text);
      return;
    }

    // Geocode our location text if we don't have a lat/lng from the autocomplete (e.g someone just typed in there and hit 'enter')
    $.ajax({
      type: "GET",
      url: "https://www.mapquestapi.com/geocoding/v1/address",
      data: {
        key: MAPQUEST_KEY,
        location: location_query_text,
        outFormat: "json",
        thumbMaps: false,
        boundingBox: mapBounds
      }
    })
      .then(function(result) {
        if (result.info.statuscode === 0) {
          var lat = result.results[0].locations[0].latLng.lat;
          var lon = result.results[0].locations[0].latLng.lng;
          submitLocation(lat, lon, location_query_text);
        } else {
          console.log("Geocoding error messages", result.info.messages);
          showGeocodeError();
        }
      })
      .catch(function(error) {
        console.log("error", error);
        showGeocodeError();
      });
  });

  // auto location (the Find Me button)
  $autoLocationButton.click(function() {
    hideGeocodeError();
    disableForm();

    if (!navigator.geolocation) {
      showGeocodeError();
      enableForm();
    } else {
      navigator.geolocation.getCurrentPosition(
        function(position) {
          var lat = position.coords.latitude;
          var lng = position.coords.longitude;
          // success! onwards to view the content
          submitLocation(lat, lng);
        },
        function(error) {
          console.log("Error finding your location: " + error.message);
          showGeocodeError();
          enableForm();
        },
        { timeout: 8000 }
      );
    }
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
});
