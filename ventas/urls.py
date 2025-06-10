from django.urls import path
from .views import registrar_venta, lista_ventas, detalle_venta,calcular_cuotas_ajax,crear_cliente_modal


urlpatterns = [
    path('', lista_ventas, name='lista_ventas'),
    path('<int:venta_id>/', detalle_venta, name='detalle_venta'),
    path('registrar/', registrar_venta, name='registrar_venta'),
    path('calcular-cuotas/', calcular_cuotas_ajax, name='calcular_cuotas'),
    path('clientes/nuevo/', crear_cliente_modal, name='crear_cliente_modal')
]
