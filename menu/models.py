from django.db import models


class Menu(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=256)
    ingredients = models.TextField()
    description = models.TextField()
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    isCold = models.BooleanField(null=True, blank=True)
    isHot = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'{self.category} {self.name}'