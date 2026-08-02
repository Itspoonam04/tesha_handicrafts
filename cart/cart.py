"""
Shared cart helpers. Import get_cart()/get_cart_item_count() from here
rather than duplicating session logic across views and context
processors.
"""

from .models import Cart


def get_cart(request):
    """Get (or create) the Cart tied to the current session."""
    if not request.session.session_key:
        request.session.create()

    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def get_cart_item_count(request):
    """Cheap count for the navbar badge — avoids building a full Cart object."""
    session_key = request.session.session_key
    if not session_key:
        return 0

    try:
        cart = Cart.objects.get(session_key=session_key)
    except Cart.DoesNotExist:
        return 0

    return cart.total_items
