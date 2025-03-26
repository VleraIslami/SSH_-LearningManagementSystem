from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(unique=True, max_length=100)
    opt = models.CharField(max_length=100, null=True, blank=True)
    refresh_token = models.CharField(max_length=100, null=True, blank=True)


USERNAME_FIELD = 'email'
REQURIED_FIELDS = ['username']


def __str__(self):
    return self.email


def save(self, *args, **kwargs):
    email_username, full_name = self.email.split("@")
    if self.full_name == self.full_name == None:
        self.full_name == email_username

    if self.username == "" or self.username == None:
        self.username = email_username
    super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # nuk eshte komplet rreshti per image
    # image=models.FileField(upload_to="user_folder", default="default-user.jpg",)
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    # vazhdon ende class Profile
