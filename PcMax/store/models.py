from django.db import models
from django.contrib.auth.models import User

#En esta pagina se creara el modelo del proyecto 
 
#Modelo 1: producto
class Producto(models.Model):
    nombre_producto = models.CharField(max_length = 50)
    descripcion_producto = models.TextField()
    precio_producto = models.IntegerField()
    cantidad_producto = models.IntegerField(default=0)  # Proporcionar un valor por defecto
    creacion_producto = models.DateTimeField(auto_now_add=True)
    #Definir la carpeta de productos
    imagen_producto = models.ImageField(upload_to='producto/', null=True, blank=True)
    id_categoria_producto = models.IntegerField() 


    def __str__(self):
        return self.nombre_producto
    
#categoria producto
class CategoriaProducto(models.Model):
    nombre_categoria = models.CharField(max_length = 50)
    def __str__(self):
        return self.nombre_categoria

# Modelo 2: Carrito
class Carrito(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # Permitir nulos
    productos = models.ManyToManyField(Producto, through='CarritoProducto')

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


 
class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.cantidad} unidades"

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    mensaje_cifrado = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True) 

def __str__(self):
    return self.nombre_producto  


class ElementoCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)