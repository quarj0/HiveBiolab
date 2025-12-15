from django.contrib import admin

from .models import TrainingRegistration


@admin.register(TrainingRegistration)
class TrainingRegistrationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "program", "created_at")
    search_fields = ("full_name", "email", "program", "experience_summary", "goals")
    readonly_fields = ("metadata", "created_at")
    list_filter = ("program", "created_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "full_name",
                    "email",
                    "phone",
                    "program",
                    "current_level",
                    "experience_summary",
                    "goals",
                    "message",
                )
            },
        ),
        ("Metadata", {"fields": ("metadata", "created_at")}),
    )
