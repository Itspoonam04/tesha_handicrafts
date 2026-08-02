from django.contrib import admin

from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "alt_text", "is_primary", "display_order")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name", "category", "price", "compare_at_price",
        "stock_quantity", "is_active", "is_bestseller", "is_new_arrival",
    )
    list_filter = ("category", "is_active", "is_bestseller", "is_new_arrival", "is_customizable")
    search_fields = ("name", "artisan_name", "material")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "slug", "category", "short_description", "description")
        }),
        ("Pricing & Stock", {
            "fields": ("price", "compare_at_price", "stock_quantity")
        }),
        ("Visibility", {
            "fields": ("is_active", "is_bestseller", "is_new_arrival")
        }),
        ("Handicraft Details", {
            "fields": ("artisan_name", "artisan_state", "material", "is_customizable")
        }),
    )
