from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, render

from .models import Product


def with_rating_annotations(queryset):
    """
    Shared helper: annotate a Product queryset with average_rating and
    review_count computed from approved reviews only. Used by the
    homepage, product list, and product detail views so rating display
    logic lives in one place.
    """
    return queryset.annotate(
        average_rating=Avg("reviews__rating", filter=Q(reviews__is_approved=True)),
        review_count=Count("reviews", filter=Q(reviews__is_approved=True), distinct=True),
    )


def product_list(request):
    products = with_rating_annotations(
        Product.objects.filter(is_active=True).select_related("category").prefetch_related("images")
    )

    category_slug = request.GET.get("category")
    if category_slug:
        products = products.filter(category__slug=category_slug)

    query = request.GET.get("q")
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(short_description__icontains=query)
        )

    context = {
        "products": products,
        "search_query": query or "",
    }
    return render(request, "products/list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(
        with_rating_annotations(Product.objects.filter(is_active=True)).select_related("category"),
        slug=slug,
    )
    reviews = product.reviews.filter(is_approved=True)

    related_products = with_rating_annotations(
        Product.objects.filter(is_active=True, category=product.category)
        .exclude(pk=product.pk)
        .select_related("category")
        .prefetch_related("images")
    )[:4]

    context = {
        "product": product,
        "reviews": reviews,
        "related_products": related_products,
    }
    return render(request, "products/detail.html", context)

from django.shortcuts import get_object_or_404, render
from homepage.models import FestivalBanner
from .models import Product


def festival_products_view(request, slug):
  banner = get_object_or_404(FestivalBanner, slug=slug)
  products = Product.objects.filter(festival_collection=banner)

  context = {'banner': banner, 'products': products}
  return render(request, 'products/festival_list.html', context)