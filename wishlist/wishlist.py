"""Shared wishlist helpers — mirrors cart/cart.py's pattern."""

from .models import Wishlist


def get_wishlist(request):
    if not request.session.session_key:
        request.session.create()

    wishlist, _ = Wishlist.objects.get_or_create(session_key=request.session.session_key)
    return wishlist


def get_wishlist_item_count(request):
    session_key = request.session.session_key
    if not session_key:
        return 0

    try:
        wishlist = Wishlist.objects.get(session_key=session_key)
    except Wishlist.DoesNotExist:
        return 0

    return wishlist.items.count()


def get_wishlist_product_ids(request):
    """Used to pre-fill heart icons as 'filled' on page load."""
    session_key = request.session.session_key
    if not session_key:
        return set()

    try:
        wishlist = Wishlist.objects.get(session_key=session_key)
    except Wishlist.DoesNotExist:
        return set()

    return set(wishlist.items.values_list("product_id", flat=True))
