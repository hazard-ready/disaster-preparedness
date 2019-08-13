// IE11 polyfills
require("native-promise-only");
require("formdata-polyfill");

function getCookie(name) {
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
};

function sendAjaxAuthRequest(url, data) {
  var object = {
    next: document.location.pathname
  };

  if(data) {
    data.forEach(function(value, key){
      object[key] = value;
    });
  }

  var csrftoken = getCookie("csrftoken");

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
  var $signupForm = $("#user-signup__form");
  var $loginForm = $("#user-login__form");
  var $updateForm = $("#user-profile__form");

  var $userButtonContainer = $("#user-button-container");
  var $failureContainer = $("#failure-container");
  var $userSignupContainer = $("#user-signup-container");
  var $userLoginContainer = $("#user-login-container");
  var $userProfileContainer = $("#user-profile-container");
  var $userInfoContainer = $("#user-info-container");

  $(".button--signup").click(function(event) {
    event.preventDefault();
    $userButtonContainer.addClass('hide');
    $failureContainer.addClass('hide');
    $userSignupContainer.removeClass('hide');;
  });

  $(".button--login").click(function(event) {
    event.preventDefault();
    $userButtonContainer.addClass('hide');
    $("#user-info-container--invalid").addClass('hide');
    $failureContainer.addClass('hide');
    $userLoginContainer.removeClass('hide');;
  });

  $(".button--cancel").click(function(event) {
    event.preventDefault();
    $userSignupContainer.addClass('hide');
    $userLoginContainer.addClass('hide');
    $userButtonContainer.removeClass('hide');;
  });

  $(".button--cancel-update").click(function(event) {
    event.preventDefault();
    $userProfileContainer.addClass('hide');
    $userInfoContainer.removeClass('hide');;
  });

  $(".button--update").click(function(event) {
    event.preventDefault();
    $userInfoContainer.addClass('hide');
    $("#user-button-container--logged-in").addClass('hide');
    $failureContainer.addClass('hide');
    $userProfileContainer.removeClass('hide');;
  });

  requiredFocus($("#user-signup__username"));
  requiredFocus($("#user-signup__password"));
  requiredBlur($("#user-signup__username"), "Valid email address required.");
  requiredBlur($("#user-signup__password"), "Required");

  $(".button--logout").click(function(event) {
    event.preventDefault();
    sendAjaxAuthRequest("accounts/logout/")
      .done(function() {
        location.reload(true);
      })
      .fail(function(error) {
        console.error('Logout error:', error)
        $userInfoContainer.addClass('hide');
        $("#user-button-container--logged-in").addClass('hide');
        $failureContainer.removeClass('hide');
      });
  });

  $signupForm.submit(function(event) {
    event.preventDefault();

    sendAjaxAuthRequest("accounts/create_user/", new FormData($signupForm[0]))
    .done(function() {
      $("#user-signup-result-container").removeClass('hide');;
    })
    .fail(function(error) {
      console.error("signup form error:", error)
      $failureContainer.removeClass('hide');
    })
    .always(function() {
      $userSignupContainer.addClass('hide');
    });
  });

  $loginForm.submit(function(event) {
    event.preventDefault();

    sendAjaxAuthRequest("accounts/login/", new FormData($loginForm[0]))
      .done(function() {
        location.hash = "user-interaction-container";
        location.reload(true);
      })
      .fail(function(error) {
        console.error("login form error:", error)
        $userLoginContainer.addClass('hide');
        $("#user-info-container--invalid").removeClass('hide');;
      });
  });

  $updateForm.submit(function(event) {
    event.preventDefault();

    sendAjaxAuthRequest("accounts/update_profile/", new FormData($updateForm[0]))
      .done(function() {
        $("#user-profile-result-container").removeClass('hide');;
      })
      .fail(function(error) {
        console.error("update form error:", error)
        $failureContainer.removeClass('hide');
      })
      .always(function() {
        $userProfileContainer.addClass('hide');
      });
  });
});
