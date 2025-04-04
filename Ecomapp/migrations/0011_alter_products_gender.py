# Generated by Django 5.1.6 on 2025-04-01 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecomapp', '0010_alter_products_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='gender',
            field=models.CharField(blank=True, choices=[('boy', 'Boy'), ('girl', 'Girl'), ('men', 'Men'), ('women', 'Women'), ('unisex', 'Unisex')], max_length=10, null=True),
        ),
    ]
