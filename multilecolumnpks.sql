ALTER TABLE app_usuarioxinvernadero DROP CONSTRAINT app_usuarioxinvernadero_pkey;
ALTER TABLE app_usuarioxinvernadero  ADD PRIMARY KEY (idinvernadero, idusuario);
ALTER TABLE app_permisoxrol DROP CONSTRAINT app_permisoxrol_pkey;
ALTER TABLE app_permisoxrol ADD PRIMARY KEY (idpermiso, idrol);