from rest_framework import generics, permissions
from .models import ReviewModel
from .serializers import ReviewSerializer
from core.mixins import SwaggerSafeMixin


class SubmitReviewAPIView(generics.CreateAPIView):
    queryset = ReviewModel.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserReviewsListAPIView(SwaggerSafeMixin, generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ReviewModel.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            return qs.filter(user=self.request.user)
        return qs.none()