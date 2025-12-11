from django.contrib import admin
from django.urls import path

from contact.views import submit_message
from newsletter.views import subscribe
from training.views import register_participant

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/newsletter/subscribe/', subscribe, name='newsletter_subscribe'),
    path('api/contact/', submit_message, name='contact_submit'),
    path('api/training/register/', register_participant, name='training_register'),
]
