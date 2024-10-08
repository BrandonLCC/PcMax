from django.db import models

#En esta pagina se creara el modelo del proyecto 

#Modelo 1: producto
class Producto(models.Model):
    nombre_producto = models.CharField(max_length = 50)
    descripcion_producto = models.TextField()
    precio_producto = models.DecimalField(max_digits = 8, decimal_places = 2)
    cantidad_producto = models.IntegerField(default=0)  # Proporcionar un valor por defecto
    creacion_producto = models.DateTimeField(auto_now_add=True)
    #Definir la carpeta de productos
    imagen_producto = models.ImageField(upload_to='producto/', null=True, blank=True)
    id_categoria_producto = models.IntegerField() 
    
def __str__(self):
    return self.nombre_producto  
