# Generated by Django 4.0.1 on 2022-01-17 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=256)),
                ('ingredients', models.TextField()),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('isCold', models.BooleanField(blank=True, null=True)),
                ('isHot', models.BooleanField(blank=True, null=True)),
            ],
        ),
    ]
