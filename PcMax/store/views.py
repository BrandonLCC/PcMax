from django.shortcuts import render, redirect
from .models import Producto
from django.db import connection
from django.shortcuts import get_object_or_404
from .form import ContactoForm

# Creacion de  las vistas 

def home(request):
    productos = Producto.objects.all()[:4]
    return render(request, 'index.html' ,{'productos': productos})

#Permite mostrar todos los datos usando ORM de forma mas facil: object.all
#Tambien podemos crear views con SQL crudo por ejmplo: select * from

def lista_productos(request):
    categoria = request.GET.get('id_categoria_producto', '')  # Recibe la categoría por GET
    if categoria:
        productos = Producto.objects.filter(id_categoria_producto=categoria)  # Filtra por categoría
    else:
        productos = Producto.objects.all()  # Si no hay categoría, muestra todos los productos
    return render(request, 'lista_productos.html', {'productos': productos})

#Se utilizara una pk para identificar el  id del producto y al seleccionarlo 
##Llevara a la pagina de detalle
def detalle_productos(request, pk):
    productos = get_object_or_404(Producto, pk=pk)
    return render(request,'detalle_producto.html', {'productos': productos})


def contacto_cliente(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactoForm()
    return render(request, 'contacto_cliente.html', {'form': form})

def guia_tutorial(request):
    return render(request, 'guia_tutorial.html')

