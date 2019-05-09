require("normalize.css/normalize.css");
require("slick-carousel/slick/slick.css");
require("slick-carousel/slick/slick-theme.css");
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

// about page images
require("../img/flowchart.png");
require("../img/cmk_headshot.jpg");
require("../img/rbk_headshot.jpg");
require("../img/gk_headshot.jpg");
require("../img/linkedin-logo.png");
require("../img/linkedin-logo@2x.png");

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

var location_query_text = "";
var input_lat;
var input_lng;

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
  $(".geocode-error-message").html(
    $("p").text("We had a problem finding that location.")
  );
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

$(document).ready(function() {
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
    $locationInput.val(""); // clear query text
    submitLocation(e.latlng.lat, e.latlng.lng, "");
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
    var autocomplete = placeSearch({
      key: MAPQUEST_KEY,
      container: input,
      useDeviceLocation: true
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
    disableForm();

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

  // Set up expanding and collapsing sections. Set up slideshow
  // in applicable sections when they are expanded.
  var collapseSectionClass = "section-content--collapse";
  var caretUpClass = "caret--up";

  $(".section-title--collapse").on("click", function(event) {
    var $sectionTitle = $(event.delegateTarget);
    var contentSectionId = $sectionTitle.data("section");
    if (contentSectionId) {
      var $contentSection = $("#" + contentSectionId);
      var $titleCaret = $sectionTitle.find(".caret");
      var $currentSlideElement = $("#" + contentSectionId + " .past-photos");

      if ($contentSection.hasClass(collapseSectionClass)) {
        $contentSection.removeClass(collapseSectionClass);
        $titleCaret.addClass(caretUpClass);

        if ($currentSlideElement) {
          $currentSlideElement.slick({
            slidesToShow: 1,
            variableWidth: false
          });
        }
      } else {
        $contentSection.addClass(collapseSectionClass);
        $titleCaret.removeClass(caretUpClass);
        if ($currentSlideElement) {
          $currentSlideElement.slick("unslick");
        }
      }
    }
  });
});
