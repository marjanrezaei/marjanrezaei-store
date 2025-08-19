# reviews/api_urls.py

from django.urls import path
from . import api_views

urlpatterns = [
    path("reviews/submit/", api_views.SubmitReviewAPIView.as_view(), name="submit-review"),
    path("reviews/my/", api_views.UserReviewsListAPIView.as_view(), name="user-reviews"),
]
