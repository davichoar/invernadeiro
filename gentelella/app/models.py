from __future__ import unicode_literals
from django.db import models


class Auditoria(models.Model):
    idauditoria = models.IntegerField(primary_key=True)
    idusuario = models.IntegerField()
    tabla = models.CharField(max_length=255)
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField()
    dataantigua = models.TextField()
    datanueva = models.TextField()


class Cronograma(models.Model):
    idcronograma = models.IntegerField(primary_key=True)
    idmodulo = models.IntegerField()
    horainicio = models.IntegerField()
    horafin = models.IntegerField()
    temperatura = models.FloatField()
    humedadambiente = models.FloatField()
    humedadtierra = models.FloatField()
    concentracionco2 = models.FloatField()
    luz = models.BooleanField()
    nivelagua = models.FloatField()


class Foto(models.Model):
    idfoto = models.IntegerField(primary_key=True)
    idmodulo = models.IntegerField(blank=True, null=True)
    ruta = models.CharField(max_length=255)
    nombresinextension = models.CharField(max_length=255)
    extension = models.CharField(max_length=255)
    nombrefoto = models.CharField(max_length=255)
    fecharegistro = models.DateTimeField()


class Historiainvernadero(models.Model):
    idhistoriainvernadero = models.IntegerField(primary_key=True)
    idinvernadero = models.IntegerField()
    nivelenergia = models.FloatField(blank=True, null=True)
    niveltanqueagua = models.FloatField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    fecharegistro = models.DateTimeField()


class Historiamodulo(models.Model):
    idhistoriamodulo = models.IntegerField(primary_key=True)
    idmodulo = models.IntegerField()
    temperatura = models.FloatField(blank=True, null=True)
    humedadtierra = models.FloatField(blank=True, null=True)
    humedadambiente = models.FloatField(blank=True, null=True)
    nivelagua = models.FloatField(blank=True, null=True)
    concentracionco2 = models.FloatField(blank=True, null=True)
    luz = models.NullBooleanField()
    fecharegistro = models.DateTimeField()
    comentario = models.CharField(max_length=255, blank=True, null=True)


class Historiapanel(models.Model):
    idhistoriapanel = models.IntegerField(primary_key=True)
    idpanel = models.IntegerField()
    encendido = models.BooleanField()
    fecharegistro = models.DateTimeField()


class Historiaplanta(models.Model):
    idhistoriaplanta = models.IntegerField(primary_key=True)
    idplanta = models.IntegerField()
    idzona = models.IntegerField()
    humedad = models.FloatField()
    comentario = models.CharField(max_length=255, blank=True, null=True)
    fecharegistro = models.DateTimeField()


class Historiasemilla(models.Model):
    idhistoriasemilla = models.IntegerField(primary_key=True)
    idsemilla = models.IntegerField()
    idmodulo = models.IntegerField()
    posx = models.IntegerField()
    posy = models.IntegerField()
    comentario = models.CharField(max_length=255, blank=True, null=True)
    fecharegistro = models.DateTimeField()


class Historiazona(models.Model):
    idhistoriazona = models.IntegerField(primary_key=True)
    idzona = models.IntegerField()
    temperatura = models.FloatField(blank=True, null=True)
    ph = models.FloatField(blank=True, null=True)
    concentracionco2 = models.FloatField(blank=True, null=True)
    fecharegistro = models.DateTimeField()


