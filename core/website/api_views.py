from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.utils.translation import gettext as _

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
        return Response({"message":  _("Your email has been registered successfully."), "data": serializer.data}, status=status.HTTP_201_CREATED)


class ContactAPIView(generics.CreateAPIView):
    queryset = ContactModel.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()

        send_mail(
            subject=_("Contact Request from") + f" {contact.first_name} {contact.last_name}",
            message=_("Email") + f": {contact.email}\n" +
                    _("Phone") + f": {contact.phone_number}\n" +
                    _("Message") + f": {contact.details}",
            from_email=contact.email,
            recipient_list=["rezaei.marjann@gmail.com"],
        )

        return Response({
            "message": _("Your message was sent successfully!"),
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)