"""
Seeds the database with realistic demo data so the storefront and
Django admin are populated out of the box: categories, products
(with generated placeholder images), and reviews.

Usage:
    python manage.py seed_demo_data

Safe to re-run — uses get_or_create so it won't create duplicates.
Replace with real photography and copy via the Django admin whenever
you're ready; this is only meant to unblock local development.
"""

import io
import random

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from categories.models import Category
from products.models import Product, ProductImage
from reviews.models import Review

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


CATEGORY_DATA = [
    {"name": "Wall Decor", "slug": "wall-decor", "color": (143, 62, 35)},
    {"name": "Pottery & Ceramics", "slug": "pottery-ceramics", "color": (107, 122, 79)},
    {"name": "Textiles", "slug": "textiles", "color": (200, 150, 62)},
    {"name": "Jewellery", "slug": "jewellery", "color": (181, 80, 47)},
    {"name": "Home & Living", "slug": "home-living", "color": (143, 62, 35)},
    {"name": "Festive & Gifting", "slug": "festive-gifting", "color": (107, 122, 79)},
]

PRODUCT_DATA = [
    {
        "name": "Hand-painted Madhubani Wall Panel",
        "category_slug": "wall-decor",
        "price": 2499, "compare_at_price": 3199,
        "artisan_name": "Sita Devi", "artisan_state": "Bihar",
        "material": "Handmade paper, natural dyes",
        "is_bestseller": True,
    },
    {
        "name": "Blue Pottery Ceramic Vase",
        "category_slug": "pottery-ceramics",
        "price": 1899, "compare_at_price": None,
        "artisan_name": "Rafiq Khan", "artisan_state": "Rajasthan",
        "material": "Ceramic, quartz powder",
        "is_new_arrival": True,
    },
    {
        "name": "Handwoven Pashmina Stole",
        "category_slug": "textiles",
        "price": 3599, "compare_at_price": 4499,
        "artisan_name": "Ghulam Nabi", "artisan_state": "Kashmir",
        "material": "Pashmina wool",
        "is_bestseller": True,
    },
    {
        "name": "Dhokra Art Brass Figurine",
        "category_slug": "home-living",
        "price": 1299, "compare_at_price": None,
        "artisan_name": "Budhram Jhara", "artisan_state": "Chhattisgarh",
        "material": "Brass, lost-wax casting",
    },
    {
        "name": "Silver Filigree Jhumka Earrings",
        "category_slug": "jewellery",
        "price": 2199, "compare_at_price": 2599,
        "artisan_name": "Manohar Behera", "artisan_state": "Odisha",
        "material": "Sterling silver",
        "is_bestseller": True, "is_customizable": True,
    },
    {
        "name": "Terracotta Diya Gift Set (Set of 6)",
        "category_slug": "festive-gifting",
        "price": 699, "compare_at_price": None,
        "artisan_name": "Kavita Prajapati", "artisan_state": "Gujarat",
        "material": "Terracotta clay",
        "is_new_arrival": True,
    },
    {
        "name": "Block-printed Cotton Bedcover",
        "category_slug": "textiles",
        "price": 1799, "compare_at_price": 2199,
        "artisan_name": "Anokhi Devi", "artisan_state": "Rajasthan",
        "material": "Cotton, natural dyes",
    },
    {
        "name": "Warli Art Wooden Wall Hanging",
        "category_slug": "wall-decor",
        "price": 1599, "compare_at_price": None,
        "artisan_name": "Jivya Soma Mashe Jr.", "artisan_state": "Maharashtra",
        "material": "Mango wood, natural pigment",
        "is_customizable": True,
    },
    {
        "name": "Channapatna Wooden Toy Set",
        "category_slug": "home-living",
        "price": 899, "compare_at_price": None,
        "artisan_name": "Ravi Kumar", "artisan_state": "Karnataka",
        "material": "Ivory wood, lacquer",
        "is_new_arrival": True,
    },
    {
        "name": "Bandhani Silk Dupatta",
        "category_slug": "textiles",
        "price": 2799, "compare_at_price": 3299,
        "artisan_name": "Fatima Khatri", "artisan_state": "Gujarat",
        "material": "Silk",
        "is_bestseller": True,
    },
    {
        "name": "Meenakari Brass Photo Frame",
        "category_slug": "home-living",
        "price": 1099, "compare_at_price": None,
        "artisan_name": "Rajesh Soni", "artisan_state": "Rajasthan",
        "material": "Brass, enamel",
    },
    {
        "name": "Kutch Embroidered Wall Tapestry",
        "category_slug": "wall-decor",
        "price": 2999, "compare_at_price": 3599,
        "artisan_name": "Hansaben Rabari", "artisan_state": "Gujarat",
        "material": "Cotton, mirror work",
        "is_bestseller": True,
    },
]

