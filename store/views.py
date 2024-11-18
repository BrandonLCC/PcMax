from django.contrib import messages

from django.shortcuts import render, redirect
from .models import Producto, Carrito , CarritoProducto as ElementoCarrito
from django.db import connection
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .form import CantidadProductoForm, ContactoForm
from .form import *
from .functions import generateAccessToken, crearOrden
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Creacion de  las vistas 

def home(request):
    productos = Producto.objects.select_related('id_categoria').all()[:4]
    return render(request, 'index.html' ,{'productos': productos})

#Permite mostrar todos los datos usando ORM de forma mas facil: object.all
#Tambien podemos crear views con SQL crudo por ejmplo: select * from

def lista_productos(request):
    categoria = request.GET.get('id_categoria', '')  
    if categoria:
        productos = Producto.objects.filter(id_categoria=categoria).select_related('id_categoria') 
    else:
        productos = Producto.objects.all()  
        
    return render(request, 'lista_productos.html', {'productos': productos})

#Se utilizara una pk para identificar el  id del producto y al seleccionarlo 
##Llevara a la pagina de detalle

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


def detalle_productos(request, pk):
    producto = get_object_or_404(Producto.objects.select_related('id_categoria','id_almacen').all(), pk=pk)  # Obtén el producto por su ID
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

@login_required
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


#agregar modificar cantidad de stock producto



def modificar_cantidad_carrito(request, elemento_id):
    elemento = get_object_or_404(ElementoCarrito, id=elemento_id)
    if request.method == 'POST':
        form = CantidadProductoForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']

            # Verifica que la cantidad solicitada no exceda el stock disponible
            if cantidad > elemento.producto.cantidad_producto:
                messages.error(request, 'La cantidad solicitada excede el stock disponible.')
            else:
                elemento.cantidad = cantidad
                elemento.save()
                messages.success(request, 'Cantidad actualizada correctamente.')
                return redirect('carro_compra')
    else:
        form = CantidadProductoForm(initial={'cantidad': elemento.cantidad})

    # Si el formulario no es válido, redirige a la misma página del carrito
    return redirect('carro_compra')

def inicio_sesion(request):
    form = InicioSesion()
    if request.method == 'POST':
        form = InicioSesion(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre_usuario']
            contraseña = form.cleaned_data['contraseña_usuario']
            user = authenticate(request, username=nombre, password=contraseña)
            if user is not None:
                login(request, user)
                print(f"Usuario {nombre} autenticado correctamente.")

                return redirect('home')
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = InicioSesion()
    return render(request, 'inicio_sesion.html', {'form': form})

def registrar_usuario(request):
    data = {
        'form': RegistroUsuarioForm()
    }

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid(): 
            form.save()  # Guarda usuario 
            messages.success(request, '¡Registro exitoso!')
            return redirect(to='home')
        else:
            form = RegistroUsuarioForm()
  
    return render(request, 'registro_cliente.html', data)


def compra_producto(request):
    print("-----")
    respuesta = generateAccessToken()
    print(respuesta)
    return render(request,'compra_producto.html')

#Parte 1: integracion y conexion con la API paypal
#Parte 2: luego se agregara los datos del carro de compras
#Parte 3: Poder almacenar la compra en la BD
class CrearOrden(APIView):
    def post(self, request):
        orden = crearOrden('carro_productos')
        return Response(orden, status=status.HTTP_200_OK)
    

#views de contacto
def contacto_nuevo(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacto_confirmacion')
    else:
        form = ContactoForm()
    return render(request, 'contacto/contacto_nuevo.html', {'form': form})


@login_required
def contacto_detalle(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    return render(request, 'contacto/contacto_detalle.html', {'contacto': contacto})

@login_required
def contacto_editar(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == "POST":
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('contacto_detalle', pk=contacto.pk)
    else:
        form = ContactoForm(instance=contacto)
    return render(request, 'contacto/contacto_editar.html', {'form': form})

@login_required
def contacto_eliminar(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    contacto.delete()
    return redirect('contacto_lista')

@login_required
def contacto_lista(request):
    contactos = Contacto.objects.all()
    return render(request, 'contacto/contacto_lista.html', {'contactos': contactos})

def contacto_confirmacion(request):
    return render(request, 'contacto/contacto_confirmacion.html')
    

