from django.db import models
from django.utils.text import slugify
from django.utils import timezone


from userauths.models import User, Profiles
from shortuuid.django_fields import ShortUUIDField

LANGUAGE = (
    ("English", "English"),
    ("German", "German"),
    ("French", "French"),
)

LEVEL = (
    ("Beginner", "Beginner"),
    ("Intermediate", "Intermediate"),
    ("Advanced", "Advanced"),
)

TEACHER_STATUS = (
    ("Draft", "Draft"),
    ("Disabled", "Disabled"),
    ("Published", "Published"),

)

PLATFORM_STATUS = (
    ("Review", "Review"),
    ("Disabled", "Disabled"),
    ("Rejected", "Rejected"),
    ("Draft", "Draft"),
    ("Published", "Published"),

)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="course-file", blank=True, null=True,
                             default="default.jpg")  # Rreshti i komentuari për imazhin
    full_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    aboout = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.full_name

    def students(self):
        return CartOrderItem.objects.filter(Teacher=self)

    def courses(self):
        return Course.objects.filter(teacher=self)

    def reviews(self):
        return Review.objects.filter(teacher=self).count()


class Category(models.Model):
    titla = models.CharField(max_length=100)
    image = models.FileField(upload_to="course-file", blank=True, null=True,
                             default="category.jpg")  # Rreshti i komentuari për imazhin
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Category"
        ordering = ['title']

    def __str__(self):
        return self.title

    def course_count(self):
        return Course.objects.filter(category=self).count()

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Course(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to="course-file", blank=True, null=True)
    image = models.FileField(upload_to="course-file", blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digit=12, decimal_places=2, default=0.00)
    language = models.CharField(choices=LANGUAGE, default="English")
    level = models.CharField(choices=LEVEL, default="Beginner")
    platform_status = models.CharField(
        choices=PLATFORM_STATUS, default="Published")
    teacher_course_status = models.CharField(
        choices=TEACHER_STATUS, default="Published")
    featured = models.BooleanField(default=False)
    course_id = ShortUUIDField(
        unique=True, Length=6, max_Length=20, alphabet="0123456789")
    slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Course"
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)


""" from django.db import models
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
            # Përdor email_username për username nëse është zbrazët
            self.username = email_username

        super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.FileField(upload_to="user_folder", default="default-user.jpg")  # Rreshti i komentuari për imazhin
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    # mundem me lon edhe zbrazet
    about = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    # facebook= models.URLField(null=True, blank=True)  mundem me shtu naj rrjet social

    def __str__(self):
        return self.user.email  # Shto për të shfaqur email-in e përdoruesit në Profile
 """
