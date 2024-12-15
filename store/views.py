from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Producto, Carrito , CarritoProducto as ElementoCarrito
from .models import Categorias
from django.db import connection
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .form import CantidadProductoForm, ContactoForm
from .form import *
from .functions import generateAccessToken, crearOrden
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .functions import * 
from .models import Ventas
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import DetalleVentas
# Creacion de  las vistas 

def home(request):
    productos = Producto.objects.select_related('id_categoria').all()[:4]
    
    user = request.user

    if user.is_active:
        estado = 'Seccion abierta'
    else:
        estado = 'false'

    return render(request, 'index.html' ,{'productos': productos,'estado':estado})

#Permite mostrar todos los datos usando ORM de forma mas facil: object.all
#Tambien podemos crear views con SQL crudo por ejmplo: select * from

def lista_productos(request):
    categoria = request.GET.get('id_categoria', '')  
    if categoria:
        categoria = get_object_or_404(Categorias, id_categoria=categoria)
        productos = Producto.objects.filter(id_categoria=categoria).select_related('id_categoria') 
    else:
        categoria = None
        productos = Producto.objects.all()  
        
    return render(request, 'lista_productos.html', {'productos': productos, 'categoria':categoria})

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

            if cantidad > productos.cantidad_producto:  
                form.add_error('cantidad', 'La cantidad solicitada excede el stock disponible.')
            else:
                elemento, creado = ElementoCarrito.objects.get_or_create(carrito=carrito, producto=productos)

                if not creado:
                    elemento.cantidad += cantidad
                else:
                    elemento.cantidad = cantidad

                elemento.save()

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

    descuento_aplicado = 0
    total_carrito_con_descuento = total_carrito

    if request.method == 'POST':
        codigo_descuento = request.POST.get('codigo_descuento', '').strip()
        if codigo_descuento == 'DESCUENTO10':  
            descuento_aplicado = 10  
            total_carrito_con_descuento = total_carrito - (total_carrito * descuento_aplicado / 100)
        elif codigo_descuento == 'DESCUENTO20':
            descuento_aplicado = 20  
            total_carrito_con_descuento = total_carrito - (total_carrito * descuento_aplicado / 100)

    request.session['descuento_aplicado'] = descuento_aplicado
    request.session['total_carrito_con_descuento'] = total_carrito_con_descuento

    return render(request, 'carro_compra.html', {
        'elementos': elementos,
        'total_carrito': total_carrito,
        'total_carrito_con_descuento': total_carrito_con_descuento,
        'descuento_aplicado': descuento_aplicado
    })

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

            if cantidad > elemento.producto.cantidad_producto:
                messages.error(request, 'La cantidad solicitada excede el stock disponible.')
            else:
                elemento.cantidad = cantidad
                elemento.save()
                messages.success(request, 'Cantidad actualizada correctamente.')
                return redirect('carro_compra')
    else:
        form = CantidadProductoForm(initial={'cantidad': elemento.cantidad})

    return redirect('carro_compra')

def guardar_favorito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    favorito, created = Favorito.objects.get_or_create(usuario=request.user, producto=producto)
    if not created:
        favorito.delete()
        mensaje = "El producto ha sido eliminado de favoritos."
    else:
        mensaje = "El producto ha sido agregado a favoritos."
    return redirect('lista_productos')

class Meta:
    unique_together = ('usuario', 'producto')  

#----------- Compra producto ---------------------#
#Parte 1: integracion y conexion con la API paypal
#Parte 2: luego se agregara los datos del carro de compras
#Parte 3: Poder almacenar la compra en la BD

@login_required
def compra_producto(request):
    #  el carrito del usuario
    carrito = get_object_or_404(Carrito, usuario=request.user)
    
    #  los elementos del carrito
    elementos = ElementoCarrito.objects.filter(carrito=carrito)
    
    descuento_aplicado = request.session.get('descuento_aplicado', 0)
    total_carrito_con_descuento = request.session.get('total_carrito_con_descuento', 0)

    # el total a USD 
    global valorFinalCarro
    valorFinalCarro = round(total_carrito_con_descuento / 940, 2)  

    return render(request, 'compra_producto.html', {
        'valorFinalCarro': valorFinalCarro, 
        'elementos': elementos,  
        'total_carrito': total_carrito_con_descuento,  
        'descuento_aplicado': descuento_aplicado  
    })



