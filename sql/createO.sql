-- Rol

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
	
-- Permiso
    
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (1, 'Ver Invernadero', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (2, 'Crear Invernadero', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (3, 'Editar Invernadero', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (4, 'Eliminar Invernadero', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (5, 'Ver Usuario', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (6, 'Crear Usuario', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (7, 'Editar Usuario', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (8, 'Eliminar Usuario', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (9, 'Ver Zona', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (10, 'Crear Zona', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (11, 'Editar Zona', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (12, 'Eliminar Zona', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (13, 'Ver Panelluz', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (14, 'Crear Panelluz', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (15, 'Editar Panelluz', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (16, 'Eliminar Panelluz', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (17, 'Ver Modulosemilla', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (18, 'Crear Modulosemilla', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (19, 'Editar Modulosemilla', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (20, 'Eliminar Modulosemilla', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (21, 'Ver Semilla', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (22, 'Crear Semilla', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (23, 'Editar Semilla', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (24, 'Eliminar Semilla', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (25, 'Ver Planta', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (26, 'Crear Planta', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (27, 'Editar Planta', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (28, 'Eliminar Planta', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (29, 'Ver Tipoplanta', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (30, 'Crear Tipoplanta', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (31, 'Editar Tipoplanta', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (32, 'Eliminar Tipoplanta', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (33, 'Ver Estadistica', true);
INSERT INTO public.app_permiso (idpermiso, nombrepermiso, habilitado) VALUES (37, 'Ver Auditoria', true);
    
-- Permisoxrol

INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 1);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 2);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 3);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 4);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 5);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 6);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 7);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 8);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 9);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 10);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 11);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 12);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 13);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 14);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 15);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 16);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 17);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 18);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 19);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 20);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 21);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 22);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 23);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 24);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 25);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 26);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 27);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 28);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 29);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 30);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 31);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 32);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 33);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (-1, 37);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 1);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 2);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 3);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 4);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 5);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 6);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 7);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 8);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 9);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 10);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 11);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 12);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 13);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 14);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 15);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 16);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 17);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 18);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 19);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 20);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 21);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 22);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 23);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 24);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 25);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 26);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 27);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 28);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 29);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 30);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 31);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 32);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 33);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (1, 37);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (3, 1);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (3, 9);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (3, 13);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (3, 17);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (3, 21);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (3, 25);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (3, 29);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (3, 33);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 1);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 9);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 10);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 11);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 13);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 14);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 15);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 17);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 18);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 19);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 21);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 22);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 23);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 25);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 26);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 27);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 29);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 30);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 31);
INSERT INTO public.app_permisoxrol(idrol, idpermiso) VALUES (2, 33);
    
-- Usuario
    	
INSERT INTO public.app_usuario(
	idusuario, idrol, nombres, apellidopaterno, apellidomaterno, sexo, fechanacimiento, nombreusuario, contrasena, correo, fechacreacion, idusuarioauditado, habilitado)
	VALUES (-1, -1, 'SuperAdmin', 'Green', 'Home', 'M', '1950-01-01 00:00:00', 'superadmin', 'greenhome', 'greenhome@greenhome.com', '2018-05-23 00:00:00', -1, true); 
    
INSERT INTO public.app_usuario(
	idusuario, idrol, nombres, apellidopaterno, apellidomaterno, sexo, fechanacimiento, nombreusuario, contrasena, correo, fechacreacion, idusuarioauditado, habilitado)
	VALUES (1, 1, 'Arthuro', 'Cueva', 'Sánchez', 'M', '1996-03-13 00:00:00', 'acueva', '123', 'a20131271@pucp.pe', '2018-05-23 00:00:00', -1, true);
    
INSERT INTO public.app_usuario(
	idusuario, idrol, nombres, apellidopaterno, apellidomaterno, sexo, fechanacimiento, nombreusuario, contrasena, correo, fechacreacion, idusuarioauditado, habilitado)
	VALUES (2, 1, 'Pedro Pablo', 'Rodriguez', 'S', 'M', '1992-09-19 00:00:00', 'prodriguez', '123', 'pedropabloRodriguez@gmail.com', '2018-05-23 00:00:00', 1, true);

-- Invernadero
    
INSERT INTO public.app_invernadero(
	idinvernadero, idadmin, codigoinvernaderojson, nombre, fechacreacion, area, niveltanqueaguamin, niveltanqueaguamax, nivelenergiamin, nivelenergiamax, phaguamin, phaguamax, latitud, longitud, habilitado, idusuarioauditado)
	VALUES (1, 1, 1, 'Inv PUCP','2018-04-20 00:00:00',2000,10,15,10,15,5,8,-12.06944,-77.07944,true,1);

INSERT INTO public.app_invernadero(
	idinvernadero, idadmin, codigoinvernaderojson, nombre, fechacreacion, area, niveltanqueaguamin, niveltanqueaguamax, nivelenergiamin, nivelenergiamax, phaguamin, phaguamax, latitud, longitud, habilitado, idusuarioauditado)
	VALUES (2, 1, 500, 'Inv Santa Maria','2018-05-23 00:00:00',5000,20,25,20,25,4,8,-12.40719,-76.77277,true,1);

-- Usuarioxinvernadero
    
INSERT INTO public.app_usuarioxinvernadero(
	idinvernadero, idusuario)
	VALUES (1,1);
	
INSERT INTO public.app_usuarioxinvernadero(
	idinvernadero, idusuario)
	VALUES (2,1);   

INSERT INTO public.app_usuarioxinvernadero(
	idinvernadero, idusuario)
	VALUES (1,2); 

INSERT INTO public.app_usuarioxinvernadero(
	idinvernadero, idusuario)
	VALUES (2,2);
	
-- Tipozona
	
