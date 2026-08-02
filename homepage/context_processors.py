"""
Site-wide template context. Available in EVERY template.
"""

from cart.cart import get_cart_item_count
from categories.models import Category
from wishlist.wishlist import get_wishlist_item_count, get_wishlist_product_ids

from .models import SiteSettings


def site_globals(request):
    nav_categories = Category.objects.filter(is_active=True, parent=None)
    site_settings = SiteSettings.load()

    return {
        "nav_categories": nav_categories,
        "site_settings": site_settings,
        "cart_item_count": get_cart_item_count(request),
        "wishlist_item_count": get_wishlist_item_count(request),
        "wishlist_product_ids": get_wishlist_product_ids(request),
    }
