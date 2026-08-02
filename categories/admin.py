from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_active", "display_order")
    list_filter = ("is_active", "parent")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("display_order", "name")
    fields = (
        "name", "slug", "description", "parent", "is_active", "display_order",
        "icon_image", "image",
    )