INSERT INTO public.app_tipozona(
	idtipozona, nombre, habilitado)
	VALUES (1, 'Zona de Semillas', true);
	
INSERT INTO public.app_tipozona(
	idtipozona, nombre, habilitado)
	VALUES (2, 'Zona de Plantas', true);

-- Zona	
	
INSERT INTO public.app_zona(
	idzona, idtipozona, idinvernadero, codigozonajson, nombre, area, temperaturaideal, temperaturamin, temperaturamax, fechacreacion, habilitado, phmin, phmax, idusuarioauditado, concentracionco2ideal, concentracionco2max, concentracionco2min)
	VALUES (1, 1, 2, 500, 'Zona de Semillas 1', 34, 25, 20,30,'2018-05-28 00:00:00',true,5,8,1, 20, 30, 10);
	
INSERT INTO public.app_zona(
	idzona, idtipozona, idinvernadero, codigozonajson, nombre, area, temperaturaideal, temperaturamin, temperaturamax, fechacreacion, habilitado, phmin, phmax, idusuarioauditado, concentracionco2ideal, concentracionco2max, concentracionco2min)
	VALUES (2, 2, 2, 501, 'Zona de Plantas 1', 34, 25, 20,30,'2018-05-29 00:00:00',true,5,8,1, 20, 30, 10);

-- Panelluz

INSERT INTO public.app_panelluz(
	idpanel, codigopaneljson, idzona, encendido, fechacreacion, habilitado, idusuarioauditado)
	VALUES (1, 500, 2, true, '2018-05-29 00:00:00', true, 1);
    
-- Modulosemilla
    
INSERT INTO public.app_modulosemilla(
	idmodulo, idzona, nombre, codigomodulojson, temperaturaideal, temperaturamin, temperaturamax, humedadtierraideal, humedadtierramin, humedadtierramax, humedadambienteideal, humedadambientemin, humedadambientemax, concentracionco2ideal, concentracionco2min, concentracionco2max, nivelaguaideal, nivelaguamin, nivelaguamax, filas, columnas, fechacreacion, habilitado, idusuarioauditado)
	VALUES (1, 1, 'Módulo 1', 500, 25, 20, 30, 15, 10, 20, 20, 15, 25, 10, 5, 15, 0.2, 0.1, 0.3, 9, 6, '2018-05-28 00:00:00', true, 1);

-- Tipoplanta

INSERT INTO public.app_tipoplanta(
	idtipoplanta, nombrecomun, nombrecientifico, habilitado, idfoto, idusuarioauditado)
	VALUES (1, 'Sacha Culantro', 'Eryngium foetidum', true, null, 1);

INSERT INTO public.app_tipoplanta(
	idtipoplanta, nombrecomun, nombrecientifico, habilitado, idfoto, idusuarioauditado)
	VALUES (2, 'Sacha Orégano', 'Lippia alba', true, null, 1);

INSERT INTO public.app_tipoplanta(
	idtipoplanta, nombrecomun, nombrecientifico, habilitado, idfoto, idusuarioauditado)
	VALUES (3, 'Sacha Inchi', 'Plukenetia volubilis', true, null, 1);

INSERT INTO public.app_tipoplanta(
	idtipoplanta, nombrecomun, nombrecientifico, habilitado, idfoto, idusuarioauditado)
	VALUES (4, 'Cocona', 'Solanum sessiliflorum', true, null, 1);

INSERT INTO public.app_tipoplanta(
	idtipoplanta, nombrecomun, nombrecientifico, habilitado, idfoto, idusuarioauditado)
	VALUES (5, 'Rocoto de la Selva', 'Capsicum pubescens', true, null, 1);

INSERT INTO public.app_tipoplanta(
	idtipoplanta, nombrecomun, nombrecientifico, habilitado, idfoto, idusuarioauditado)
	VALUES (6, 'Ají Macusarí', 'Capsicum annuum', true, null, 1);

INSERT INTO public.app_tipoplanta(
	idtipoplanta, nombrecomun, nombrecientifico, habilitado, idfoto, idusuarioauditado)
	VALUES (7, 'Ají Dulce', 'Capsicum chinense', true, null, 1);

INSERT INTO public.app_tipoplanta(
	idtipoplanta, nombrecomun, nombrecientifico, habilitado, idfoto, idusuarioauditado)
	VALUES (8, 'Achiote', 'Bixa orellana', true, null, 1);

-- Planta

INSERT INTO public.app_planta(
	idplanta, idtipoplanta, idzona, idsemilla, codigoplantajson, fechacreacion, humedadmin, humedadideal, humedadmax, idusuarioauditado, condicionesshidas, habilitado)
	VALUES (1, 1, 2, null, 500, '2018-05-28 00:00:00', 25, 30, 40, 1, null, true);

-- Lol

--INSERT INTO public.app_historiazona(
--    idhistoriazona, idzona, temperatura, ph, concentracionco2, fecharegistro)
--    VALUES (1, 1, 24, 22, 27,'2018-05-29 00:00:00');
	
--INSERT INTO public.app_historiazona(
--	  idhistoriazona, idzona, temperatura, ph, concentracionco2, fecharegistro)
--	  VALUES (2, 1, 25, 23, 28,'2018-05-30 00:00:00');


--INSERT INTO public.app_historiainvernadero(
--	  idhistoriainvernadero, idinvernadero, nivelenergia, niveltanqueagua, comentario, fecharegistro)
--	  VALUES (1, 1, 40.4, 30.2, '- Vacío -','2018-05-23 00:00:00' );
	
--INSERT INTO public.app_historiainvernadero(
--    idhistoriainvernadero, idinvernadero, nivelenergia, niveltanqueagua, comentario, fecharegistro)
--    VALUES (2, 1, 20.4, 23.2, '- Vacío -','2018-04-23 00:00:00' );