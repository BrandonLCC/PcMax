# Generated by Django 4.2.17 on 2024-12-16 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0013_remove_ventas_id_usuario_categorias_imagen_categoria_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventas',
            name='id_usuario',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='store.usuario'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_agregado', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
