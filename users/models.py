from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

from django.utils import timezone


class User(AbstractUser):
    nationalCode = models.CharField(max_length=70, null=True)
    postalCode = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=11, null=True)
    mobile = models.CharField(max_length=11, null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=1000, null=True)
    refCode = models.CharField(max_length=50, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    updatedAt = models.DateTimeField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.updatedAt = timezone.now()
        super(User, self).save(*args, **kwargs)
