# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Clientes(models.Model):
    id = models.IntegerField(primary_key=True)
    nombres = models.CharField(max_length=200, blank=True, null=True)
    apellidos = models.CharField(max_length=200, blank=True, null=True)
    documentonro = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=200, blank=True, null=True)
    activo = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientes'

    def __str__(self):
        return f'{self.nombres} {self.apellidos} - {self.documentonro}'


class CuentasCobrar(models.Model):
    id = models.IntegerField(primary_key=True)
    tabla = models.CharField(max_length=100)
    tablaid = models.IntegerField()
    cuota = models.IntegerField()
    importe = models.DecimalField(max_digits=18, decimal_places=5)
    cobrado = models.DecimalField(max_digits=18, decimal_places=5)
    vence = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cuentas_cobrar'
        unique_together = (('tabla', 'tablaid', 'cuota'),)


class Depositos(models.Model):
    id = models.IntegerField(primary_key=True)
    deposito = models.CharField(max_length=200)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'depositos'

    def __str__(self):
        return self.deposito


class Monedas(models.Model):
    id = models.IntegerField(primary_key=True)
    moneda = models.CharField(max_length=50)
    abrebiatura = models.CharField(max_length=5)
    decimales = models.IntegerField()
    activo = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'monedas'

    def __str__(self):
        return f'{self.abrebiatura} - {self.moneda}'


class PlazoDetalles(models.Model):
    id = models.IntegerField(primary_key=True)
    plazoid = models.ForeignKey('Plazos', models.DO_NOTHING, db_column='plazoid')
    cuota = models.IntegerField()
    dias = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'plazo_detalles'
        unique_together = (('plazoid', 'cuota'),)


class Plazos(models.Model):
    id = models.IntegerField(primary_key=True)
    plazo = models.CharField(max_length=100)
    tipoid = models.IntegerField()
    cuotas = models.IntegerField()
    irregular = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'plazos'

    def __str__(self):
        return f'{self.plazo} - {self.cuotas} cuotas'


class TalonarioDetalle(models.Model):
    id = models.IntegerField(primary_key=True)
    talonarioid = models.ForeignKey('Talonarios', models.DO_NOTHING, db_column='talonarioid')
    tabla = models.CharField(max_length=100)
    tablaid = models.IntegerField()
    talonarionro = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'talonario_detalle'
        unique_together = (('talonarioid', 'talonarionro'),)


class Talonarios(models.Model):
    id = models.IntegerField(primary_key=True)
    nroinicial = models.IntegerField()
    nrofinal = models.IntegerField()
    seriea = models.CharField(max_length=5)
    serieb = models.CharField(max_length=5)
    timbrado = models.CharField(max_length=15)
    vigenciaincio = models.DateField()
    vigenciafin = models.DateField()
    activo = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'talonarios'

    def __str__(self):
        return f'{self.seriea}-{self.serieb}'


class TiposDocumento(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=200)
    abrebiatura = models.CharField(max_length=5)
    tipoid = models.IntegerField()
    activo = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'tipos_documento'

    def __str__(self):
        return f'{self.abrebiatura} - {self.tipo}'


class Ventas(models.Model):
    id = models.IntegerField(primary_key=True)
    fechaproceso = models.DateTimeField(blank=True, null=True)
    fechafactura = models.DateTimeField(blank=True, null=True)
    clienteid = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='clienteid')
    serie = models.CharField(max_length=10, blank=True, null=True)
    nrofactura = models.IntegerField()
    totalexento = models.DecimalField(max_digits=18, decimal_places=5)
    totalimpuesto = models.DecimalField(max_digits=18, decimal_places=5)
    totalbase = models.DecimalField(max_digits=18, decimal_places=5)
    totalfactura = models.DecimalField(max_digits=18, decimal_places=5)
    depositoid = models.ForeignKey(Depositos, models.DO_NOTHING, db_column='depositoid')
    monedaid = models.ForeignKey(Monedas, models.DO_NOTHING, db_column='monedaid')
    tipodocid = models.ForeignKey(TiposDocumento, models.DO_NOTHING, db_column='tipodocid')
    plazoid = models.ForeignKey(Plazos, models.DO_NOTHING, db_column='plazoid')
    talonarioid = models.ForeignKey(Talonarios, models.DO_NOTHING, db_column='talonarioid')

    class Meta:
        managed = False
        db_table = 'ventas'

    def __str__(self):
        return f'{self.serie}-{self.nrofactura}'
