// prepare page
require("../img/basic_kit.jpg");
require("../img/icon-happy.svg");
require("../img/icon-useful.svg");
require("../img/icon-home.svg");
require("../img/icon-print.svg");
require("../img/icon-check.svg");
require("../img/icon-money.svg");

// get the hash, if there is one
var anchor = window.location.hash;

var $prepareItems = $(".prepare-item");
var $prepareContentItems = $(".prepare-content__item");

function showItemDetail(detailId) {
  var $detail = $(detailId);

  $prepareContentItems.removeClass("prepare-content__item--active");
  $('[data-item="' + detailId.slice(1) + '"]').addClass(
    "prepare-content__item--active"
  );

  // hide all of the item detail elements but this one
  $prepareItems.addClass("hide");
  $detail.removeClass("hide");
}

$(document).ready(function() {
  $prepareContentItems.click(function(event) {
    $prepareContentItems.removeClass("prepare-content__item--active");
    var $itemTitle = $(event.delegateTarget);
    $itemTitle.addClass("prepare-content__item--active");
    var itemDetailId = $itemTitle.data("item");
    if (itemDetailId) {
      showItemDetail("#" + itemDetailId);
    }
  });

  if (anchor) {
    showItemDetail(anchor);

    // Open the relevant collapsible panel on the left and close all others
    $(".section-content").addClass("section-content--collapse");
    $(".caret").removeClass("caret--up");
    var sectionId = $(anchor).data("section");
    var $sectionTitle = $('[data-section="' + sectionId + '"]');
    var $contentSection = $("#" + sectionId);
    var $titleCaret = $sectionTitle.find(".caret");
    $contentSection.removeClass("section-content--collapse");
    $titleCaret.addClass("caret--up");
  }
});
