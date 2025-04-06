from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(unique=True, max_length=100)
    opt = models.CharField(max_length=100, null=True, blank=True)
    refresh_token = models.CharField(max_length=100, null=True, blank=True)

    # Përdor related_name për të shmangur përplasjet
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_user_groups',  # Emër unik për këtë model
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_user_permissions',  # Emër unik për këtë model
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        email_username, _ = self.email.split("@")
        
        if self.full_name is None:  # Korrigjim për kontrollin e None
            self.full_name = email_username  # Përdor email_username nëse full_name është None

        if not self.username:  # Kontrollo për një username të zbrazët ose None
            self.username = email_username  # Përdor email_username për username nëse është zbrazët
        
        super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.FileField(upload_to="user_folder", default="default-user.jpg")  # Rreshti i komentuari për imazhin
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email  # Shto për të shfaqur email-in e përdoruesit në Profile
