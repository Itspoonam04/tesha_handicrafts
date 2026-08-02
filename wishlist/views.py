from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from products.models import Product

from .models import WishlistItem
from .wishlist import get_wishlist


def wishlist_detail(request):
    wishlist = get_wishlist(request)
    items = wishlist.items.select_related("product").prefetch_related("product__images")
    context = {"items": items}
    return render(request, "wishlist/detail.html", context)


@require_POST
def wishlist_toggle(request, product_id):
    """
    AJAX endpoint: adds the product if not present, removes it if present.
    Returns JSON so the front-end can update the heart icon and navbar
    badge without a full page reload.
    """
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    wishlist = get_wishlist(request)

    item = WishlistItem.objects.filter(wishlist=wishlist, product=product).first()
    if item:
        item.delete()
        added = False
    else:
        WishlistItem.objects.create(wishlist=wishlist, product=product)
        added = True

    return JsonResponse({"added": added, "count": wishlist.items.count()})
