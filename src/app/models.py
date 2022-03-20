import os
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.db import models
from django_extensions.db.models import TimeStampedModel
from versatileimagefield.fields import VersatileImageField


def path_and_filename(instance, filename):
    upload_to = f'medias/{instance.__class__.__name__.lower()}'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):

    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    avatar = VersatileImageField('user_avatar', null=True, blank=True, upload_to=path_and_filename)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}: {self.full_name}'

    def has_perm(self, perm, obj=None):
        """
        Check if the user has a specific permission
        """
        return True

    def has_module_perms(self, app_label):
        """
        Check if a user has permissions to view the app `app_label`
        """
        return True

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Post(TimeStampedModel):

    topic = models.CharField(max_length=50)
    content = models.TextField()
    owner = models.ForeignKey('User', related_name='posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField('User', related_name='liked_posts', blank=True)

    def __str__(self):
        return f'{self.owner}: {self.topic}'
