from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, username, phone, password=None):
        if not email:
            raise ValueError('User Must Have A Email Address')

        if not phone:
            raise ValueError('User Must Have A Phone Number')

        if not username:
            raise ValueError('User Must Have A Username')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, phone, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False, null=True)
    is_forget = models.BooleanField(default=False, null=True)
    is_customer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    token = models.CharField(max_length=150, null=True)
    obj = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'phone']