from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

User = get_user_model()
from .tasks import send_reset_email

User = get_user_model()

from .serializers import RegisterSerializer, MyTokenObtainPairSerializer
from .models.users import User


class MyTokenObtainPairAPIView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = authenticate(
                email=request.data['email'], 
                password=request.data['password']
            )
            if user:
                login(request, user)
        return response


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class CheckEmailExistsAPI(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "").strip()
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        exists = User.objects.filter(email__iexact=email).exists()
        return Response({"exists": exists})


class PasswordResetAPI(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "").strip()
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(email__iexact=email).exists():
            return Response({"error": "No account found with this email"}, status=status.HTTP_404_NOT_FOUND)

        # Schedule async email
        send_reset_email.apply_async((email,), eta=now() + timedelta(hours=48))

        return Response({"message": "Password reset link will be sent to your email."}, status=status.HTTP_200_OK)


class PasswordResetConfirmAPI(APIView):
    """
    Handles password reset confirmation via API.
    Expects: uid, token, new_password, confirm_password
    """
    
    def post(self, request, *args, **kwargs):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not uidb64 or not token or not new_password or not confirm_password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)
