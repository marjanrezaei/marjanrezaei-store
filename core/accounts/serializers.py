from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

from .models.users import User
from .models.profiles import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'type']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'image', 'image_url']
        ref_name = "AccountsProfileSerializer"


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1", "first_name", "last_name", "phone_number"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password1"]:
            raise serializers.ValidationError({"password1": "Passwords do not match."})
        try:
            validate_password(attrs["password"])
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return attrs

    def create(self, validated_data):
        # Remove password1 before creating user
        validated_data.pop("password1")
        password = validated_data.pop("password")

        # Extract profile info
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        phone_number = validated_data.pop("phone_number")

        # Create user
        user = User.objects.create_user(email=validated_data["email"], password=password, is_verified=False)

        # Update related profile
        profile = user.user_profile  # because related_name='user_profile'
        profile.first_name = first_name
        profile.last_name = last_name
        profile.phone_number = phone_number
        profile.save()

        return user

    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'type': self.user.type
        }
        return data
    

class EmptySerializer(serializers.Serializer):
    pass