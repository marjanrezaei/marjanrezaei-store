from django.urls import path
from . import api_views

app_name = "review_api"

urlpatterns = [
    path("submit/", api_views.SubmitReviewAPIView.as_view(), name="submit-review-api"),
    path("my/", api_views.UserReviewsListAPIView.as_view(), name="user-reviews-api"),
]
