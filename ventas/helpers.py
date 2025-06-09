from ventas.models import Ventas

def obtener_siguiente_numero():
    try:
        ultimo_registro = Ventas.objects.order_by('-nrofactura')[0]
        return ultimo_registro.nrofactura + 1
    except IndexError:
        return 1
