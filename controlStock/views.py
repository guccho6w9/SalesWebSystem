from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from openpyxl import load_workbook
from django.http import HttpResponse
from openpyxl import Workbook
import pandas as pd
from django.contrib import messages
from django.db.models import Q, F
import json
from django.forms.models import model_to_dict



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.datastructures import MultiValueDictKeyError
from .models import HistorialProducto
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views import View


# DB
from django.db.utils import IntegrityError
from django.db.models import Case, When
"""
from django.shortcuts import render, redirect
from .models import *
from .utils import *
from django.contrib import messages
from datetime import datetime
import pytz
# DB
from django.db.utils import IntegrityError
from django.db.models import Case, When
# Login
from django.contrib.auth.decorators import login_required
# Create your views here.
from accounts.views import user_has_required_group, access_denied
from django.contrib.auth.decorators import user_passes_test
"""

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

# PRODUCTO
from django.db.models import Q

def producto(request):
    # Retrieve all products
    all_products = Producto.objects.all()

    # Search functionality
    query = request.GET.get('q', '')
    if query:
        all_products = all_products.filter(
            Q(cod__icontains=query) |
            Q(des__icontains=query)
        )

    # Obtener parámetros de ordenamiento y dirección
    order_by = request.GET.get('order_by', 'id_pd')
    direction = request.GET.get('direction', 'asc')

    # Verificar el campo de ordenamiento y aplicar la dirección adecuada
    if order_by == 'id_pd':
        all_products = all_products.order_by('-id_pd' if direction == 'desc' else 'id_pd')
    elif order_by == 'cod':
        all_products = all_products.order_by('-cod' if direction == 'desc' else 'cod')
    elif order_by == 'des':
        all_products = all_products.order_by('-des' if direction == 'desc' else 'des')
    elif order_by == 'pre':
        all_products = all_products.order_by('-pre' if direction == 'desc' else 'pre')

    paginator = Paginator(all_products, 150)
    page = request.GET.get('page')

    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)

    # Add an index to each product
    for i, product in enumerate(productos, start=(productos.number - 1) * productos.paginator.per_page + 1):
        product.index = i

    context = {'productos': productos, 'query': query, 'order_by': order_by, 'direction': direction}
    return render(request, 'producto\\producto.html', context)






def listar_productos(request):
    productos = Producto.objects.all()[:200]
    return render(request, 'producto.html', {'productos': productos})
    #return render(request, 'producto\\producto.html', context)


def registrarProducto(request):
    if request.method == 'GET':
        return render(request, 'producto\\producto.html')
    else:
        cod = request.POST['cod']  # Convertir a mayúsculas
        des = request.POST['des'].upper()
        pre = request.POST['pre']
        try:
            producto = Producto.objects.create(cod=cod, des=des, pre=pre)
            messages.success(request, '¡Registrado!')
        except IntegrityError as e:
            messages.error(request, '¡Ya existe un Producto con ese Codigo!')
        except Exception as e:
            messages.error(request, f"¡Ocurrió un error! {e}")
    return redirect('producto')


def eliminarProducto(request, id_pd):
    # Obtener el producto
    producto = Producto.objects.get(id_pd=id_pd)

    # Lógica para eliminar el producto
    producto.delete()
    messages.success(request, '¡Eliminado!')

    # Después de eliminar, redirigir a la URL actual
    current_url = request.GET.get('current_url', '/')
    return redirect(current_url)



def edicionProducto(request, id_pd):
    producto = Producto.objects.get(id_pd=id_pd)
    return render(request, "producto\\edicionProducto.html", {"producto": producto})

