function getCsrfFromCookie() {
  var name = "csrftoken";
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    cookies.forEach(function(cookie) {
      cookie = cookie.trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        return cookieValue;
      }
    });
  }
  return cookieValue;
}

// stolen straight from underscore, but we don't need a whole library for this.
function debounce(func, wait, immediate) {
  var timeout;
  return function() {
    var context = this,
      args = arguments;
    var later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    var callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
}


function lazyLoadVideos() {
  $(".video").each(function(idx) {
    var self = $(this);
    var embedCode = self.data("embed");
    // Load the video preview thumbnails asynchronously
    var preview = new Image();
    preview.src = "https://img.youtube.com/vi/" + embedCode + "/sddefault.jpg";
    preview.alt = "";
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

module.exports = {
  getCsrfFromCookie: getCsrfFromCookie,
  debounce: debounce,
  lazyLoadVideos: lazyLoadVideos
};
