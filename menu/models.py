from django.db import models


class Category(models.Model):
    CHOICES = [
        ('Appetizer', 'پیش غذا'),
        ('Tea and coffee', 'چای و قهوه'),
        ('Deserts', 'دسرها'),
        ('Main Food', 'غذاهای اصلی'),
        ('Cold Drinks', 'نوشیدنی های سرد'),
    ]
    name = models.CharField(max_length=100, choices=CHOICES)

    class Meta:
        ordering = ('name',)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Type(models.Model):
    CHOICES = [
        ('Appetizer', 'پیش غذا'),
        ('Tea and coffee', 'چای و قهوه'),
        ('Deserts', 'دسرها'),
        ('Main Food', 'غذاهای اصلی'),

    ]
    name = models.CharField(max_length=100, choices=CHOICES)

    class Meta:
        ordering = ('name',)
        verbose_name = "type"
        verbose_name_plural = "types"

    def __str__(self):
        return self.name


class Menu(models.Model):
    category = models.ForeignKey(Category, related_name="menu", on_delete=models.CASCADE)
    type = models.ForeignKey(Type, related_name='menu', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=256)
    photo = models.ImageField(upload_to='menu/images/')
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()

    class Meta:
        ordering = ('category',)

    def __str__(self):
        return f'{self.category} {self.name}'