def editarProducto(request):
    if request.method == 'POST':
        try:
            id_pd = request.POST['id_pd']
            cod = request.POST['cod']
            des = request.POST['des']
            pre = request.POST['pre']

            # Obtén el producto antes de modificarlo
            producto = get_object_or_404(Producto, id_pd=id_pd)

            # Guarda el cambio en el historial
            HistorialProducto.objects.create(
                producto=producto,
                nombre_anterior=producto.des,
                cod_anterior=producto.cod,
                id_anterior=producto.id_pd,
                precio_anterior=producto.pre,
                precio_actualizado=pre,  # Nuevo campo para el precio actualizado
                fecha_cambio=timezone.now()
            )

            # Actualiza los datos del producto
            producto.cod = cod
            producto.des = des
            producto.pre = pre
            producto.save()

            messages.success(request, '¡Datos actualizados y cambio registrado en el historial!')
            return redirect('producto')  # Cambia 'producto' con el nombre correcto de tu URL de productos

        except ValueError:
            messages.error(request, 'Valores inválidos. Ingrese valores válidos.')
            return redirect('producto')  # Cambia 'producto' con el nombre correcto de tu URL de productos

    return redirect('producto')  # Cambia 'producto' con el nombre correcto de tu URL de productos





def import_from_excel(request):
    if request.method == 'POST':

        try:
            excel_file = request.FILES['excel_file']
        except MultiValueDictKeyError:
            messages.error(request, 'No se seleccionó ningún archivo para importar.')
            return redirect('import_from_excel')
        

        # Verificar si el archivo es un archivo Excel
        if not excel_file.name.endswith('.xlsx'):
            messages.error(request, 'El archivo seleccionado no es un archivo Excel válido.')
            return redirect('import_from_excel')
        

        # Procesar el archivo Excel con pandas
        try:
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                Producto.objects.create(
                    cod=row['cod'],
                    des=row['des'],
                    pre=float(row['pre']),
                    aju=row['aju'],
                    ofe=row['ofe']
                )
            messages.success(request, 'Importación exitosa.')
        except Exception as e:
            messages.error(request, f"Ocurrió un error al importar desde el archivo Excel: {e}")
            return redirect('import_from_excel')

        return render(request, 'import_form.html')

    return render(request, 'import_form.html')


def exportar_productos(request):
    # Lógica para exportar productos a un archivo Excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="productos.xlsx"'

    # Crea un libro de trabajo y una hoja de cálculo
    wb = Workbook()
    ws = wb.active

    # Agrega encabezados a la hoja de cálculo
    ws.append(['cod', 'des', 'pre', 'aju', 'ofe'])

    # Agrega datos de productos a la hoja de cálculo
    productos = Producto.objects.all()
    for producto in productos:
        ws.append([producto.cod, producto.des, producto.pre])

    # Guarda el libro de trabajo en la respuesta
    wb.save(response)

    return response


def borrarTodosProductos(request):
    Producto.objects.all().delete()
    messages.success(request, '¡Todos los productos han sido eliminados!')
    return redirect('producto')




def aumentar_precio(request, id_pd):
    producto = get_object_or_404(Producto, id_pd=id_pd)

    if request.method == 'POST':
        try:
            porcentaje = float(request.POST.get('porcentaje', 0))
            nuevo_precio = producto.pre * (1 + porcentaje / 100)

            # Guarda el cambio en el historial
            HistorialProducto.objects.create(
                producto=producto,
                cod_anterior=producto.cod,
                nombre_anterior=producto.des,
                id_anterior=producto.id_pd,
                precio_anterior=producto.pre,
                precio_actualizado=round(nuevo_precio, 2),  # Nuevo campo para el precio actualizado
                fecha_cambio=timezone.now()
            )

            producto.pre = round(nuevo_precio, 2)
            producto.save()

            messages.success(request, f"¡Precio aumentado en {porcentaje}%!")

            # Redirige a la página anterior
            return redirect(request.META.get('HTTP_REFERER', 'producto'))
        except ValueError:
            messages.error(request, 'Porcentaje inválido. Ingrese un número válido.')
            return render(request, 'aumentar_precio.html', {'producto': producto})

    return render(request, 'aumentar_precio.html', {'producto': producto})



