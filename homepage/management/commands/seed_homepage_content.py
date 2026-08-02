"""
Seeds homepage content: SiteSettings, HeroSlide(s), FestivalBanner(s),
and Testimonial(s), using generated placeholder images (requires
Pillow — already a project dependency).

Usage:
    python manage.py seed_homepage_content

Safe to re-run — uses get_or_create so it won't create duplicates.
"""

import io

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from homepage.models import FestivalBanner, HeroSlide, SiteSettings, Testimonial

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


HERO_SLIDES = [
    {
        "title": "Bring Tradition Home with Handmade Creations",
        "subtitle": "Authentic Indian handicrafts, made by artisans across the country.",
        "cta_text": "Shop Now",
        "cta_url": "/products/",
        "secondary_cta_text": "Customize Your Order",
        "secondary_cta_url": "/customize/",
        "color": (181, 80, 47),
    },
]

FESTIVAL_BANNERS = [
    {"title": "Ganesh Chaturthi", "color": (143, 62, 35)},
    {"title": "Gudi Padwa", "color": (200, 150, 62)},
    {"title": "Diwali Collection", "color": (107, 122, 79)},
    {"title": "Wedding Collection", "color": (181, 80, 47)},
]

TESTIMONIALS = [
    {"name": "Ashwini Deshmukh", "rating": 5, "quote": "Beautiful quality and finishing!", "color": (200, 150, 62)},
    {"name": "Prajakta Kulkarni", "rating": 5, "quote": "Loved the customization and service.", "color": (107, 122, 79)},
    {"name": "Snehal Patil", "rating": 4, "quote": "Perfect for Ganpati Decoration!", "color": (181, 80, 47)},
    {"name": "Rohit More", "rating": 5, "quote": "Top quality products. Highly recommended.", "color": (143, 62, 35)},
]


def make_placeholder_image(text, size=(1200, 700), color=(181, 80, 47)):
    image = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(image)
    draw.text((size[0] // 2, size[1] // 2), text, fill=(255, 255, 255), anchor="mm")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = "Seeds SiteSettings, HeroSlide, FestivalBanner, and Testimonial demo content."

    def handle(self, *args, **options):
        if not PIL_AVAILABLE:
            self.stderr.write(self.style.ERROR("Pillow is not installed. Run: pip install Pillow"))
            return

        SiteSettings.load()
        self.stdout.write(self.style.SUCCESS("Site settings row ready (edit it in /admin/)."))

        for order, slide in enumerate(HERO_SLIDES):
            obj, created = HeroSlide.objects.get_or_create(
                title=slide["title"],
                defaults={
                    "subtitle": slide["subtitle"],
                    "cta_text": slide["cta_text"],
                    "cta_url": slide["cta_url"],
                    "secondary_cta_text": slide["secondary_cta_text"],
                    "secondary_cta_url": slide["secondary_cta_url"],
                    "display_order": order,
                },
            )
            if created:
                obj.image.save(f"hero-{order}.jpg", make_placeholder_image(slide["title"], color=slide["color"]), save=True)
        self.stdout.write(self.style.SUCCESS(f"  {len(HERO_SLIDES)} hero slide(s) ready."))

        for order, banner in enumerate(FESTIVAL_BANNERS):
            obj, created = FestivalBanner.objects.get_or_create(
                title=banner["title"], defaults={"display_order": order},
            )
            if created:
                obj.image.save(
                    f"festival-{order}.jpg",
                    make_placeholder_image(banner["title"], size=(600, 450), color=banner["color"]),
                    save=True,
                )
        self.stdout.write(self.style.SUCCESS(f"  {len(FESTIVAL_BANNERS)} festival banner(s) ready."))

        for order, t in enumerate(TESTIMONIALS):
            obj, created = Testimonial.objects.get_or_create(
                customer_name=t["name"],
                defaults={"rating": t["rating"], "quote": t["quote"], "display_order": order},
            )
            if created:
                obj.photo.save(
                    f"testimonial-{order}.jpg",
                    make_placeholder_image(t["name"], size=(500, 600), color=t["color"]),
                    save=True,
                )
        self.stdout.write(self.style.SUCCESS(f"  {len(TESTIMONIALS)} testimonial(s) ready."))

        self.stdout.write(self.style.SUCCESS("Homepage content seeded. Edit it all in /admin/."))
