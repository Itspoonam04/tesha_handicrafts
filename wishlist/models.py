from django.db import models

from products.models import Product


class Wishlist(models.Model):
    """Session-based wishlist, mirroring the Cart pattern. See cart/models.py."""
    session_key = models.CharField(max_length=40, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist ({self.session_key})"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("wishlist", "product")

    def __str__(self):
        return f"{self.product.name} (wishlisted)"
