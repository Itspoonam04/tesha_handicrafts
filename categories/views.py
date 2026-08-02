from django.shortcuts import get_object_or_404, render

from products.views import with_rating_annotations
from products.models import Product

from .models import Category


def category_list(request):
    categories = Category.objects.filter(is_active=True, parent=None)
    context = {"categories": categories}
    return render(request, "categories/list.html", context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)

    products = with_rating_annotations(
        Product.objects.filter(is_active=True, category=category)
        .select_related("category")
        .prefetch_related("images")
    )

    context = {
        "category": category,
        "products": products,
    }
    return render(request, "categories/detail.html", context)
