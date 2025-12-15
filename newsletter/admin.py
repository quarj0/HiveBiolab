from django.contrib import admin

from .models import NewsletterSubscriber


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "source", "created_at")
    search_fields = ("email", "name", "source")
    readonly_fields = ("metadata", "created_at")
    list_filter = ("created_at",)
    fieldsets = (
        (None, {"fields": ("email", "name", "source")}),
        ("Metadata", {"fields": ("metadata", "created_at")}),
    )
