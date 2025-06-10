from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from .helpers import obtener_siguiente_numero
from django.contrib import messages
from django.db.models import Q, Max
from .models import Ventas, Clientes, TiposDocumento, Plazos, Monedas, Depositos, Talonarios, \
    CuentasCobrar, PlazoDetalles
from django.http import JsonResponse
from datetime import datetime, timedelta

class VentaForm(forms.ModelForm):
    class Meta:
        model = Ventas
        fields = ['fechafactura', 'clienteid', 'tipodocid', 'plazoid', 'talonarioid', 'depositoid', 
                  'monedaid', 'totalbase', 'totalimpuesto', 'totalexento']
        widgets = {
            'fechafactura': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Seleccione la fecha'
                }
            ),
            'clienteid': forms.Select(attrs={'class': 'form-control'}),
            'tipodocid': forms.Select(attrs={'class': 'form-control'}),
            'plazoid': forms.Select(attrs={'class': 'form-control'}),
            'talonarioid': forms.Select(attrs={'class': 'form-control'}),
            'depositoid': forms.Select(attrs={'class': 'form-control'}),
            'monedaid': forms.Select(attrs={'class': 'form-control'}),
            'totalbase': forms.NumberInput(attrs={'class': 'form-control', 'thousands_separator': ','}),
            'totalimpuesto': forms.NumberInput(attrs={'class': 'form-control'}),
            'totalexento': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo opciones activas
        self.fields['clienteid'].queryset = Clientes.objects.filter(activo=1)
        self.fields['tipodocid'].queryset = TiposDocumento.objects.filter(activo=1)
        self.fields['plazoid'].queryset = Plazos.objects.all()
        self.fields['talonarioid'].queryset = Talonarios.objects.filter(activo=1)
        
        # Agregar clases CSS a todos los campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

def registrar_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            try:
                venta = form.save(commit=False)
                venta.id = Ventas.objects.aggregate(max_id=Max('id'))['max_id'] + 1 if Ventas.objects.exists() else 1
                venta.fechaproceso = venta.fechafactura
                venta.serie = f'{venta.talonarioid}'
                venta.nrofactura = obtener_siguiente_numero()
                venta.totalfactura = venta.totalbase + venta.totalimpuesto # + venta.totalexento # No sé si exento se suma o se resta
                venta.save()
                
                messages.success(request, 'Venta registrada exitosamente!')
                return redirect('lista_ventas')
            except Exception as e:
                messages.error(request, f'Error al registrar la venta: {str(e)}')
    else:
        form = VentaForm()
    
    context = {
        'form': form,
        'title': 'Registro de Nueva Venta',
    }
    return render(request, 'ventas/registrar_venta.html', context)

def lista_ventas(request):
    # Obtener todas las ventas ordenadas por fecha más reciente
    ventas = Ventas.objects.all().order_by('-fechafactura', '-nrofactura')
    
    # Búsqueda (opcional)
    query = request.GET.get('q')
    if query:
        ventas = ventas.filter(
            Q(nrofactura__icontains=query) |
            Q(clienteid__nombres__icontains=query) |
            Q(clienteid__apellidos__icontains=query) |
            Q(clienteid__documentonro__icontains=query)
        )
    
    context = {
        'ventas': ventas,
        'title': 'Listado de Ventas',
    }
    return render(request, 'ventas/lista_ventas.html', context)


class PagoCuotaForm(forms.Form):
    monto = forms.DecimalField(
        label='Monto a pagar',
        max_digits=18,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01'
        })
    )
    

