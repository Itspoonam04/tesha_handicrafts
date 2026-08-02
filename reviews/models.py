from django.conf import settings
from django.db import models

from products.models import Product


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Linked once the reviewer is a registered account.",
    )
    reviewer_name = models.CharField(
        max_length=100, help_text="Display name shown with the review (used if no account is linked)."
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)

    is_approved = models.BooleanField(
        default=True, help_text="Uncheck to hide a review from the storefront without deleting it."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.rating}\u2605 by {self.reviewer_name} on {self.product.name}"