def ver_historial_producto(request, id_pd):
    # Lógica para obtener el historial del producto (si es necesario)
    producto = get_object_or_404(Producto, id_pd=id_pd)
    historial = HistorialProducto.objects.filter(producto=producto).order_by('-fecha_cambio')  # Ordena por fecha de cambio descendente

    # Puedes agregar lógica adicional aquí según tus necesidades
    print(historial)
    print(f'id_pd recibido: {id_pd}')

    return render(request, 'producto/historial_producto.html', {'producto': producto, 'historial': historial})

def listar_productos_seleccionados(request):
    if request.method == 'POST':
        try:
            selected_products = json.loads(request.POST.get('selected_products', '[]'))
            selected_products = [int(id_pd) for id_pd in selected_products]
            selected_products = Producto.objects.filter(id_pd__in=selected_products)

            # Save the list of dictionaries in the session
            request.session['selected_products'] = list(selected_products.values())

            return render(request, 'listar_productos_seleccionados.html', {'selected_products': selected_products})
        except ValueError:
            # Handle the case where the JSON decoding fails
            messages.error(request, 'Error al cargar los productos seleccionados.')
            return render(request, 'listar_productos_seleccionados.html', {'selected_products': []})

    # Load the selected products from the session
    selected_products = request.session.get('selected_products', [])
    
    return render(request, 'listar_productos_seleccionados.html', {'selected_products': selected_products})



def quitar_producto_seleccionado(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        # Obtener la lista actual de productos seleccionados desde la sesión
        selected_products = request.session.get('selected_products', [])
        print("Selected Products in Session before removal:", selected_products)

        try:
            # Convertir el product_id a int
            product_id = int(product_id)
            print("producto a eliminar antes del if:", product_id)

            # Obtener el producto correspondiente al product_id
            producto_to_remove = get_object_or_404(Producto, id_pd=product_id)

            # Asegurarse de que el producto esté en la lista antes de intentar eliminarlo
            if any(prod['id_pd'] == product_id for prod in selected_products):
                print("producto a eliminar en el if:", product_id)

                # Quitar el producto de la lista
                selected_products = [prod for prod in selected_products if prod['id_pd'] != product_id]

                # Guardar la lista actualizada en la sesión
                print("Selected Products in Session after removal:", selected_products)
                request.session['selected_products'] = selected_products
        except (ValueError, KeyError):
            pass

    return redirect('listar_productos_seleccionados')


def limpiar_productos_seleccionados(request):
    # Limpiar la lista de productos seleccionados en la sesión
    request.session.pop('selected_products', None)

    # Redirigir a la página principal de productos
    return redirect('producto')


def ajustar_precio_seleccionados(request):
    if request.method == 'POST':
        try:
            selected_products = request.session.get('selected_products', [])
            porcentaje = float(request.POST.get('porcentaje', 0))

            for product in selected_products:
                id_pd = product['id_pd']
                producto = Producto.objects.get(id_pd=id_pd)

                # Guarda el cambio en el historial
                HistorialProducto.objects.create(
                    producto=producto,
                    cod_anterior=producto.cod,
                    nombre_anterior=producto.des,
                    id_anterior=producto.id_pd,
                    precio_anterior=producto.pre,
                    precio_actualizado=round(producto.pre * (1 + porcentaje / 100), 2),
                    fecha_cambio=timezone.now()
                )

                # Ajusta el precio del producto
                producto.pre = round(producto.pre * (1 + porcentaje / 100), 2)
                producto.save()

                # Actualiza el precio en la lista de productos seleccionados en la sesión
                product['pre'] = producto.pre

            messages.success(request, f"¡Precios ajustados en {porcentaje}% para todos los productos seleccionados!")

            # Guardar la lista actualizada en la sesión
            request.session['selected_products'] = selected_products

            return render(request, 'listar_productos_seleccionados.html', {'selected_products': selected_products})
        except ValueError:
            messages.error(request, 'Porcentaje inválido. Ingrese un número válido.')

    # Redirige a la página principal de productos si ocurre algún error
    return redirect('listar_productos_seleccionados')


