from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import uuid

from django.db.models.signals import post_delete
from django.dispatch import receiver


def image_path(_, filename):
    extension = filename.split('.')[-1]
    unique_id = uuid.uuid4().hex
    new_imagename = 'profile/'+unique_id+'.'+extension
    return new_imagename


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have en email address")
        if not username:
            raise ValueError("User must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to=image_path, null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


@receiver(post_delete, sender=User)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)