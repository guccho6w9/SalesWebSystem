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
    path('quitar_producto_seleccionado/', quitar_producto_seleccionado, name='quitar_producto_seleccionado'),
    path('limpiar_productos_seleccionados/', views.limpiar_productos_seleccionados, name='limpiar_productos_seleccionados'),
    path('ajustar_precio_seleccionados/', views.ajustar_precio_seleccionados, name='ajustar_precio_seleccionados'),
 
    # Otras URLs de tu aplicación
    


]

