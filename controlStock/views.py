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
from django.utils.translation import activate
from num2words import num2words
from django.template.loader import get_template
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from collections import defaultdict

from django.urls import reverse


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.datastructures import MultiValueDictKeyError
from .models import HistorialProducto
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views import View
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
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

    paginator = Paginator(all_products, 300)
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
        return render(request, 'producto/producto.html')
    else:
        cod = request.POST['cod'].upper()  # Convertir a mayúsculas
        des = request.POST['des'].upper()
        pre = request.POST['pre']
        stock = request.POST['stock']
        try:
            # Verificar si ya existe un producto con el mismo código
            if Producto.objects.filter(cod=cod).exists():
                messages.error(request, '¡Ya existe un Producto con ese Codigo!')
            else:
                # Si no existe, crear el nuevo producto
                producto = Producto.objects.create(cod=cod, des=des, pre=pre, stock=stock)
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
            stock = request.POST['stock']

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
            producto.stock = stock
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
                # Redondear el valor del precio a dos decimales
                pre = round(float(row['pre']), 2)
                Producto.objects.create(
                    cod=row['cod'],
                    des=row['des'],
                    pre=pre,
                    stock=int(row.get('stock', 0))
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
    ws.append(['cod', 'des', 'pre', 'stock'])

    # Agrega datos de productos a la hoja de cálculo
    productos = Producto.objects.all()
    for producto in productos:
        ws.append([producto.cod, producto.des, producto.pre, producto.stock])

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
    # Obtener los productos seleccionados de la sesión
    selected_products = request.session.get('selected_products', [])

    # Si es una solicitud POST, actualizar la lista de productos seleccionados
    if request.method == 'POST':
        try:
            # Obtener los IDs de los productos seleccionados del POST
            selected_products_ids = json.loads(request.POST.get('selected_products', '[]'))
            selected_products_ids = [int(id_pd) for id_pd in selected_products_ids]

            # Filtrar los productos correspondientes a los IDs
            selected_products_queryset = Producto.objects.filter(id_pd__in=selected_products_ids)

            # Guardar la lista de productos seleccionados en la sesión
            request.session['selected_products'] = list(selected_products_queryset.values())

            # Redirigir a la misma página
            return redirect('listar_productos_seleccionados')
        except ValueError:
            # Manejar errores de decodificación JSON
            print("")

    # Renderizar la página con los productos seleccionados
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
    return redirect('producto')

def actualizar_productos_seleccionados(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            # Obtener la lista de productos seleccionados del cuerpo de la solicitud
            selected_products = json.loads(request.body)

            # Guardar la lista de productos seleccionados en la sesión
            request.session['selected_products'] = selected_products

            # Obtener los detalles completos de los productos seleccionados
            selected_products_details = Producto.objects.filter(id_pd__in=selected_products)

            # Convertir los detalles de los productos a un formato adecuado para JSON
            selected_products_details_json = list(selected_products_details.values())

            return JsonResponse({'selected_products': selected_products_details_json})
        except ValueError:
            # Manejar el error si falla la decodificación JSON
            return JsonResponse({'error': 'Error al cargar los productos seleccionados.'}, status=400)

    # Si la solicitud no es AJAX o no es POST, devolver un error
    return JsonResponse({'error': 'Solicitud no válida.'}, status=400)


def agregar_producto_facturacion(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cantidad = int(request.POST.get('cantidad'))
        producto = Producto.objects.get(pk=product_id)
        
        # Verificar si la cantidad ingresada excede el stock disponible
        if cantidad > producto.stock:
            return HttpResponseBadRequest("La cantidad ingresada excede el stock disponible.")
        
        # Calcular el subtotal del producto
        subtotal = producto.pre * cantidad
        
        # Guardar la cantidad y el subtotal en el producto
        producto.cantidad = cantidad
        producto.subtotal = subtotal
        producto.en_carrito = True
        producto.save()
        
        # Redirigir al usuario de vuelta a la página del producto
        return redirect(request.META.get('HTTP_REFERER', 'producto'))
    else:
        return redirect('ir_inicio')
    
def mostrar_carrito_productos(request):
    # Obtener los productos que están en el carrito pero no han sido facturados aún
    productos_en_carrito = Producto.objects.filter(en_carrito=True)
    subtotales = []
    
    # Calcular el subtotal de cada producto multiplicando el precio por la cantidad
    for producto in productos_en_carrito:
        subtotales.append(producto.subtotal)

    # Calcular el total de la factura y convertirlo a palabras
    total = sum(subtotales)
    total_en_palabras = convertir_precio_a_palabras(total)
    
    # Pasar los productos filtrados a la plantilla
    return render(request, 'producto/carrito_productos.html', {
        'factura_productos': productos_en_carrito,
        'total': total,
        'total_en_palabras': total_en_palabras,
        'fecha_actual': timezone.now()
    })

def eliminar_producto_factura(request):
    if request.method == 'POST':
        product_cod = request.POST.get('product_cod')
        print("ID DEL PRODUCTO",product_cod)
        # Obtener el producto específico
        producto = get_object_or_404(Producto, cod=product_cod)

        
        # Cambiar el estado del producto en el carrito a False y resetear la cantidad a 1
        producto.en_carrito = False
        producto.cantidad = 1
        producto.save()
        
        messages.success(request, f"Se ha eliminado el producto {producto.des} de la factura.")
    
    return redirect('mostrar_carrito_productos')

def eliminar_productos_factura(request):
    
    if request.method == 'POST':
        # Actualizar el estado de los productos en el carrito a False
 
        productos_en_carrito = Producto.objects.filter(en_carrito=True)
        productos_en_carrito.update(en_carrito=False)
        
        # Redirigir de vuelta a la página de productos
        return redirect('producto')

    # Si no es una solicitud POST, redirigir a alguna página de error o de inicio
    return redirect('inicio')

def ir_inicio(request):
    return render(request, 'producto/producto.html')

def carrito_productos(request):
    # Obtener los productos seleccionados de la sesión

        return render(request, 'producto/carrito_productos.html')


def convertir_precio_a_palabras(precio):
    activate('es')  # Activa el idioma español para la conversión

    # Dividir el precio en la parte entera y decimal
    parte_entera = int(precio)
    parte_decimal = round(precio - parte_entera, 2)

    # Convertir la parte entera a palabras
    parte_entera_palabras = num2words(parte_entera, lang='es')

    # Convertir la parte decimal a palabras, limitando a dos decimales
    if parte_decimal > 0:
        parte_decimal_palabras = 'con ' + num2words(int(parte_decimal * 100), lang='es') + ' centavos'
    else:
        parte_decimal_palabras = ''

    # Combinar las partes en una frase
    if parte_decimal_palabras:
        total_en_palabras = f"{parte_entera_palabras} pesos {parte_decimal_palabras}"
    else:
        total_en_palabras = f"{parte_entera_palabras} pesos"

    return total_en_palabras


def agregar_datos_cliente(request):
    if request.method == 'POST':
        # Verificar si ya existe un cliente en la base de datos
        if Cliente.objects.exists():
            # Si existe, obtén el cliente existente
            cliente = Cliente.objects.first()
            # Actualiza los datos del cliente con los nuevos datos del formulario
            cliente.nombre = request.POST['cliente']
            cliente.domicilio = request.POST['domicilio']
            cliente.ciudad = request.POST['ciudad']
            cliente.condicion_venta = request.POST['condicion_venta']
            cliente.condicion_fiscal = request.POST['condicion_fiscal']
            cliente.cuit_dni = request.POST['cuit_dni']
            cliente.fecha_vencimiento_pago = request.POST['fecha_vencimiento_pago']
            cliente.save()
        else:
            # Si no hay ningún cliente en la base de datos, crea uno nuevo
            cliente = Cliente.objects.create(
                nombre=request.POST['cliente'],
                domicilio=request.POST['domicilio'],
                ciudad=request.POST['ciudad'],
                condicion_venta=request.POST['condicion_venta'],
                condicion_fiscal=request.POST['condicion_fiscal'],
                cuit_dni=request.POST['cuit_dni'],
                fecha_vencimiento_pago=request.POST['fecha_vencimiento_pago']
            )
        # Redirigir a la página de productos después de agregar o actualizar al cliente
        return redirect('producto')
    else:
        # Si no es una solicitud POST, redirige a la página de productos
        return redirect('producto') # Si no es una solicitud POST, redirige a la página correspondiente
    
def ingreso_stock_seleccionado(request):
    if request.method == 'POST':
        try:
            selected_products = request.session.get('selected_products', [])
            cantidad = int(request.POST.get('cantidad', 0))

            for product in selected_products:
                producto = Producto.objects.get(id_pd=product['id_pd'])
                print("LA CANTIDAD:", producto.stock, cantidad)
                producto.stock += cantidad
                producto.save()

                # Actualizar la cantidad en la lista de productos seleccionados en la sesión
                product['stock'] = producto.stock

            messages.success(request, f"¡Stock aumentado en {cantidad} unidades para todos los productos seleccionados!")

            # Guardar la lista actualizada en la sesión
            request.session['selected_products'] = selected_products

            return render(request, 'listar_productos_seleccionados.html', {'selected_products': selected_products})
        except ValueError:
            messages.error(request, 'Cantidad inválida. Ingrese un número válido.')

    # Redirige a la página principal de productos si ocurre algún error
    return redirect('producto')


def registrar_factura(request):
    if request.method == 'POST':
        # Obtener datos del cliente
        cliente = request.POST.get('cliente')
        domicilio = request.POST.get('domicilio')
        ciudad = request.POST.get('ciudad')
        condicion_venta = request.POST.get('condicion_venta')
        condicion_fiscal = request.POST.get('condicion_fiscal')
        cuit_dni = request.POST.get('cuit_dni')

        # Obtener los productos de la factura
        factura_productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        subtotales = request.POST.getlist('subtotal')

        # Inicializar el total de la factura
        total_factura = 0

        # Crear una instancia de HistorialFactura
        factura = HistorialFactura.objects.create(
            fecha=timezone.now(),
            nombre_cliente=cliente,
            domicilio=domicilio,
            ciudad=ciudad,
            condicion_venta=condicion_venta,
            condicion_fiscal=condicion_fiscal,
            cuit_dni=cuit_dni,
        )

        # Crear un registro en FacturaProducto para cada producto en la factura
        for prod_id, cantidad, subtotal in zip(factura_productos, cantidades, subtotales):
            producto_obj = Producto.objects.get(pk=prod_id)
            cantidad_entero = int(cantidad)
            subtotal_float = float(subtotal.replace(',', '.'))  # Reemplazar coma por punto para asegurar que sea un número flotante válido

            # Crear un nuevo registro en FacturaProducto
            FacturaProducto.objects.create(
                producto=producto_obj,
                cantidad=cantidad_entero,
                subtotal_calculado=subtotal_float,
                factura=factura,
            )

            # Calcular el subtotal del producto y sumarlo al total de la factura
            total_factura += subtotal_float

            # Actualizar el stock del producto
            producto_obj.stock -= cantidad_entero
            producto_obj.carrito = False  # Restablecer a carrito=False
            producto_obj.save()

        # Asignar el total de la factura a la instancia de HistorialFactura
        factura.total = total_factura
        factura.save()

        # Redirigir a la página de historial de facturas
        return redirect('ir_historialfactura')
    else:
        # Manejar el caso en el que no se reciba una solicitud POST correctamente
        return HttpResponseBadRequest('La solicitud debe ser de tipo POST')
    

def ir_historialfactura(request):
    # Obtener todas las facturas de la base de datos
    facturas = HistorialFactura.objects.all()
    
    return render(request, 'producto/historial_factura.html', {'facturas': facturas})


def historial_factura(request):
    # Obtener todas las facturas de la base de datos
    facturas = FacturaProducto.objects.all().select_related('producto')  # Incluye la descripción del producto
    return render(request, 'producto/historial_factura.html', {'facturas': facturas})


def borrar_historial_facturas(request):
    if request.method == 'POST':
        # Borrar todos los registros del historial de facturas
        HistorialFactura.objects.all().delete()
        return HttpResponseRedirect(reverse('ir_historialfactura'))