// IE11 polyfills
require("native-promise-only");
require("formdata-polyfill");

var utils = require("./utils");

var $userInfoContainer = $("#user-info-container");

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

  $userInfoContainer.empty()
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
  var $userSignupContainer = $("#user-signup-container");
  var $userLoginContainer = $("#user-login-container");
  var $userProfileContainer = $("#user-profile-container");

  $(".button--signup").click(function(event) {
    event.preventDefault();
    $userButtonContainer.addClass('hide');
    $userSignupContainer.removeClass('hide');
    $('#user-signup__username').focus();
  });

  $(".button--login").click(function(event) {
    event.preventDefault();
    $userButtonContainer.addClass('hide');
    $userLoginContainer.removeClass('hide');;
    $('#user-login__username').focus();
  });

  $(".button--cancel").click(function(event) {
    event.preventDefault();
    $userSignupContainer.addClass('hide');
    $userLoginContainer.addClass('hide');
    $userButtonContainer.removeClass('hide');
    $userInfoContainer.addClass('hide');
  });

  $(".button--cancel-update").click(function(event) {
    event.preventDefault();
    $userProfileContainer.addClass('hide');
    $userInfoContainer.removeClass('hide');
    $userButtonContainer.removeClass('hide');
    $userInfoContainer.addClass('hide');
  });

  $(".button--update").click(function(event) {
    event.preventDefault();
    $userInfoContainer.addClass('hide');
    $userButtonContainer.addClass('hide');
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
        $(".login-welcome").addClass('hide');
      });
  });

  $signupForm.submit(function(event) {
    event.preventDefault();

    sendAjaxAuthRequest(createUserApiUrl, new FormData($signupForm[0]))
    .done(function(data) {
      $userInfoContainer.append(data).removeClass('hide').focus();
      $userSignupContainer.addClass('hide');
    })
    .fail(function(request, status, error) {
      $userInfoContainer.append(request.responseText).removeClass('hide').focus();
    })
  });

  $loginForm.submit(function(event) {
    event.preventDefault();
    sendAjaxAuthRequest(loginApiUrl, new FormData($loginForm[0]))
      .done(function(data) {
        location.reload(true);
        $userInfoContainer.append(data).removeClass('hide').focus();
      })
      .fail(function(request, status, error) {
        console.error("login form error:", error, "status:", status);
      });
  });

  $updateForm.submit(function(event) {
    event.preventDefault();

    sendAjaxAuthRequest(updateProfileApiUrl, new FormData($updateForm[0]))
      .done(function(data) {
        $userInfoContainer.append(data).removeClass('hide').focus();
        $userProfileContainer.addClass('hide');
      })
      .fail(function(request, status, error) {
        $userInfoContainer.append(request.responseText).removeClass('hide').focus();
      })
  });
});
