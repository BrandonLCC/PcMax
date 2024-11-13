from django.db import models
from django.contrib.auth.models import User

class Regiones(models.Model):
    id_region = models.IntegerField(primary_key=True)
    nombre_region = models.CharField(max_length=20)

class Comunas(models.Model):
    id_comuna = models.IntegerField(primary_key=True)
    nombre_comuna = models.CharField(max_length=20)
    id_region = models.OneToOneField(Regiones, on_delete = models.CASCADE)
    
class Almacenes(models.Model):
    id_almacen = models.IntegerField(primary_key=True) # Agregar primary_key=True si es el identificador principal    nombre_almacen = models.CharField(max_length=50)
    nombre_almacen = models.CharField(max_length=50)
    direccion_almacen = models.TextField(max_length=100)
    id_comuna = models.ForeignKey(Comunas, on_delete = models.CASCADE) #models.CharField(max_length=2)
    
    def __str__(self): 
        return self.nombre_almacen
    
    
class Categorias(models.Model):
    id_categoria = models.IntegerField(primary_key=True) 
    nombre_categoria = models.CharField(max_length = 50)
    def __str__(self):
        return self.nombre_categoria    

class Producto(models.Model):
    nombre_producto = models.CharField(max_length = 50)
    descripcion_producto = models.TextField()
    precio_producto = models.IntegerField()
    cantidad_producto = models.IntegerField(default=0)  
    creacion_producto = models.DateTimeField(auto_now_add=True)
    imagen_producto = models.ImageField(upload_to='producto/', null=True, blank=True)
    id_categoria = models.ForeignKey(Categorias,on_delete=models.CASCADE, default=0)#Sin categoria
    id_almacen = models.ForeignKey(Almacenes, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nombre_producto    



class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=100)
    gmail_usuario = models.EmailField(max_length=50, )
    #Encriptar la contraseña    
    contraseña_usuario = models.CharField(max_length=500)
    #id_comuna = models.OneToOneField(Comunas, on_delete=models.CASCADE)
     
    def __str__(self): 
        return self.nombre_usuario

class Ventas(models.Model):
    id_venta = models.IntegerField(primary_key = True)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total_venta = models.IntegerField
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class DetalleVentas(models.Model):
    id_detalle_venta = models.IntegerField(primary_key = True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    cantidad_producto = models.IntegerField()  
    precio_producto = models.IntegerField()  
    subtotal = models.IntegerField()  

#hisotrial de productos que el usuario ha visto

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    mensaje_cifrado = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.nombre

#Modelos del carro de compras
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
    
class ElementoCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)



