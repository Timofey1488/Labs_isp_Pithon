# Generated by Django 4.0.4 on 2022-05-19 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptoshop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
    ]
