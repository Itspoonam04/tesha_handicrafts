/**
 * Tesha Handicrafts — main.js
 * ---------------------------
 * All site JavaScript lives here (or in additional files loaded from
 * base.html's {% block extra_js %}). No inline <script> blocks or
 * inline event handlers (onclick="...") are used anywhere in the
 * templates, per project coding rules.
 */

document.addEventListener("DOMContentLoaded", function () {
    initWishlistToggles();
});

/**
 * Reads Django's CSRF token from the csrftoken cookie, for use in
 * AJAX requests (fetch() doesn't automatically include it the way
 * a <form> with {% csrf_token %} does).
 */
function getCsrfToken() {
    var match = document.cookie.match(/(^|;\s*)csrftoken=([^;]+)/);
    return match ? match[2] : "";
}

/**
 * Wires up the heart/wishlist icon on product cards and the product
 * detail page. Sends a POST to /wishlist/toggle/<product_id>/ and
 * updates the icon + navbar badge based on the JSON response —
 * no full page reload needed.
 */
function initWishlistToggles() {
    var toggles = document.querySelectorAll(".tesha-wishlist-toggle");

    toggles.forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            event.stopPropagation();

            var productId = button.getAttribute("data-product-id");
            if (!productId) {
                return;
            }

            fetch("/wishlist/toggle/" + productId + "/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCsrfToken(),
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    var icon = button.querySelector("i");

                    if (data.added) {
                        icon.classList.remove("bi-heart");
                        icon.classList.add("bi-heart-fill");
                        icon.style.color = "var(--tesha-terracotta)";
                    } else {
                        icon.classList.remove("bi-heart-fill");
                        icon.classList.add("bi-heart");
                        icon.style.color = "";
                    }

                    updateWishlistBadge(data.count);
                })
                .catch(function () {
                    // Network/server error — fail silently rather than
                    // breaking the page; the icon simply won't update.
                });
        });
    });
}

/**
 * Updates (or adds/removes) the small count badge on the navbar
 * wishlist icon after a toggle, in both the desktop and mobile nav.
 */
function updateWishlistBadge(count) {
    var wishlistLinks = document.querySelectorAll('a[aria-label="Wishlist"]');

    wishlistLinks.forEach(function (link) {
        var badge = link.querySelector(".tesha-icon-badge");

        if (count > 0) {
            if (!badge) {
                badge = document.createElement("span");
                badge.className = "tesha-icon-badge";
                link.appendChild(badge);
            }
            badge.textContent = count;
        } else if (badge) {
            badge.remove();
        }
    });
}
