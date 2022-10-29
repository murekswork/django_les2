from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class CustomUserManager(BaseUserManager):

    def create_user(self, username, password, email) -> 'User':
        if not username:
            raise ValueError('USER MUST HAVE UNIQUE USERNAME')
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        profile = Profile(user=user)
        profile.save(using=self._db)
        return user

    def create_superuser(self, username, password, email) -> 'User':
        user = self.create_user(username=username, password=password, email=email)
        user.staff = True
        user.admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    image_url = models.URLField(blank=True, max_length=500, default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460__340.png')
    nickname = models.CharField(default='User', max_length=50)
    age = models.IntegerField(default=0)
    about = models.CharField(default='Nothing', max_length=1000)
    balance = models.FloatField(default=0)


class User(AbstractUser):
    objects = CustomUserManager()
    username: str = models.CharField(max_length=50, unique=True)
    is_active: bool = models.BooleanField(default=True)
    staff: bool = models.BooleanField(default=False)
    admin: bool = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD =[]


    def __str__(self):
        return self.username

    def is_admin(self):
        return self.admin

    def is_staff(self):
        return self.staff

    def active(self):
        return self.is_active

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perm(self, perm, app_label):
        return True
# Create your models here.