class CrearOrden(APIView):
    def post(self, request):
        orden = crearOrden(valorFinalCarro) 
        guardar_venta(valorFinalCarro,request)
        detalle_ventas(request)
        return Response(orden, status=status.HTTP_200_OK)

def crearOrden(valorFinalCarro):
    try:
        access_token = generateAccessToken()
        url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": str(valorFinalCarro)
                    }
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()    

    except Exception as error:
        print("Error:", error)
        return None

def guardar_venta(total_venta, request):

    try:
        if not total_venta:
            raise ValueError("total_venta es obligatorio.")
        
        usuario = Usuario.objects.get(gmail_usuario=request.user.email)  
        
        venta = Ventas.objects.create(
            total_venta=total_venta,
            id_usuario_id=usuario.id  
        )
        print("Venta creada:", venta)
        return venta
    



    except ValueError as ve:
        print(f"ValorError: {ve}")
        return None
    except Exception as e:
        print(f"Error al guardar la venta: {e}")
        return None

def detalle_ventas(request):
    try:
        carrito = get_object_or_404(Carrito, usuario=request.user)
        elementos = ElementoCarrito.objects.filter(carrito=carrito)

        if not elementos.exists():
            raise ValueError("El carrito está vacío.")

        usuario = Usuario.objects.get(gmail_usuario=request.user.email)  

        venta = Ventas.objects.filter(id_usuario=usuario).order_by('-id_venta').first()

        if not venta:
            raise ValueError("No se encontró ninguna venta asociada al usuario.")

        with transaction.atomic():
            detalles_venta = []

            for elemento in elementos:

                producto = elemento.producto
                cantidad = elemento.cantidad
                precio = producto.precio_producto  
                subtotal = cantidad * precio  

                detalle = DetalleVentas.objects.create(
                    id_producto=producto,
                    id_venta=venta, 
                    cantidad_producto=cantidad,
                    precio_producto=precio,
                    subtotal=subtotal
                )
                detalles_venta.append(detalle)

            elementos.delete()  
            
        return {
            "venta_id": venta.id,
            "detalles": detalles_venta,
        }

    except ValueError as ve:
        print(f"Error: {ve}")
        return None
    except Exception as e:
        print(f"Error al crear detalles de venta: {e}")
        return None
    
class historialCompras(APIView):
    def get(self, request):
        try:
            # Obtener el usuario autenticado
            usuario = get_object_or_404(Usuario, gmail_usuario=request.user.email)

            # Obtener las ventas del usuario
            ventas = Ventas.objects.filter(id_usuario=usuario)

            productos_comprados = []

            # Iterar sobre cada venta para obtener los detalles
            for venta in ventas:
                detalles_venta = DetalleVentas.objects.filter(id_venta=venta)

                for detalle in detalles_venta:
                    producto = detalle.id_producto  # Obtenemos el objeto Producto completo
                    productos_comprados.append({
                        'venta_id': venta.id_venta,
                        'producto_nombre': producto.nombre_producto,
                        'cantidad': detalle.cantidad_producto,
                        'precio': detalle.precio_producto,
                        'subtotal': detalle.subtotal,
                    })

            return render(request, 'historial.html', {'productos_comprados': productos_comprados})


        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


def registrar_usuario(request):
   
    if request.method == 'POST':
            form = RegistroUsuarioForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password2 = form.cleaned_data['password2']
                form.save()  # Guarda usuario 
                usuario = Usuario.objects.create(
                    nombre_usuario = username,
                    gmail_usuario = email,
                    contraseña_usuario = password2,

                )
                messages.success(request, f"El usuario:{username} ha sido creado")
                return redirect('home')
    else:
        form = RegistroUsuarioForm()

    context = { 'form' : form }
    return render(request, 'registro_cliente.html',context )


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
    

