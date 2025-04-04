# Generated by Django 5.1.6 on 2025-03-31 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecomapp', '0007_remove_products_colors_remove_products_sizes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='size',
            name='size_type',
            field=models.CharField(choices=[('numeric', 'Numeric'), ('label', 'Label')], default='valid Python.', max_length=50),
            preserve_default=False,
        ),
    ]
