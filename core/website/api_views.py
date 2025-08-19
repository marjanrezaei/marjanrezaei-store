from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import NewsLetterModel, ContactModel
from .serializers import NewsLetterSerializer, ContactSerializer

class NewsletterAPIView(generics.CreateAPIView):
    queryset = NewsLetterModel.objects.all()
    serializer_class = NewsLetterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "ایمیل شما با موفقیت ثبت شد.", "data": serializer.data}, status=status.HTTP_201_CREATED)


class ContactAPIView(generics.CreateAPIView):
    queryset = ContactModel.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()

        # Optional: send email notification
        from django.core.mail import send_mail
        send_mail(
            subject=f"Contact Request from {contact.first_name} {contact.last_name}",
            message=(
                f"Email: {contact.email}\n"
                f"Phone: {contact.phone_number}\n"
                f"Message: {contact.details}"
            ),
            from_email=contact.email,
            recipient_list=["your_email@example.com"],
        )

        return Response({"message": "پیام شما با موفقیت ارسال شد!", "data": serializer.data}, status=status.HTTP_201_CREATED)
