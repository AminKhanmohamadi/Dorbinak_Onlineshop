# Generated by Django 5.1 on 2024-09-04 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='offer',
            field=models.CharField(blank=True, choices=[('0', '0 %'), ('5', '5 %'), ('10', '10 %'), ('20', '20 %'), ('30', '30 %'), ('40', '40 %'), ('50', '50 %')], max_length=100, null=True, verbose_name='Offer'),
        ),
    ]