from django.urls import path
from .api_views import NewsletterAPIView, ContactAPIView

app_name = "website_api"

urlpatterns = [
    path("newsletter/", NewsletterAPIView.as_view(), name="newsletter_api"),
    path("contact/", ContactAPIView.as_view(), name="contact_api"),
]
