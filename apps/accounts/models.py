from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    email = models.EmailField(unique=True)


    def __str__(self):
        return self.username



class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )
    bio = models.TextField(
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"
    