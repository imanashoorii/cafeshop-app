from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

from django.utils import timezone


class User(AbstractUser):
    nationalCode = models.CharField(max_length=70, null=True)
    postalCode = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=11)
    mobile = models.CharField(max_length=11)
    email = models.CharField(max_length=256)
    address = models.CharField(max_length=1000, null=True)
    refCode = models.CharField(max_length=50, null=True, unique=True)
    last_login = models.DateTimeField(blank=True, null=True)
    updatedAt = models.DateTimeField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.updatedAt = timezone.now()
        super(User, self).save(*args, **kwargs)


class OTP(models.Model):
    phone = models.CharField(max_length=11, unique=True)
    otp = models.CharField(max_length=6)
    count = models.PositiveSmallIntegerField(default=0)
    verify = models.BooleanField(default=False)

    def __str__(self):
        return self.phone
