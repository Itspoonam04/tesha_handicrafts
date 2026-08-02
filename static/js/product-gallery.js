/**
 * Product detail page — image gallery.
 * Clicking a thumbnail swaps the main product image. No inline
 * onclick handlers are used; everything is wired up here.
 */
document.addEventListener("DOMContentLoaded", function () {
    var mainImage = document.getElementById("mainProductImage");
    var thumbButtons = document.querySelectorAll(".tesha-thumb-btn");

    if (!mainImage || thumbButtons.length === 0) {
        return;
    }

    thumbButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            var newUrl = button.getAttribute("data-image-url");
            if (newUrl) {
                mainImage.setAttribute("src", newUrl);
            }
        });
    });
});
