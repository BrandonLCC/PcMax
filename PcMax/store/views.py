from django.shortcuts import render
from .models import Producto
from django.db import connection
from django.shortcuts import get_object_or_404

# Creacion de  las vistas 

def home(request):
    return render(request, 'index.html')

#Permite mostrar todos los datos usando ORM de forma mas facil: object.all
#Tambien podemos crear views con SQL crudo por ejmplo: select * from

def lista_productos(request):
    #Verificar si esta esto bien definido por product o producto
    productos = Producto.objects.all()
    return render (request, 'lista_productos.html', {'productos': productos})

#Se utilizara una pk para identificar el id del producto y al seleccionarlo 
##Llevara a la pagina de detalle
def detalle_productos(request, pk):
    productos = get_object_or_404(Producto, pk=pk)
    return render(request,'detalle_producto.html', {'productos': productos})