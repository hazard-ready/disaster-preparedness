$( document ).ready(function() {
  
  $("#location-submit").click(function() {
    
    var selection = $("#location-text").val();
    
    $.getJSON('https://maps.googleapis.com/maps/api/geocode/json?address=' + selection + '&key=AIzaSyBSZGyycuPZO0BBfJqO-RBFeKM7_icZUnk',
      function(data) {
        
        lat = data.results[0].geometry.location.lat;
        lon = data.results[0].geometry.location.lng;
        
        var image_url = "<image src='http://api.tiles.mapbox.com/v4/meesterstump.8bf4e389/pin-s+08B(" + lon + "," + lat + ")/" + lon + "," + lat + ",15/970x300.png64?access_token=pk.eyJ1IjoibWVlc3RlcnN0dW1wIiwiYSI6IkdGVVFTSkkifQ.8_WCPGKmIImxpNy4dEWU1A'>";
        
        $("#map-image").html(image_url);
        
    });
    
  });  

});