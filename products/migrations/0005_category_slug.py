# Generated by Django 5.1 on 2024-09-04 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, verbose_name='Slug'),
        ),
    ]
