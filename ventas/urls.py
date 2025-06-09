from django.urls import path
from .views import registrar_venta, lista_ventas, detalle_venta

urlpatterns = [
    path('', lista_ventas, name='lista_ventas'),
    path('<int:venta_id>/', detalle_venta, name='detalle_venta'),
    path('registrar/', registrar_venta, name='registrar_venta'),
]
