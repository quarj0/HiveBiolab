from django.db import models


class TrainingRegistration(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=32, blank=True)
    program = models.CharField(max_length=255)
    current_level = models.CharField(max_length=255, blank=True, null=True)
    experience_summary = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
