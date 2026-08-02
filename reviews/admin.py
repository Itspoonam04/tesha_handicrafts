from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "reviewer_name", "rating", "is_approved", "created_at")
    list_filter = ("is_approved", "rating")
    search_fields = ("reviewer_name", "product__name", "comment")
    list_editable = ("is_approved",)
