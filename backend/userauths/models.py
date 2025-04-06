from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(unique=True, max_length=100)
    otp = models.CharField(unique=True, max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Korrektimi i gabimit në metodën save
        email_username, _ = self.email.split("@")
        if not self.full_name:  # Përdor "if not self.full_name" për të kontrolluar nëse është None ose bosh
            self.full_name = email_username
        if not self.username:  # Po ashtu për username
            self.username = email_username
        super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="user_folder", default="default-user.jpg", null=True, blank=True)
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Përdorim full_name nga përdoruesi nëse nuk ka një të dhënë
        return self.full_name if self.full_name else self.user.full_name

    def save(self, *args, **kwargs):
        # Përdorim emailin nga model User
        if not self.full_name:
            self.full_name = self.user.email.split("@")[0]  # Përdor email_username nga email-i
        super(Profile, self).save(*args, **kwargs)


# Krijimi i Profile pas krijimit të një përdoruesi të ri
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Ruajtja e profile pas përditësimit të përdoruesit
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
