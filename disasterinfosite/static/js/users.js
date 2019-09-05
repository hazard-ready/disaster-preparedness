// IE11 polyfills
require("native-promise-only");
require("formdata-polyfill");

var utils = require("./utils");

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

function sendAjaxAuthRequest(url, data) {
  var object = {
    next: document.location.pathname
  };

  if (data) {
    data.forEach(function(value, key) {
      object[key] = value;
    });
  }

  var csrftoken = utils.getCsrfFromCookie();

  return $.ajax({
    crossDomain: false,
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    method: "POST",
    url: url,
    data: object
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
    $userSignupContainer.removeClass('hide');
    $('#user-signup__username').focus();
  });

  $(".button--login").click(function(event) {
    event.preventDefault();
    $userButtonContainer.addClass('hide');
    $("#user-info-container--invalid").addClass('hide');
    $failureContainer.addClass('hide');
    $userLoginContainer.removeClass('hide');;
    $('#user-login__username').focus();
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
    $userProfileContainer.removeClass('hide');
    $('#user-profile__address1').focus();
  });

  requiredFocus($("#user-signup__username"));
  requiredFocus($("#user-signup__password"));
  requiredBlur($("#user-signup__username"), "Valid email address required.");
  requiredBlur($("#user-signup__password"), "Required");

  $(".button--logout").click(function(event) {
    event.preventDefault();
    sendAjaxAuthRequest(logoutApiUrl)
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

    sendAjaxAuthRequest(createUserApiUrl, new FormData($signupForm[0]))
    .done(function() {
      $("#user-signup-result-container").removeClass('hide').focus();
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

    sendAjaxAuthRequest(loginApiUrl, new FormData($loginForm[0]))
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

    sendAjaxAuthRequest(updateProfileApiUrl, new FormData($updateForm[0]))
      .done(function() {
        $("#user-profile-result-container").removeClass('hide').focus();
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
