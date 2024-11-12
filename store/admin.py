from django.contrib import admin
from django.contrib import admin
from .models import Producto, Categorias, Ventas, DetalleVentas

@admin.register(Producto)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 
                    'descripcion_producto',
                    'precio_producto',
                    'cantidad_producto',
                    'creacion_producto', 
                    'imagen_producto',
                    'id_almacen',)
    search_fields = ('nombre_producto', 'descripcion_producto')
    list_filter = ('creacion_producto',)
    

@admin.register(Categorias)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre_categoria',)
    search_fields = ('nombre_categoria',)


admin.site.register(Ventas)
admin.site.register(DetalleVentas)

# opcion de eliminar


