# Generated by Django 4.0.4 on 2022-05-24 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptoshop', '0003_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
