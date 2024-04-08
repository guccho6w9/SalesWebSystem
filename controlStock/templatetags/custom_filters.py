from django import template
import locale
register = template.Library()

@register.filter(name='add_dot_separator')
def add_dot_separator(value):
    # Dividir el valor en parte entera y parte decimal
    parts = str(value).split(',')
    # Obtener la parte entera y la parte decimal
    int_part = parts[0]
    decimal_part = parts[1] if len(parts) > 1 else '00'
    # Formatear la parte entera con punto separador de miles
    int_part = "{:,}".format(int(int_part)).replace(',', '.')
    # Unir las partes nuevamente
    return ','.join([int_part, decimal_part])