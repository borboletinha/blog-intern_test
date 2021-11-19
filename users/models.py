from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not first_name:
            raise ValueError('Please enter your first name')
        if not last_name:
            raise ValueError('Please enter your last name')
        if not username:
            raise ValueError('Please enter your username')
        if not email:
            raise ValueError('Please enter your email')
        user = self.model(first_name=first_name, last_name=last_name,
                          username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(first_name=first_name, last_name=last_name,
                                username=username, email=self.normalize_email(email), password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(db_index=True, max_length=255, verbose_name='first name')
    last_name = models.CharField(db_index=True, max_length=255, verbose_name='last name')
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')
    last_login = models.DateTimeField(auto_now=True, verbose_name='last login')
    is_active = models.BooleanField(default=True, verbose_name='active')
    is_superuser = models.BooleanField(default=False, verbose_name='superuser')
    is_staff = models.BooleanField(default=False, verbose_name='staff')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = UserManager()

    def __str__(self):
        return self.username + '|' + self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, package_name):
        return True
