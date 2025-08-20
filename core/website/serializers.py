from rest_framework import serializers
from .models import NewsLetterModel, ContactModel


class NewsLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetterModel
        fields = ['id', 'email']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactModel
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'email', 'details', 'created_at']
        read_only_fields = ['created_at']
