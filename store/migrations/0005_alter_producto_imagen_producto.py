# Generated by Django 4.2.16 on 2024-10-08 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_producto_imagen_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen_producto',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
    ]