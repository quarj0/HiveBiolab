from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("metadata", "created_at")
    list_filter = ("created_at",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "email",
                    "subject",
                    "message",
                    "organization",
                )
            },
        ),
        ("Metadata", {"fields": ("metadata", "created_at")}),
    )
