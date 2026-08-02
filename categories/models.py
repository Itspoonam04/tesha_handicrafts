from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, help_text="Used in the URL, e.g. 'wall-decor'")
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="categories/", blank=True, null=True,
        help_text="Banner image used on the category grid page and category detail header.",
    )
    icon_image = models.ImageField(
        upload_to="categories/icons/", blank=True, null=True,
        help_text="Small square/circular icon used in the homepage 'Shop by Category' row. Falls back to the banner image if left blank.",
    )

    # Supports simple two-level nesting, e.g. "Home Decor" -> "Wall Decor"
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories"
    )

    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers appear first in the navbar and category grid."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("categories:detail", kwargs={"slug": self.slug})
