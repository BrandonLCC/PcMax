from django.shortcuts import render, redirect
from .models import Producto, Carrito , CarritoProducto as ElementoCarrito
from django.db import connection
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .form import CantidadProductoForm, ContactoForm

# Creacion de  las vistas 

def home(request):
    productos = Producto.objects.all()[:4]
    return render(request, 'index.html' ,{'productos': productos})

#Permite mostrar todos los datos usando ORM de forma mas facil: object.all
#Tambien podemos crear views con SQL crudo por ejmplo: select * from

def lista_productos(request):
    categoria = request.GET.get('id_categoria_producto', '')  
    if categoria:
        productos = Producto.objects.filter(id_categoria_producto=categoria) 
    else:
        productos = Producto.objects.all()  
        
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



def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})

def detalle_productos(request, pk):
    producto = get_object_or_404(Producto, pk=pk)  # Obtén el producto por su ID
    return render(request, 'detalle_producto.html', {'producto': producto})

def carro_compra(request):
    return render(request, 'carro_compra.html')


def agregar_al_carrito(request, producto_id):
    productos = get_object_or_404(Producto, id=producto_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = CantidadProductoForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']

            # Verifica que la cantidad solicitada no exceda el stock disponible
            if cantidad > productos.cantidad_producto:  # Asegúrate de que sea 'cantidad_producto'
                form.add_error('cantidad', 'La cantidad solicitada excede el stock disponible.')
            else:
                # Crea o actualiza el elemento en el carrito
                elemento, creado = ElementoCarrito.objects.get_or_create(carrito=carrito, producto=productos)

                # Actualiza la cantidad en el carrito
                if not creado:
                    elemento.cantidad += cantidad
                else:
                    elemento.cantidad = cantidad

                # Guarda el elemento del carrito
                elemento.save()

                # Actualiza el stock del producto
                productos.cantidad_producto -= cantidad
                productos.save()

                return redirect('carro_compra')
    else:
        form = CantidadProductoForm()

    return render(request, 'detalle_producto.html', {'producto': productos, 'form': form})

login_required
def carro_compra(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    elementos = ElementoCarrito.objects.filter(carrito=carrito)
    
    total_carrito = 0
    for elemento in elementos:
        elemento.total = elemento.producto.precio_producto * elemento.cantidad
        total_carrito += elemento.total
    
    return render(request, 'carro_compra.html', {'elementos': elementos, 'total_carrito': total_carrito})

def eliminar_del_carrito(request, elemento_id):
    elemento = get_object_or_404(ElementoCarrito, id=elemento_id)
    elemento.delete()
    return redirect('carro_compra')
