from django.db import models
from accounts.validators import validate_iranian_phone

# Create your models here.
class NewsLetterModel(models.Model):
    email = models.EmailField()
    
    def __str__(self):
        return self.email
    
    

class ContactModel(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=11,
        validators=[validate_iranian_phone])
    email = models.EmailField()
    details = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"
