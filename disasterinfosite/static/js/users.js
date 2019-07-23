function sendAjaxAuthRequest(url, data) {
  var object = {
    next: document.location.pathname
  };
  data.forEach(function(value, key){
    object[key] = value;
  });

  var getCookie = function(name) {
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
  var csrftoken = getCookie("csrftoken");

  return $.ajax({
    crossDomain: false,
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    type: "POST",
    url: url,
    data: JSON.stringify(data)
  });
}

function formInputsAreValid($formSelector) {
  var inputs = $formSelector.find("input:visible");
  inputs.forEach(function(input) {
    if (!input.checkValidity()) {
      console.log(inputs[i], "invalid");
      return false;
    }
  });
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
  var $signupForm = $("#user-signup__form");
  var $loginForm = $("#user-login__form");
  var $updateForm = $("#user-profile__form");

  var $userButtonContainer = $("#user-button-container");
  var $failureContainer = $("#failure-container");
  var $userSignupContainer = $("#failure-container");
  var $userLoginContainer = $("#user-login-container");
  var $userProfileContainer = $("#user-profile-container");
  var $userInfoContainer = $("#user-info-container");

  $(".button--signup").click(function(event) {
    event.preventDefault();
    $userButtonContainer.hide();
    $failureContainer.hide();
    $userSignupContainer.show();
  });

  $(".button--login").click(function(event) {
    event.preventDefault();
    $userButtonContainer.hide();
    $("#user-info-container--invalid").hide();
    $failureContainer.hide();
    $userLoginContainer.show();
  });

  $(".button--cancel").click(function(event) {
    event.preventDefault();
    $userSignupContainer.hide();
    $userLoginContainer.hide();
    $userButtonContainer.show();
  });

  $(".button--cancel-update").click(function(event) {
    event.preventDefault();
    $userProfileContainer.hide();
    $userInfoContainer.show();
  });

  $(".button--update").click(function(event) {
    event.preventDefault();
    $userInfoContainer.hide();
    $("#user-button-container--logged-in").hide();
    $failureContainer.hide();
    $userProfileContainer.show();
  });

  requiredFocus($("#user-signup__username"));
  requiredFocus($("#user-signup__password"));
  requiredBlur($("#user-signup__username"), "Valid email address required.");
  requiredBlur($("#user-signup__password"), "Required");

  $(".button--logout").click(function(event) {
    event.preventDefault();
    sendAjaxAuthRequest("accounts/logout/")
      .then(function() {
        location.reload(true);
      })
      .catch(function(error) {
        $userInfoContainer.hide();
        $("#user-button-container--logged-in").hide();
        $failureContainer.show();
      });
  });

  $signupForm.submit(function(event) {
    event.preventDefault();

    if (!formInputsAreValid($signupForm)) {
      return false;
    }

    sendAjaxAuthRequest("accounts/create_user/", new FormData($signupForm[0]))
    .then(function() {
      $("#user-signup-result-container").show();
    })
    .catch(function(err) {
      $failureContainer.show();
    })
    .always(function() {
      $userSignupContainer.hide();
    });
  });

  $loginForm.submit(function(event) {
    event.preventDefault();
    if (!formInputsAreValid($loginForm)) {
      return false;
    }

    sendAjaxAuthRequest("accounts/login/", new FormData($loginForm[0]))
      .then(function() {
        location.hash = "user-interaction-container";
        location.reload(true);
      })
      .catch(function(error) {
        $userLoginContainer.hide();
        $("#user-info-container--invalid").show();
      });
  });

  $updateForm.submit(function(event) {
    event.preventDefault();
    if (!formInputsAreValid($updateForm)) {
      return false;
    }

    sendAjaxAuthRequest("accounts/update_profile/", new FormData($updateForm[0]))
      .then(function() {
        $("#user-profile-result-container").show();
      })
      .catch(function(err) {
        $failureContainer.show();
      })
      .always(function() {
        $userProfileContainer.hide();
      });
  });
});
