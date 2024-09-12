# Generated by Django 5.1 on 2024-09-12 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]