from django.dispatch import receiver
from ..validators import validate_iranian_phone
from django.db.models.signals import post_save
from django.db import models
from .users import User

class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True, related_name='user_profile')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=11,
        validators=[validate_iranian_phone], 
        unique=True)
    
    image = models.ImageField(upload_to="profile/", default="profile/default.jpg")
    image_url = models.URLField(blank=True, null=True)  # فقط برای لیارا

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_image(self):
        if self.image_url:
            return self.image_url 
        elif self.image:
            return self.image.url 
        else:
            return 'https://marjan.storage.c2.liara.space/default.jpg'

    def get_fullname(self):
        if self.first_name or self.last_name:
            return self.first_name + " " + self.last_name
        return "کاربر جدید"
    

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, pk=instance.pk)