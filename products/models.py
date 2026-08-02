from django.db import models
from django.urls import reverse

from categories.models import Category
from django.db import models
from homepage.models import FestivalBanner


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products"
    )

    short_description = models.CharField(
        max_length=255, blank=True, help_text="Shown on product cards / listing pages."
    )
    description = models.TextField(blank=True, help_text="Full description shown on the product detail page.")

    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Optional 'strike-through' original price to show a discount.",
    )

    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide from the storefront without deleting.")
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)

    # Handicraft-specific fields
    artisan_name = models.CharField(max_length=150, blank=True)
    artisan_state = models.CharField(max_length=100, blank=True, help_text="e.g. 'Rajasthan', 'West Bengal'")
    material = models.CharField(max_length=150, blank=True, help_text="e.g. 'Terracotta, Brass'")
    is_customizable = models.BooleanField(default=False)

    festival_collection = models.ForeignKey(
        FestivalBanner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        help_text='Select if this product belongs to a specific festival collection',  # <--- Make sure this comma is here!
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})

    @property
    def is_on_sale(self):
        return self.compare_at_price is not None and self.compare_at_price > self.price

    @property
    def primary_image(self):
        image = self.images.filter(is_primary=True).first()
        return image or self.images.first()

    @property
    def in_stock(self):
        return self.stock_quantity > 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"Image for {self.product.name}"
