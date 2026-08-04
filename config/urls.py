"""
Root URL configuration for Tesha Handicrafts.

Each app owns its own urls.py and is included here under a clear
prefix. As sections are built, uncomment/add the relevant include().
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # Homepage lives at the site root.
    path("", include("homepage.urls")),

    # Catalog
    path("products/", include("products.urls")),
    path("categories/", include("categories.urls")),

    # Account & auth
    path("accounts/", include("accounts.urls")),

    # Shopping
    path("cart/", include("cart.urls")),
    path("wishlist/", include("wishlist.urls")),
    path("orders/", include("orders.urls")),
    path("coupons/", include("coupons.urls")),
    path("payments/", include("payments.urls")),
    path("customize/", include("customization.urls")),

    # Reviews (nested under products in practice, own app for logic)
    path("reviews/", include("reviews.urls")),

    # Seller/admin-facing dashboard (distinct from Django admin)
    path("dashboard/", include("dashboard.urls")),
]

# Serve user-uploaded media locally in development only.
# In production, media is served by nginx/S3/etc., not Django.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)