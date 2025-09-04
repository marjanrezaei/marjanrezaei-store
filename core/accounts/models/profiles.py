from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from ..validators import validate_iranian_phone
from .users import User
from core.utils.liara_upload import delete_from_liara, upload_to_liara


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="user_profile"
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=11, validators=[validate_iranian_phone], unique=True, blank=True, null=True
    )

    image = models.ImageField(upload_to="profile/", default="profile/default.jpg")
    image_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Override save to handle Liara upload and replace old image if updated.
        """
        if self.image:
            # if updating an existing profile, delete old image first
            if self.pk:
                old = Profile.objects.filter(pk=self.pk).first()
                if old and old.image_url and old.image != self.image:
                    key = "/".join(old.image_url.split("/")[-2:])
                    delete_from_liara(key)

            # upload new image
            filename = f"{self.user.id}_profile.jpg"
            url = upload_to_liara(self.image, filename, folder="profile")
            if url:
                self.image_url = url
                self.image = None  # clear local file storage

        super().save(*args, **kwargs)

    def get_image(self):
        if self.image_url:
            return self.image_url
        elif self.image:
            return self.image.url
        return "https://marjan.storage.c2.liara.space/default.jpg"

    def get_fullname(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        return "کاربر جدید"

    def delete_image(self):
        if self.image_url:
            key = "/".join(self.image_url.split("/")[-2:])
            delete_from_liara(key)
            self.image_url = None
        if self.image:
            self.image.delete(save=False)
            self.image = None
        self.save()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_delete, sender=Profile)
def delete_profile_images(sender, instance, **kwargs):
    instance.delete_image()
