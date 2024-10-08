from django.contrib import admin
from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 
                    'descripcion_producto',
                    'precio_producto',
                    'cantidad_producto',
                    'creacion_producto', 
                    'imagen_producto')
    search_fields = ('nombre_producto', 'descripcion_producto')
    list_filter = ('creacion_producto',)