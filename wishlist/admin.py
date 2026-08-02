from django.contrib import admin

from .models import Wishlist, WishlistItem


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0
    readonly_fields = ("product", "added_at")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("session_key", "created_at")
    inlines = [WishlistItemInline]
    readonly_fields = ("session_key", "created_at")
