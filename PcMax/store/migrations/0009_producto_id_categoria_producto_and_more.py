# Generated by Django 4.2.16 on 2024-10-08 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_producto_imagen_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='id_categoria_producto',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen_producto',
            field=models.ImageField(blank=True, null=True, upload_to='producto/'),
        ),
    ]