class Invernadero(models.Model):
    idinvernadero = models.IntegerField(primary_key=True)
    idadmin = models.IntegerField()
    codigoinvernaderojson = models.IntegerField()
    nombre = models.CharField(max_length=255)
    fechacreacion = models.DateTimeField()
    area = models.FloatField(blank=True, null=True)
    niveltanqueaguaideal = models.FloatField(blank=True, null=True)
    niveltanqueaguamin = models.FloatField(blank=True, null=True)
    niveltanqueaguamax = models.FloatField(blank=True, null=True)
    nivelenergiaideal = models.FloatField(blank=True, null=True)
    nivelenergiamin = models.FloatField(blank=True, null=True)
    nivelenergiamax = models.FloatField(blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    condicionesshidas = models.NullBooleanField()
    idusuarioauditado = models.IntegerField()
    habilitado = models.BooleanField()


class Modulosemilla(models.Model):
    idmodulo = models.IntegerField(primary_key=True)
    codigomodulojson = models.IntegerField()
    temperaturaideal = models.FloatField(blank=True, null=True)
    temperaturamin = models.FloatField(blank=True, null=True)
    temperaturamax = models.FloatField(blank=True, null=True)
    humedadtierraideal = models.FloatField(blank=True, null=True)
    humedadtierramin = models.FloatField(blank=True, null=True)
    humedadtierramax = models.FloatField(blank=True, null=True)
    humedadambienteideal = models.FloatField(blank=True, null=True)
    humedadambientemin = models.FloatField(blank=True, null=True)
    humedadambientemax = models.FloatField(blank=True, null=True)
    concentracionco2ideal = models.FloatField(blank=True, null=True)
    concentracionco2min = models.FloatField(blank=True, null=True)
    concentracionco2max = models.FloatField(blank=True, null=True)
    nivelaguaideal = models.FloatField(blank=True, null=True)
    nivelaguamin = models.FloatField(blank=True, null=True)
    nivelaguamax = models.FloatField(blank=True, null=True)
    filas = models.IntegerField()
    columnas = models.IntegerField()
    fechacreacion = models.DateTimeField()
    habilitado = models.BooleanField()
    idusuarioauditado = models.IntegerField()
    condicionesshidas = models.NullBooleanField()


class Panelluz(models.Model):
    idpanel = models.IntegerField(primary_key=True)
    codigopaneljson = models.IntegerField()
    idzona = models.IntegerField()
    habilitado = models.BooleanField()


class Permiso(models.Model):
    idpermiso = models.IntegerField(primary_key=True)
    nombrepermiso = models.CharField(max_length=255)
    habilitado = models.BooleanField()


class Permisoxrol(models.Model):
    idrol = models.IntegerField(primary_key=True)
    idpermiso = models.IntegerField()


class Planta(models.Model):
    idplanta = models.IntegerField(primary_key=True)
    idtipoplanta = models.IntegerField()
    idzona = models.IntegerField()
    idsemilla = models.IntegerField(blank=True, null=True)
    codigoplantajson = models.IntegerField()
    fechacreacion = models.DateTimeField()
    humedadmin = models.FloatField(blank=True, null=True)
    humedadideal = models.FloatField(blank=True, null=True)
    humedadmax = models.FloatField(blank=True, null=True)
    idusuarioauditado = models.IntegerField()
    condicionesshidas = models.NullBooleanField()
    habilitado = models.BooleanField()


class Rol(models.Model):
    idrol = models.IntegerField(primary_key=True)
    nombrerol = models.CharField(max_length=255)
    habilitado = models.BooleanField()


class Semilla(models.Model):
    idsemilla = models.IntegerField(primary_key=True)
    idtipoplanta = models.IntegerField()
    idmodulo = models.IntegerField()
    fechacreacion = models.DateTimeField()
    habilitado = models.BooleanField()
    idusuarioauditado = models.IntegerField()


class Tipoplanta(models.Model):
    idtipoplanta = models.IntegerField(primary_key=True)
    nombrecomun = models.CharField(max_length=255)
    nombrecientifico = models.CharField(max_length=255)
    habilitado = models.BooleanField()
    idfoto = models.IntegerField(blank=True, null=True)


class Tipozona(models.Model):
    idtipozona = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255)
    habilitado = models.BooleanField()


class Usuario(models.Model):
    idusuario = models.IntegerField(primary_key=True)
    idrol = models.IntegerField()
    nombres = models.CharField(max_length=255)
    apellidopaterno = models.CharField(max_length=255)
    apellidomaterno = models.CharField(max_length=255)
    sexo = models.CharField(max_length=1)
    fechanacimiento = models.DateTimeField()
    nombreusuario = models.CharField(max_length=255)
    contrasena = models.CharField(max_length=255)
    correo = models.CharField(max_length=255)
    fechacreacion = models.DateTimeField()
    idusuarioauditado = models.IntegerField()
    habilitado = models.BooleanField()
    def getnombrecompleto(self):
        return self.nombres + ' ' + self.apellidopaterno


class Usuarioxinvernadero(models.Model):
    idinvernadero = models.IntegerField(primary_key=True)
    idusuario = models.IntegerField()


class Zona(models.Model):
    idzona = models.IntegerField(primary_key=True)
    idtipozona = models.IntegerField()
    idinvernadero = models.IntegerField()
    codigozonajson = models.IntegerField()
    nombre = models.CharField(max_length=255)
    area = models.FloatField(blank=True, null=True)
    temperaturaideal = models.FloatField(blank=True, null=True)
    temperaturamin = models.FloatField(blank=True, null=True)
    temperaturamax = models.FloatField(blank=True, null=True)
    phideal = models.FloatField(blank=True, null=True)
    phmin = models.FloatField(blank=True, null=True)
    phmax = models.FloatField(blank=True, null=True)
    concentracionco2ideal = models.FloatField(blank=True, null=True)
    concentracionco2min = models.FloatField(blank=True, null=True)
    concentracionco2max = models.FloatField(blank=True, null=True)
    fechacreacion = models.DateTimeField()
    habilitado = models.BooleanField()
    idusuarioauditado = models.IntegerField()
    condicionesshidas = models.NullBooleanField()


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
