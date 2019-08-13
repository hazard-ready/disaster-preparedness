require("slick-carousel/slick/slick.css");
require("slick-carousel/slick/slick-theme.css");

require("slick-carousel");


$(document).ready(function() {
  // Set up expanding and collapsing sections. Set up slideshow
  // in applicable sections when they are expanded.
  var collapseSectionClass = "section-content--collapse";
  var caretUpClass = "caret--up";

  $(".section-title").on("click", function(event) {
    var $sectionTitle = $(event.delegateTarget);
    var contentSectionId = $sectionTitle.data("section");
    if (contentSectionId) {
      var $contentSection = $("#" + contentSectionId);
      var $titleCaret = $sectionTitle.find(".caret");
      var $currentSlideElement = $("#" + contentSectionId + " .past-photos");

      if ($contentSection.hasClass(collapseSectionClass)) {
        $contentSection.removeClass(collapseSectionClass);
        $titleCaret.addClass(caretUpClass);

        if ($currentSlideElement) {
          $currentSlideElement.slick({
            slidesToShow: 1,
            variableWidth: false
          });
        }
      } else {
        $contentSection.addClass(collapseSectionClass);
        $titleCaret.removeClass(caretUpClass);
        if ($currentSlideElement) {
          $currentSlideElement.slick("unslick");
        }
      }
    }
  });
});
