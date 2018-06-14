INSERT INTO public.app_permiso(
	idpermiso, nombrepermiso, habilitado)
	VALUES (1,'permisoPrueba1', true);
	
INSERT INTO public.app_rol(
	idrol, nombrerol, habilitado)
	VALUES (-1, 'SuperAdmin', true);
	
INSERT INTO public.app_rol(
	idrol, nombrerol, habilitado)
	VALUES (1, 'Admin', true);
	
INSERT INTO public.app_rol(
	idrol, nombrerol, habilitado)
	VALUES (2, 'Jardinero', true);
	
INSERT INTO public.app_rol(
	idrol, nombrerol, habilitado)
	VALUES (3, 'General', true);
	
INSERT INTO public.app_usuario(
	idusuario, idrol, nombres, apellidopaterno, apellidomaterno, sexo, fechanacimiento, nombreusuario, contrasena, correo, fechacreacion, idusuarioauditado, habilitado)
	VALUES (1, 1, 'Chuck', 'Norris', 'S', 'M', '1990-10-19 00:00:00', 'cnorris', '123', 'chuckNorris@gmail.com', '2018-05-23 00:00:00', -1, true);
	
INSERT INTO public.app_invernadero(
	idinvernadero, idadmin, codigoinvernaderojson, nombre, fechacreacion, area, niveltanqueaguamin, niveltanqueaguamax, nivelenergiamin, nivelenergiamax, habilitado, idusuarioauditado)
	VALUES (1, 1, 1, 'Inv PUCP','2018-04-20 00:00:00',2000,10,15,10,15,true,1);

INSERT INTO public.app_invernadero(
	idinvernadero, idadmin, codigoinvernaderojson, nombre, fechacreacion, area, niveltanqueaguamin, niveltanqueaguamax, nivelenergiamin, nivelenergiamax, habilitado, idusuarioauditado)
	VALUES (2, 1, 2, 'Inv Santa Maria','2018-05-23 00:00:00',5000,20,25,20,25,true,1);
	
INSERT INTO public.app_usuarioxinvernadero(
	idinvernadero, idusuario)
	VALUES (1, 1);
	
INSERT INTO public.app_usuarioxinvernadero(
	idinvernadero, idusuario)
	VALUES (2, 1);
	
INSERT INTO public.app_usuario(
	idusuario, idrol, nombres, apellidopaterno, apellidomaterno, sexo, fechanacimiento, nombreusuario, contrasena, correo, fechacreacion, idusuarioauditado, habilitado)
	VALUES (-1, -1, 'SuperAdmin', 'Green', 'Home', 'M', '1950-01-01 00:00:00', 'superadmin', 'greenhome', 'greenhome@greenhome.com', '2018-05-23 00:00:00', -1, true);
	
INSERT INTO public.app_usuario(
	idusuario, idrol, nombres, apellidopaterno, apellidomaterno, sexo, fechanacimiento, nombreusuario, contrasena, correo, fechacreacion, idusuarioauditado, habilitado)
	VALUES (2, 1, 'Pedro Pablo', 'Rodriguez', 'S', 'M', '1992-09-19 00:00:00', 'prodriguez', '123', 'pedropabloRodriguez@gmail.com', '2018-05-23 00:00:00', 1, true);

INSERT INTO public.app_usuarioxinvernadero(
	idinvernadero, idusuario)
	VALUES (1,2);
	
INSERT INTO public.app_tipozona(
	idtipozona, nombre, habilitado)
	VALUES (1, 'Zona de Semillas', true);
	
INSERT INTO public.app_tipozona(
	idtipozona, nombre, habilitado)
	VALUES (2, 'Zona de Plantas', true);
	
INSERT INTO public.app_historiainvernadero(
	idhistoriainvernadero, idinvernadero, nivelenergia, niveltanqueagua, comentario, fecharegistro)
	VALUES (1, 1, 40.4, 30.2, 'here.. buzz lightyear','2018-05-23 00:00:00' );
	
INSERT INTO public.app_historiainvernadero(
	idhistoriainvernadero, idinvernadero, nivelenergia, niveltanqueagua, comentario, fecharegistro)
	VALUES (2, 1, 20.4, 23.2, 'here.. buzz lightyear 2','2018-04-23 00:00:00' );
	
INSERT INTO public.app_zona(
	idzona, idtipozona, idinvernadero, codigozonajson, nombre, area, temperaturaideal, temperaturamin, temperaturamax, fechacreacion, habilitado, phmin, phmax, idusuarioauditado, concentracionco2ideal, concentracionco2max, concentracionco2min)
	VALUES (1, 1, 1, 1, 'Zona 1', 34, 25, 20,30,'2018-05-28 00:00:00',true,5,8,1, 20, 30, 10);
	
	
INSERT INTO public.app_historiazona(
	idhistoriazona, idzona, temperatura, ph, concentracionco2, fecharegistro)
	VALUES (1, 1, 24, 22, 27,'2018-05-29 00:00:00');
	
INSERT INTO public.app_historiazona(
	idhistoriazona, idzona, temperatura, ph, concentracionco2, fecharegistro)
	VALUES (2, 1, 25, 23, 28,'2018-05-30 00:00:00');