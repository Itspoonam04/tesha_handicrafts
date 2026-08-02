/**
 * Homepage testimonials — video play buttons.
 * If a testimonial has an uploaded video file, play it inline.
 * If it only has an embed URL (e.g. YouTube), open it in a new tab.
 */
document.addEventListener("DOMContentLoaded", function () {
    var playButtons = document.querySelectorAll(".tesha-testimonial-play-btn");

    playButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            var wrap = button.closest(".tesha-testimonial-video-wrap");
            var video = wrap ? wrap.querySelector("video") : null;
            var embedUrl = button.getAttribute("data-embed-url");

            if (video) {
                button.style.display = "none";
                video.setAttribute("controls", "true");
                video.play();
            } else if (embedUrl) {
                window.open(embedUrl, "_blank", "noopener");
            }
        });
    });
});
