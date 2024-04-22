from django.db.models import Manager
from django.utils import timezone
from taggit.managers import TaggableManager
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionManager, PermissionsMixin


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_staff=False, is_superuser=False, **kwargs):
        if not email and password and username:
            raise ValueError("Please enter a username , password and a valid email address")
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            is_staff=False,
            is_superuser=False,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **kwargs):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        return user


class CustomUser(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField()
    bio = models.TextField()
    profile_photo = models.ImageField(upload_to='media/')
    date_of_birth = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = 'PB', "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, related_name='post_author', on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    tags = TaggableManager()

    objects = Manager()
    published = PublishManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish']


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, related_name='comment_author', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.body