def detalle_venta(request, venta_id):
    venta = get_object_or_404(Ventas, pk=venta_id)
    cuotas = None
    
    # Manejar el POST para registrar pagos
    if request.method == 'POST' and 'registrar_pago' in request.POST:
        form = PagoCuotaForm(request.POST)
        if form.is_valid():
            cuota_id = request.POST.get('cuota_id')
            monto = form.cleaned_data['monto']
            
            try:
                cuota = CuentasCobrar.objects.get(id=cuota_id)
                # Actualizar el monto cobrado
                cuota.cobrado += monto
                if cuota.cobrado > cuota.importe:
                    messages.warning(request, 'El monto ingresado supera el saldo de la cuota')
                else:
                    cuota.save()
                    messages.success(request, f'Pago de {monto} registrado en la cuota {cuota.cuota}')
                    return redirect('detalle_venta', venta_id=venta.id)
            except CuentasCobrar.DoesNotExist:
                messages.error(request, 'Cuota no encontrada')
    
    # Verificar si es una venta a crédito
    if venta.plazoid and venta.plazoid.cuotas > 1:
        cuotas = CuentasCobrar.objects.filter(
            tabla='VENTAS',
            tablaid=venta.id
        ).order_by('cuota')
        
        plazo_detalles = PlazoDetalles.objects.filter(plazoid=venta.plazoid).order_by('cuota')
        
        if plazo_detalles.exists():
            for cuota in cuotas:
                detalle = plazo_detalles.filter(cuota=cuota.cuota).first()
                if detalle:
                    cuota.dias_plazo = detalle.dias
    
    form = PagoCuotaForm()
    
    context = {
        'venta': venta,
        'cuotas': cuotas,
        'title': f'Detalle de Venta {venta.serie}-{venta.nrofactura}',
        'form': form,
    }
    return render(request, 'ventas/detalle_venta.html', context)

def calcular_cuotas_ajax(request):
    if request.method == 'GET':
        try:
            tipodocid = int(request.GET.get('tipodocid'))
            plazoid = int(request.GET.get('plazoid'))
            monedaid = int(request.GET.get('monedaid'))
            totalfactura = float(request.GET.get('totalfactura'))
            fechafactura_str = request.GET.get('fechafactura')

            if not fechafactura_str:
                raise ValueError('Fecha de factura requerida.')

            fechafactura = datetime.strptime(fechafactura_str, '%Y-%m-%d').date()

            tipo_doc = TiposDocumento.objects.get(pk=tipodocid)
            plazo = Plazos.objects.get(pk=plazoid)
            moneda = Monedas.objects.get(pk=monedaid)

            cuotas = []
            decimales = moneda.decimales
            importe_base = round(totalfactura / plazo.cuotas, decimales)
            ultima_cuota = round(totalfactura - (importe_base * (plazo.cuotas - 1)), decimales)

            if tipo_doc.tipoid == 0:  # Contado
                cuotas.append({
                    'cuota': 1,
                    'importe': round(totalfactura, decimales),
                    'vence': fechafactura.isoformat(),
                })
            else:
                for i in range(1, plazo.cuotas + 1):
                    if plazo.irregular:
                        detalle = PlazoDetalles.objects.get(plazoid=plazo, cuota=i)
                        dias = detalle.dias
                        vto = fechafactura + timedelta(days=dias)
                    else:
                        vto = fechafactura + timedelta(days=30 * i)

                    cuotas.append({
                        'cuota': i,
                        'importe': ultima_cuota if i == plazo.cuotas else importe_base,
                        'vence': vto.isoformat(),
                    })

            return JsonResponse({'status': 'ok', 'cuotas': cuotas})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
def crear_cliente_modal(request):
    if request.method == 'POST':
        # Obtener el siguiente ID disponible
        ultimo_id = Clientes.objects.aggregate(max_id=Max('id'))['max_id'] or 0
        nuevo_id = ultimo_id + 1

        Clientes.objects.create(
            id=nuevo_id,
            nombres=request.POST.get('nombres'),
            apellidos=request.POST.get('apellidos'),
            documentonro=request.POST.get('documentonro'),
            direccion=request.POST.get('direccion'),
            email=request.POST.get('email'),
            telefono=request.POST.get('telefono'),
            activo=1
        )

        from django.contrib import messages
        messages.success(request, 'Cliente creado correctamente.')

    return redirect('lista_ventas')