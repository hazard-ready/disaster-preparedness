// Signup and login functionality

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

  $(".button--logout").click(function() {
    sendAjaxAuthRequest(
      "accounts/logout/",
      { next: "/" },
      function() {
        $("#user-info-container").hide();
        $("#user-button-container--logged-in").hide();
        $("#failure-container").show();
      },
      function() {
        $("#user-info-container").hide();
        $("#user-button-container--logged-in").hide();
        $("#failure-container").hide();
        $("#user-button-container").show();
      }
    );
  });

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

  requiredFocus($("#user-signup__username"));
  requiredFocus($("#user-signup__password"));
  requiredBlur($("#user-signup__username"), "Valid email address required.");
  requiredBlur($("#user-signup__password"), "Required");
  setValueOnFocus($("#user-signup__state"), "MT");
  setValueOnFocus($("#user-signup__zip"), "598");

  var sendAjaxAuthRequest = function(url, data, error, success) {
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
    $.ajaxSetup({
      crossDomain: false,
      beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    });
    $.ajax({
      type: "POST",
      url: url,
      data: data,
      error: error,
      success: success
    });
  };

  $("#user-signup__submit").click(function() {
    var inputs = $("#user-signup__form").find("input:visible");
    for (var i = 0; i < inputs.length; i++) {
      if (!inputs[i].checkValidity()) {
        return false;
      }
    }

    var username = $("#user-signup__username").val();
    var password = $("#user-signup__password").val();
    var address1 = $("#user-signup__address1").val();
    var address2 = $("#user-signup__address2").val();
    var city = $("#user-signup__city").val();
    var state = $("#user-signup__state").val();
    var zip = $("#user-signup__zip").val();

    sendAjaxAuthRequest(
      "accounts/create_user/",
      {
        username: username,
        password: password,
        address1: address1,
        address2: address2,
        city: city,
        state: state,
        zip_code: zip,
        next: document.location.pathname
      },
      function(err) {
        $("#user-signup-container").hide();
        $("#failure-container").show();
      },
      function() {
        $("#user-signup-container").hide();
        $("#user-signup-result-container").show();
      }
    );
  });

  $("#user-login__submit").click(function() {
    var inputs = $("#user-login__form").find("input:visible");
    for (var i = 0; i < inputs.length; i++) {
      if (!inputs[i].checkValidity()) {
        return false;
      }
    }
    var username = $("#user-login__username").val();
    var password = $("#user-login__password").val();

    sendAjaxAuthRequest(
      "accounts/login/",
      {
        username: username,
        password: password,
        next: document.location.pathname
      },
      function() {
        $("#user-login-container").hide();
        $("#user-info-container--invalid").show();
      },
      function() {
        document.location.hash = "user-interaction-container";
        document.location.reload(true);
        $("#user-login-container").hide();
        $("#user-info-container").show();
      }
    );
  });

  $("#user-profile__submit").click(function() {
    var inputs = $("#user-profile__form").find("input:visible");
    for (var i = 0; i < inputs.length; i++) {
      if (!inputs[i].checkValidity()) {
        return false;
      }
    }
    var address1 = $("#user-profile__address1").val();
    var address2 = $("#user-profile__address2").val();
    var city = $("#user-profile__city").val();
    var state = $("#user-profile__state").val();
    var zip = $("#user-profile__zip").val();

    sendAjaxAuthRequest(
      "accounts/update_profile/",
      {
        address1: address1,
        address2: address2,
        city: city,
        state: state,
        zip_code: zip,
        next: document.location.pathname
      },
      function(err) {
        $("#user-profile-container").hide();
        $("#failure-container").show();
      },
      function() {
        $("#user-profile-container").hide();
        $("#user-profile-result-container").show();
      }
    );
  });
});
