from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True, 
                                    error_messages={'unique': "Email already used"})
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    is_manager= models.BooleanField('Is manager', default=False)
    is_customer = models.BooleanField('Is customer', default=False)
    is_provider = models.BooleanField('Is provider', default=False)
    is_saparepart = models.BooleanField('Is saparepart', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    class Meta:
        db_table = 'user_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ["-id"]

    def __str__(self):
        return self.email
    


class OTP(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    created_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_otp'
        verbose_name = 'otp'
        verbose_name_plural = 'otps'
        ordering = ["-id"]

    def __str__(self):

        return f'{self.user.email}--{self.otp}'