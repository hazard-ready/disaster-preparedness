function sendAjaxAuthRequest(url, data) {
  var getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = $.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };
  var csrftoken = getCookie("csrftoken");

  return $.ajax({
    crossDomain: false,
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    type: "POST",
    url: url,
    data: data
  });
}

function formInputsAreValid($formSelector) {
  var inputs = $formSelector.find("input:visible");
  for (var i = 0; i < inputs.length; i++) {
    if (!inputs[i].checkValidity()) {
      console.log(inputs[i], "invalid");
      return false;
    }
  }
  return true;
}

function setValueOnFocus(el, value) {
  el.focus(function() {
    if (el.val() === "") {
      el.val(value);
    }
  });
}

function requiredFocus(el) {
  el.focus(function() {
    el.removeAttr("placeholder");
  });
}

function requiredBlur(el, text) {
  el.blur(function() {
    if (el.val() === "") {
      el.attr("placeholder", text);
    }
  });
}

$(document).ready(function() {
  $(".button--signup").click(function() {
    $("#user-button-container").hide();
    $("#failure-container").hide();
    $("#user-signup-container").show();
  });

  $(".button--login").click(function() {
    $("#user-button-container").hide();
    $("#user-info-container--invalid").hide();
    $("#failure-container").hide();
    $("#user-login-container").show();
  });

  $(".button--cancel").click(function() {
    $("#user-signup-container").hide();
    $("#user-login-container").hide();
    $("#user-button-container").show();
  });

  $(".button--cancel-update").click(function() {
    $("#user-profile-container").hide();
    $("#user-info-container").show();
  });

  $(".button--update").click(function() {
    $("#user-info-container").hide();
    $("#user-button-container--logged-in").hide();
    $("#failure-container").hide();
    $("#user-profile-container").show();
  });

  requiredFocus($("#user-signup__username"));
  requiredFocus($("#user-signup__password"));
  requiredBlur($("#user-signup__username"), "Valid email address required.");
  requiredBlur($("#user-signup__password"), "Required");

  // You can use these if the area this app covers makes them useful
  setValueOnFocus($("#user-signup__state"), "MT");
  setValueOnFocus($("#user-signup__zip"), "598");

  $(".button--logout").click(function(event) {
    event.preventDefault();
    sendAjaxAuthRequest("accounts/logout/")
      .then(function() {
        location.reload(true);
      })
      .catch(function(error) {
        $("#user-info-container").hide();
        $("#user-button-container--logged-in").hide();
        $("#failure-container").show();
      });
  });

  $(".user-signup__submit").click(function(event) {
    event.preventDefault();

    if (!formInputsAreValid($("#user-signup__form"))) {
      return false;
    }

    sendAjaxAuthRequest("accounts/create_user/", {
      username: $("#user-signup__username").val(),
      password: $("#user-signup__password").val(),
      address1: $("#user-signup__address1").val(),
      address2: $("#user-signup__address2").val(),
      city: $("#user-signup__city").val(),
      state: $("#user-signup__state").val(),
      zip_code: $("#user-signup__zip").val(),
      next: document.location.pathname
    })
      .then(function() {
        $("#user-signup-result-container").show();
      })
      .catch(function(err) {
        $("#failure-container").show();
      })
      .always(function() {
        $("#user-signup-container").hide();
      });
  });

  $(".user-login__submit").click(function(event) {
    event.preventDefault();
    if (!formInputsAreValid($("#user-login__form"))) {
      return false;
    }

    sendAjaxAuthRequest("accounts/login/", {
      username: $("#user-login__username").val(),
      password: $("#user-login__password").val()
    })
      .then(function() {
        location.hash = "user-interaction-container";
        location.reload(true);
      })
      .catch(function(error) {
        $("#user-login-container").hide();
        $("#user-info-container--invalid").show();
      });
  });

  $(".user-profile__submit").click(function(event) {
    event.preventDefault();
    if (!formInputsAreValid($("#user-profile__form"))) {
      return false;
    }

    sendAjaxAuthRequest("accounts/update_profile/", {
      address1: $("#user-profile__address1").val(),
      address2: $("#user-profile__address2").val(),
      city: $("#user-profile__city").val(),
      state: $("#user-profile__state").val(),
      zip_code: $("#user-profile__zip").val(),
      next: document.location.pathname
    })
      .then(function() {
        $("#user-profile-result-container").show();
      })
      .catch(function(err) {
        $("#failure-container").show();
      })
      .always(function() {
        $("#user-profile-container").hide();
      });
  });
});
