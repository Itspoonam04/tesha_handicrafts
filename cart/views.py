from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product

from .cart import get_cart
from .models import CartItem


def cart_detail(request):
    cart = get_cart(request)
    items = cart.items.select_related("product").prefetch_related("product__images")
    context = {"cart": cart, "items": items}
    return render(request, "cart/detail.html", context)


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    quantity = int(request.POST.get("quantity", 1))
    quantity = max(quantity, 1)

    cart = get_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})
    if not created:
        item.quantity += quantity
        item.save()

    messages.success(request, f"Added \u201c{product.name}\u201d to your cart.")

    next_url = request.POST.get("next") or "cart:detail"
    return redirect(next_url)


@require_POST
def cart_update(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)

    quantity = int(request.POST.get("quantity", 1))
    if quantity <= 0:
        item.delete()
        messages.info(request, f"Removed \u201c{item.product.name}\u201d from your cart.")
    else:
        item.quantity = quantity
        item.save()
        messages.success(request, "Cart updated.")

    return redirect("cart:detail")


@require_POST
def cart_remove(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    product_name = item.product.name
    item.delete()
    messages.info(request, f"Removed \u201c{product_name}\u201d from your cart.")
    return redirect("cart:detail")
