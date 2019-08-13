require("normalize.css/normalize.css");
require("../style/app.scss");

require("./sections");

// images
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

function highlightMenu($itemTitle) {
  $prepareContentItems.removeClass("prepare-content__item--active");
  $itemTitle.addClass("prepare-content__item--active");
}

function showItemDetail(detailId) {
  var $detail = $(detailId);

  highlightMenu($('[data-item="' + detailId.slice(1) + '"]'));

  // hide all of the item detail elements but this one
  $prepareItems.addClass("hide");
  $detail.removeClass("hide");
}

$(document).ready(function() {
  $prepareContentItems.click(function(event) {
    var $itemTitle = $(event.delegateTarget);

    highlightMenu($itemTitle);

    var itemDetailId = $itemTitle.data("item");
    if (itemDetailId) {
      showItemDetail("#" + itemDetailId);
    }
  });

  if (anchor) {
    showItemDetail(anchor);

    // Open the relevant collapsible panel on the left and close all others
    var collapseSectionClass = "section-content--collapse";
    var caretUpClass = "caret--up";
    $(".section-content").addClass(collapseSectionClass);
    $(".caret").removeClass(caretUpClass);
    var sectionId = $(anchor).data("section");
    var $titleCaret = $('[data-section="' + sectionId + '"]').find(".caret");
    var $contentSection = $("#" + sectionId);
    $contentSection.removeClass(collapseSectionClass);
    $titleCaret.addClass(caretUpClass);
  }

  $(".print-button").click(function() {
    window.print();
    return false;
  });
});
