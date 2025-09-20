from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from ..validators import validate_iranian_phone
from .users import User
from core.utils.liara_upload import delete_from_liara, upload_to_liara
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="user_profile"
    )
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(
        max_length=11,
        validators=[validate_iranian_phone],
        unique=True,
        blank=True,
        null=True
    )

    image = models.ImageField(upload_to="profile/", default="profile/default.jpg", blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Override save to handle Liara upload if in production,
        otherwise keep local image.
        """
        super().save(*args, **kwargs)

        if self.image:
            if settings.LIARA_UPLOAD_ENABLED:
                if self.pk:
                    old = Profile.objects.filter(pk=self.pk).first()
                    if old and old.image_url and old.image != self.image:
                        key = "/".join(old.image_url.split("/")[-2:])
                        delete_from_liara(key)

                filename = f"{self.user.id}_profile.jpg"
                url = upload_to_liara(self.image, filename, folder="profile")
                if url:
                    self.image_url = url
                    super().save(update_fields=["image_url"])
            else:
                if not self.image_url:
                    self.image_url = self.image.url
                    super().save(update_fields=["image_url"])

    def get_image(self):
        if self.image_url:
            return self.image_url
        elif self.image:
            return self.image.url
        return "/media/profile/default.jpg"

    def get_fullname(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        return "New User"

    def delete_image(self):
        if settings.LIARA_UPLOAD_ENABLED:
            if self.image_url:
                key = "/".join(self.image_url.split("/")[-2:])
                delete_from_liara(key)
                self.image_url = None
        else:
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
