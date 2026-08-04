# def index(request):
#     hero_slides = HeroSlide.objects.filter(is_active=True)
#     festival_banners = FestivalBanner.objects.filter(is_active=True)
#     testimonials = Testimonial.objects.filter(is_active=True)

#     featured_categories = Category.objects.filter(
#         is_active=True,
#         parent=None
#     )[:8]

#     featured_products = with_rating_annotations(
#         Product.objects.filter(
#             is_active=True,
#             is_bestseller=True
#         )
#         .select_related("category")
#         .prefetch_related("images")
#     )[:6]

#     context = {
#         "hero_slides": hero_slides,
#         "featured_categories": featured_categories,
#         "featured_products": featured_products,
#         "festival_banners": festival_banners,
#         "testimonials": testimonials,
#     }

#     return render(request, "homepage/index.html", context)

# from django.shortcuts import render
# from categories.models import Category
# from .models import HeroSlide, FestivalBanner, Testimonial

# def index(request):
#     hero_slides = HeroSlide.objects.filter(is_active=True)
#     festival_banners = FestivalBanner.objects.filter(is_active=True)
#     testimonials = Testimonial.objects.filter(is_active=True)
#     featured_categories = Category.objects.filter(
#         is_active=True,
#         parent=None
#     )[:8]

#     return render(request, "homepage/index.html", {
#         "hero_slides": hero_slides,
#         "festival_banners": festival_banners,
#         "testimonials": testimonials,
#         "featured_categories": featured_categories,
#     })

from django.shortcuts import render
from .models import HeroSlide, FestivalBanner
from categories.models import Category

def index(request):
    hero_slides = HeroSlide.objects.filter(is_active=True)

    featured_categories = Category.objects.filter(
        is_active=True,
        parent=None
    )[:8]

    festival_banners = FestivalBanner.objects.filter(
        is_active=True
    )

    return render(request, "homepage/index.html", {
        "hero_slides": hero_slides,
        "featured_categories": featured_categories,
        "festival_banners": festival_banners,
    })