from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
import traceback
import jwt
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.urls import reverse
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import RegisterSerializer, MyTokenObtainPairSerializer
from .models.users import User

User = get_user_model()


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
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            user_obj = get_object_or_404(User, email=email)
            token = self.get_time_limited_token_for_user(user_obj)

            # Determine frontend URL dynamically
            if settings.DEBUG:
                frontend_url = "http://127.0.0.1:8000"
            else:
                frontend_url = "https://marjanrezaei-store.onrender.com"

            # Generate activation path and full link
            activation_path = reverse("accounts_api:activation", kwargs={"token": token})
            activation_link = f"{frontend_url}{activation_path}"

            # Render email template
            message = render_to_string("email/activation_email.tpl", {"activation_link": activation_link})

            # Send email
            try:
                email_message = EmailMessage(
                    subject="Activate your account",
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )
                email_message.content_subtype = "html"
                email_message.send()
                print(f"[SUCCESS] Email sent to {email}")
            except Exception as e:
                print(f"[ERROR] Failed to send email: {e}")
                traceback.print_exc()

            # Print link for direct browser testing
            print(f"Activation link for testing: {activation_link}")

            return Response(
                {"email": email, "activation_link": activation_link},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_time_limited_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
   

class ActivationApiView(generics.GenericAPIView):
    """
    Activate a user via token in the URL
    """
    permission_classes = [AllowAny]

    def get(self, request, token, *args, **kwargs):
        try:
            untoken = UntypedToken(token)
            user_id = untoken.payload.get("user_id")
            user_obj = User.objects.get(id=user_id)
            if user_obj.is_verified:
                return Response({"detail": "Account already activated"}, status=status.HTTP_400_BAD_REQUEST)
            user_obj.is_verified = True
            user_obj.save()
            return Response({"detail": "Account activated successfully"}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPI(APIView):
    """
    Initiates password reset via JWT email.
    Expects JSON: { "email": "user@example.com" }
    """
    permission_classes = []  # Allow any

    def post(self, request):
        email = request.data.get("email", "").strip()
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({"error": "No account found with this email."}, status=status.HTTP_404_NOT_FOUND)

        # Generate JWT token with user ID
        token = str(AccessToken.for_user(user))

        # Build reset URL
        path = reverse('accounts_api:password-reset-confirm-api')  # you can create a single endpoint for JWT
        domain = settings.FRONTEND_URL.rstrip('/')
        reset_link = f"{domain}{path}?token={token}"

        # Render email
        message = render_to_string("accounts/password_reset_email.html", {
            "user": user,
            "reset_link": reset_link,
        })

        email_message = EmailMessage(
            subject="Password Reset Request",
            body=message,
            to=[email],
            from_email=settings.DEFAULT_FROM_EMAIL,
        )
        email_message.content_subtype = "html"
        email_message.send()

        return Response({"message": "A password reset link has been sent to your email."}, status=status.HTTP_200_OK)


class PasswordResetConfirmJWTAPI(APIView):
    """
    دریافت JWT از query params و تغییر پسورد کاربر.
    """
    permission_classes = []  
    def post(self, request):
        token = request.query_params.get("token")  
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not token or not new_password or not confirm_password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        if payload.get("type") != "password_reset":
            return Response({"error": "Invalid token type"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=payload.get("user_id"))
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)

