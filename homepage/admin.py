from django.contrib import admin

from .models import FestivalBanner, HeroSlide, SiteSettings, Testimonial


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Branding", {"fields": ("site_name", "logo", "topbar_text")}),
        ("Contact Info", {"fields": ("contact_phone", "contact_email", "contact_address")}),
        ("Social Links", {"fields": ("instagram_url", "facebook_url", "whatsapp_url")}),
        ("Footer", {"fields": ("footer_about_text",)}),
    )

    def has_add_permission(self, request):
        # Prevent creating a second row — this model is a singleton.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "display_order")
    list_editable = ("is_active", "display_order")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "rating", "has_video", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
    list_filter = ("is_active", "rating")


@admin.register(FestivalBanner)
class FestivalBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
