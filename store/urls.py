from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CrearOrden

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('carro_compra/', views.carro_compra, name='carro_compra'),
    path('producto/<int:pk>/', views.detalle_productos, name='detalle_producto'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:elemento_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('contacto/', views.contacto_cliente  , name='contacto_cliente'),
    path('guia_y_tutorial/', views.guia_tutorial, name='guia_tutorial'),
    path('carro/modificar/<int:elemento_id>/', views.modificar_cantidad_carrito, name='modificar_cantidad_carrito'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('registro_cliente/', views.registrar_usuario, name='registro_cliente'),
    path('compra_producto/', views.compra_producto, name='compra_producto'),
    path('api/orders', CrearOrden.as_view(), name='crear-orden'),

   ]