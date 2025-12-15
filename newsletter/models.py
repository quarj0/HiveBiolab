from django.db import models


class NewsletterSubscriber(models.Model):
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
