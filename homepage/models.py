from django.db import models


class SiteSettings(models.Model):
    """
    Singleton-style model: only one row is meant to ever exist.
    Controls the logo, top offer bar text, and footer contact info
    from the Django admin instead of being hardcoded in templates.
    """
    site_name = models.CharField(max_length=100, default="Tesha Handicrafts")
    logo = models.ImageField(
        upload_to="site/", blank=True, null=True,
        help_text="Shown in the navbar. Recommended: transparent PNG, ~200px tall.",
    )

    topbar_text = models.CharField(
        max_length=200, blank=True,
        default="Free Shipping Above \u20b9999 | Handmade in India",
    )

    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_address = models.CharField(max_length=255, blank=True)

    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    whatsapp_url = models.URLField(blank=True)

    footer_about_text = models.TextField(
        blank=True,
        default="Bringing authentic, handmade Indian craftsmanship to homes everywhere.",
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        # Enforce a single row (pk=1) so there's only ever one settings object.
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HeroSlide(models.Model):
    """A slide in the homepage hero carousel. Admin can add/reorder/hide."""
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="hero/")
    cta_text = models.CharField(max_length=50, default="Shop Now")
    cta_url = models.CharField(max_length=255, default="/products/")
    secondary_cta_text = models.CharField(max_length=50, blank=True)
    secondary_cta_url = models.CharField(max_length=255, blank=True)

    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """
    Customer review shown in the homepage 'Customer Reviews' section.
    Supports either an uploaded video or an external video URL
    (e.g. YouTube/Instagram Reel embed link), plus a photo + quote.
    """
    customer_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="testimonials/photos/", blank=True, null=True)
    quote = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], default=5
    )

    video_file = models.FileField(upload_to="testimonials/videos/", blank=True, null=True)
    video_embed_url = models.URLField(
        blank=True, help_text="Alternative to uploading a file — paste a YouTube/embed URL."
    )

    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.customer_name} ({self.rating}\u2605)"

    @property
    def has_video(self):
        return bool(self.video_file or self.video_embed_url)


from django.db import models
from django.utils.text import slugify


class FestivalBanner(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    image = models.ImageField(upload_to="banners/")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
