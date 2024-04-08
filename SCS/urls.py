"""
URL configuration for SCS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from controlStock import views
from controlStock.views import import_from_excel
from controlStock.views import aumentar_precio, listar_productos, ver_historial_producto, listar_productos_seleccionados, quitar_producto_seleccionado, limpiar_productos_seleccionados, ajustar_precio_seleccionados


"""
from django.urls import include, path
from scd import views
from django.contrib.auth.views import PasswordResetConfirmView
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    # PRODUCTO
    path('producto/', views.producto, name='producto'),
    path('registrar/producto/', views.registrarProducto, name='registrarProducto'),
    path('eliminar/producto/<id_pd>', views.eliminarProducto, name='eliminarProducto'),
    path('edicion/producto/<id_pd>', views.edicionProducto, name='edicionProducto'),
    path('editar/producto/', views.editarProducto, name='editarProducto'),
    path('import/', import_from_excel, name='import_from_excel'),
  
    path('borrar_todos_productos/', views.borrarTodosProductos, name='borrar_todos_productos'),
    path('aumentar_precio/<int:id_pd>/', aumentar_precio, name='aumentar_precio'), 
    path('listar_productos/', listar_productos, name='listar_productos'),
    path('ver_historial/<int:id_pd>/', ver_historial_producto, name='ver_historial_producto'),
    path('exportar-productos/', views.exportar_productos, name='exportar_productos'),
    path('listar_productos_seleccionados/', listar_productos_seleccionados, name='listar_productos_seleccionados'),
    path('agregar_producto_facturacion/', views.agregar_producto_facturacion, name='agregar_producto_facturacion'),
    path('carrito_productos/', views.carrito_productos, name='carrito_productos'),
    path('ir_inicio/', views.ir_inicio, name='ir_inicio'),
    path('eliminar_productos_factura/', views.eliminar_productos_factura, name='eliminar_productos_factura'),
    path('mostrar_carrito_productos/', views.mostrar_carrito_productos, name='mostrar_carrito_productos'),
    path('agregar_datos_cliente/', views.agregar_datos_cliente, name='agregar_datos_cliente'),
    path('eliminar_producto_factura/', views.eliminar_producto_factura, name='eliminar_producto_factura'),
    path('ingreso_stock_seleccionado/', views.ingreso_stock_seleccionado, name='ingreso_stock_seleccionado'),
    path('actualizar_productos_seleccionados/', views.actualizar_productos_seleccionados, name='actualizar_productos_seleccionados'),
    path('registrar_factura/', views.registrar_factura, name='registrar_factura'),
    path('historial_factura/', views.historial_factura, name='historial_factura'),
    path('historialfactura/', views.ir_historialfactura, name='ir_historialfactura'),
    path('borrar_historial_facturas/', views.borrar_historial_facturas, name='borrar_historial_facturas'),
    path("ajustar_todos_precios/", views.ajustar_todos_precios, name="ajustar_todos_precios"),
    path("ingresar_stock_todos_productos/", views.ingresar_stock_todos_productos, name="ingresar_stock_todos_productos"),
    path("historial_facturas/", views.historial_facturas, name="historial_facturas"),
 
 
    


    path('quitar_producto_seleccionado/', quitar_producto_seleccionado, name='quitar_producto_seleccionado'),
    path('limpiar_productos_seleccionados/', views.limpiar_productos_seleccionados, name='limpiar_productos_seleccionados'),
    path('ajustar_precio_seleccionados/', views.ajustar_precio_seleccionados, name='ajustar_precio_seleccionados'),
 
    # Otras URLs de tu aplicación
    


]