REVIEW_SAMPLES = [
    ("Ashwini Deshmukh", 5, "Beautiful quality and finishing, exactly like the photos."),
    ("Prajakta Kulkarni", 5, "Loved the craftsmanship. Will order again."),
    ("Snehal Patil", 4, "Great product, packaging could be sturdier."),
    ("Rohit More", 5, "Top quality, highly recommended for gifting."),
    ("Neha Shah", 4, "Very happy with the purchase, arrived on time."),
    ("Arjun Verma", 3, "Good product but slightly smaller than expected."),
]


def make_placeholder_image(text, size=(800, 800), color=(181, 80, 47)):
    """Generate a simple in-memory placeholder image (requires Pillow)."""
    image = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(image)
    draw.text((size[0] // 2, size[1] // 2), text, fill=(255, 255, 255), anchor="mm")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = "Seeds demo categories, products, images, and reviews."

    def handle(self, *args, **options):
        if not PIL_AVAILABLE:
            self.stderr.write(self.style.ERROR(
                "Pillow is not installed. Run: pip install Pillow"
            ))
            return

        self.stdout.write("Seeding categories...")
        categories_by_slug = {}
        for order, cat in enumerate(CATEGORY_DATA):
            category, created = Category.objects.get_or_create(
                slug=cat["slug"],
                defaults={"name": cat["name"], "display_order": order},
            )
            if created or not category.image:
                category.image.save(
                    f"{cat['slug']}.jpg",
                    make_placeholder_image(cat["name"], size=(600, 800), color=cat["color"]),
                    save=True,
                )
            categories_by_slug[cat["slug"]] = category
        self.stdout.write(self.style.SUCCESS(f"  {len(categories_by_slug)} categories ready."))

        self.stdout.write("Seeding products...")
        created_count = 0
        for data in PRODUCT_DATA:
            slug = self._slugify(data["name"])
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": data["name"],
                    "category": categories_by_slug.get(data["category_slug"]),
                    "short_description": f"Handcrafted {data['material'].lower()} by artisans in {data['artisan_state']}.",
                    "description": (
                        f"This {data['name'].lower()} is handcrafted by {data['artisan_name']} "
                        f"in {data['artisan_state']}, using traditional techniques passed down "
                        f"through generations. Made from {data['material'].lower()}, each piece "
                        f"carries small natural variations that make it one of a kind."
                    ),
                    "price": data["price"],
                    "compare_at_price": data.get("compare_at_price"),
                    "stock_quantity": random.randint(5, 40),
                    "is_bestseller": data.get("is_bestseller", False),
                    "is_new_arrival": data.get("is_new_arrival", False),
                    "is_customizable": data.get("is_customizable", False),
                    "artisan_name": data["artisan_name"],
                    "artisan_state": data["artisan_state"],
                    "material": data["material"],
                },
            )

            if created:
                created_count += 1
                product_image = ProductImage(product=product, is_primary=True, display_order=0)
                product_image.image.save(
                    f"{slug}-1.jpg",
                    make_placeholder_image(product.name, color=(200, 150, 62)),
                    save=True,
                )

                # Seed 2-4 reviews per product
                sample_reviews = random.sample(REVIEW_SAMPLES, k=random.randint(2, 4))
                for reviewer_name, rating, comment in sample_reviews:
                    Review.objects.create(
                        product=product,
                        reviewer_name=reviewer_name,
                        rating=rating,
                        comment=comment,
                    )

        self.stdout.write(self.style.SUCCESS(f"  {created_count} new products created."))
        self.stdout.write(self.style.SUCCESS("Demo data ready. Visit /admin/ to view and edit it."))

    @staticmethod
    def _slugify(name):
        return name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace(",", "")
