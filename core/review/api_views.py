from rest_framework import generics, permissions
from .models import ReviewModel
from .serializers import ReviewSerializer


class SubmitReviewAPIView(generics.CreateAPIView):
    queryset = ReviewModel.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserReviewsListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ReviewModel.objects.filter(user=self.request.user)
