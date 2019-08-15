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

function sendAjaxAuthRequest(url, data) {
  var object = {
    next: document.location.pathname
  };

  if (data) {
    data.forEach(function(value, key) {
      object[key] = value;
    });
  }

  var csrftoken = getCsrfFromCookie();

  return $.ajax({
    crossDomain: false,
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    type: "POST",
    url: url,
    data: object
  });
}

module.exports = {
  sendAjaxAuthRequest: sendAjaxAuthRequest,
  debounce: debounce
};
