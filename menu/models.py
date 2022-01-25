from django.db import models


class Category(models.Model):
    CHOICES = [
        (1, 'پیش غذا'),
        (2, 'چای و قهوه'),
        (3, 'دسرها'),
        (4, 'غذاهای اصلی'),
        (5, 'نوشیدنی های سرد'),
    ]
    name = models.IntegerField(choices=CHOICES)

    class Meta:
        ordering = ('name',)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.get_name_display()


class Type(models.Model):
    CHOICES = (
        (1, 'ماکتیل ها'),
        (2, 'نوشیدنی های سالم'),
        (3, 'شیک ها'),
        (4, 'غذاهای اصلی'),
        (5, 'پیشنهاد باریستا'),
        (6, 'دمنوش های الهام بخش'),
        (7, 'دسرها'),
        (8, 'وافل/کرپ'),
        (9, 'پیتزا و پاستا'),
        (10, 'ساندویج و برگر'),
        (11, 'استیک'),
        (12, 'غذای ایرانی'),
        (13, 'صبحانه'),
        (14, 'سالاد'),
        (15, 'سوپ'),
    )
    name = models.IntegerField(choices=CHOICES)

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
