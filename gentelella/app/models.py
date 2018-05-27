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
    nivelenergia = models.FloatField()
    niveltanqueagua = models.FloatField()
    comentario = models.CharField(max_length=255)
    fecharegistro = models.DateTimeField()



class Historiamodulo(models.Model):
    idhistoriamodulo = models.IntegerField(primary_key=True)
    idmodulo = models.IntegerField()
    temperatura = models.FloatField()
    humedadtierra = models.FloatField()
    humedadambiente = models.FloatField()
    nivelagua = models.FloatField()
    concentracionco2 = models.FloatField()
    luz = models.BooleanField()
    fecharegistro = models.DateTimeField()
    comentario = models.CharField(max_length=255)


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
    comentario = models.CharField(max_length=255)
    fecharegistro = models.DateTimeField()


class Historiasemilla(models.Model):
    idhistoriasemilla = models.IntegerField(primary_key=True)
    idsemilla = models.IntegerField()
    idmodulo = models.IntegerField()
    posx = models.IntegerField()
    posy = models.IntegerField()
    comentario = models.CharField(max_length=255)
    fecharegistro = models.DateTimeField()


class Historiazona(models.Model):
    idhistoriazona = models.IntegerField(primary_key=True)
    idzona = models.IntegerField()
    temperatura = models.FloatField()
    ph = models.FloatField()
    concentracionco2 = models.FloatField()
    fecharegistro = models.DateTimeField()

	
class Invernadero(models.Model):
    idinvernadero = models.IntegerField(primary_key=True)
    idadmin = models.IntegerField()
    codigoinvernaderojson = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255)
    fechacreacion = models.DateTimeField()
    area = models.FloatField()
    habilitado = models.BooleanField()
    idusuarioauditado = models.IntegerField(blank=True, null=True)


class Modulosemilla(models.Model):
    idmodulo = models.IntegerField(primary_key=True)
    codigomodulojson = models.IntegerField(unique=True)
    temperaturaideal = models.FloatField()
    temperaturamin = models.FloatField()
    temperaturamax = models.FloatField()
    humedadtierraideal = models.FloatField()
    humedadtierramin = models.FloatField()
    humedadtierramax = models.FloatField()
    humedadambienteideal = models.FloatField()
    humedadambientemin = models.FloatField()
    humedadambientemax = models.FloatField()
    concentracionco2ideal = models.FloatField()
    concentracionco2min = models.FloatField()
    concentracionco2max = models.FloatField()
    filas = models.IntegerField()
    columnas = models.IntegerField()
    habilitado = models.BooleanField()
    fechacreacion = models.DateTimeField()
    idusuarioauditado = models.IntegerField(blank=True, null=True)


class Panelluz(models.Model):
    idpanel = models.IntegerField(primary_key=True)
    codigopaneljson = models.IntegerField(unique=True)
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
    fechacreacion = models.DateTimeField()
    habilitado = models.BooleanField()
    idusuarioauditado = models.IntegerField(blank=True, null=True)
    humedadmin = models.FloatField()
    humedadideal = models.FloatField()
    humedadmax = models.FloatField()


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
    idusuarioauditado = models.IntegerField(blank=True, null=True)



class Tipoplanta(models.Model):
    idtipoplanta = models.IntegerField(primary_key=True)
    nombrecomun = models.CharField(max_length=255)
    nombrecientifico = models.CharField(max_length=255)
    habilitado = models.BooleanField()
    idfoto = models.IntegerField()


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
    idusuarioauditado = models.IntegerField(blank=True, null=True)
    def getnombrecompleto(self):
        return self.nombres + ' ' + self.apellidopaterno

class Usuarioxinvernadero(models.Model):
    idinvernadero = models.IntegerField(primary_key=True)
    idusuario = models.IntegerField()


class Zona(models.Model):
    idzona = models.IntegerField(primary_key=True)
    idtipozona = models.IntegerField()
    idinvernadero = models.IntegerField()
    codigozonajson = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=255)
    area = models.FloatField()
    temperaturaideal = models.FloatField()
    temperaturamin = models.FloatField()
    temperaturamax = models.FloatField()
    fechacreacion = models.DateTimeField()
    habilitado = models.BooleanField()
    idusuarioauditado = models.IntegerField(blank=True, null=True)
