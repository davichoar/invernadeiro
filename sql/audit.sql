-- Auditoria Usuario

CREATE OR REPLACE FUNCTION audit_usuario() RETURNS trigger AS $audit_usuario$
    DECLARE
        accion varchar;
        nuevoid integer;
        dataantigua varchar;
        datanueva varchar;
    BEGIN
        IF TG_OP = 'INSERT' THEN
            accion := 'crear';
            dataantigua := '';
        ELSIF NEW.habilitado = OLD.habilitado THEN
            accion := 'editar';
            dataantigua := row_to_json(OLD);
        ELSE
            accion := 'eliminar';
            dataantigua := row_to_json(OLD);
        END IF;
        datanueva := row_to_json(NEW);
        SELECT MAX(idauditoria) into nuevoid FROM app_auditoria;
        IF nuevoid IS NULL THEN
            nuevoid := 0;
        END IF;
        nuevoid := nuevoid + 1;
        INSERT INTO app_auditoria(
            idauditoria, idusuario, tabla, accion, fecha, dataantigua, datanueva)
            VALUES (nuevoid, NEW.idusuarioauditado, 'Usuario', accion, now(), dataantigua, datanueva);
        RETURN NEW;
    END;
$audit_usuario$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS audit_usuario ON app_usuario;

CREATE TRIGGER audit_usuario AFTER INSERT OR UPDATE ON app_usuario
    FOR EACH ROW EXECUTE PROCEDURE audit_usuario();

-- Auditoria Invernadero

CREATE OR REPLACE FUNCTION audit_invernadero() RETURNS trigger AS $audit_invernadero$
    DECLARE
        accion varchar;
        nuevoid integer;
        dataantigua varchar;
        datanueva varchar;
    BEGIN
        IF TG_OP = 'INSERT' THEN
            accion := 'crear';
            dataantigua := '';
        ELSIF NEW.habilitado = OLD.habilitado THEN
            accion := 'editar';
            dataantigua := row_to_json(OLD);
        ELSE
            accion := 'eliminar';
            dataantigua := row_to_json(OLD);
        END IF;
        datanueva := row_to_json(NEW);
        SELECT MAX(idauditoria) into nuevoid FROM app_auditoria;
        IF nuevoid IS NULL THEN
            nuevoid := 0;
        END IF;
        nuevoid := nuevoid + 1;
        INSERT INTO app_auditoria(
            idauditoria, idusuario, tabla, accion, fecha, dataantigua, datanueva)
            VALUES (nuevoid, NEW.idusuarioauditado, 'Invernadero', accion, now(), dataantigua, datanueva);
        RETURN NEW;
    END;
$audit_invernadero$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS audit_invernadero ON app_invernadero;

CREATE TRIGGER audit_invernadero AFTER INSERT OR UPDATE ON app_invernadero
    FOR EACH ROW EXECUTE PROCEDURE audit_invernadero();

-- Auditoria Zona

CREATE OR REPLACE FUNCTION audit_zona() RETURNS trigger AS $audit_zona$
    DECLARE
        accion varchar;
        nuevoid integer;
        dataantigua varchar;
        datanueva varchar;
    BEGIN
        IF TG_OP = 'INSERT' THEN
            accion := 'crear';
            dataantigua := '';
        ELSIF NEW.habilitado = OLD.habilitado THEN
            accion := 'editar';
            dataantigua := row_to_json(OLD);
        ELSE
            accion := 'eliminar';
            dataantigua := row_to_json(OLD);
        END IF;
        datanueva := row_to_json(NEW);
        SELECT MAX(idauditoria) into nuevoid FROM app_auditoria;
        IF nuevoid IS NULL THEN
            nuevoid := 0;
        END IF;
        nuevoid := nuevoid + 1;
        INSERT INTO app_auditoria(
            idauditoria, idusuario, tabla, accion, fecha, dataantigua, datanueva)
            VALUES (nuevoid, NEW.idusuarioauditado, 'Zona', accion, now(), dataantigua, datanueva);
        RETURN NEW;
    END;
$audit_zona$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS audit_zona ON app_zona;

CREATE TRIGGER audit_zona AFTER INSERT OR UPDATE ON app_zona
    FOR EACH ROW EXECUTE PROCEDURE audit_zona();
    
-- Auditoria Panelluz

CREATE OR REPLACE FUNCTION audit_panelluz() RETURNS trigger AS $audit_panelluz$
    DECLARE
        accion varchar;
        nuevoid integer;
        dataantigua varchar;
        datanueva varchar;
    BEGIN
        IF TG_OP = 'INSERT' THEN
            accion := 'crear';
            dataantigua := '';
        ELSIF NEW.habilitado = OLD.habilitado THEN
            accion := 'editar';
            dataantigua := row_to_json(OLD);
        ELSE
            accion := 'eliminar';
            dataantigua := row_to_json(OLD);
        END IF;
        datanueva := row_to_json(NEW);
        SELECT MAX(idauditoria) into nuevoid FROM app_auditoria;
        IF nuevoid IS NULL THEN
            nuevoid := 0;
        END IF;
        nuevoid := nuevoid + 1;
        INSERT INTO app_auditoria(
            idauditoria, idusuario, tabla, accion, fecha, dataantigua, datanueva)
            VALUES (nuevoid, NEW.idusuarioauditado, 'Panelluz', accion, now(), dataantigua, datanueva);
        RETURN NEW;
    END;
$audit_panelluz$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS audit_panelluz ON app_panelluz;

CREATE TRIGGER audit_panelluz AFTER INSERT OR UPDATE ON app_panelluz
    FOR EACH ROW EXECUTE PROCEDURE audit_panelluz();
    
-- Auditoria Planta

CREATE OR REPLACE FUNCTION audit_planta() RETURNS trigger AS $audit_planta$
    DECLARE
        accion varchar;
        nuevoid integer;
        dataantigua varchar;
        datanueva varchar;
    BEGIN
        IF TG_OP = 'INSERT' THEN
            accion := 'crear';
            dataantigua := '';
        ELSIF NEW.habilitado = OLD.habilitado THEN
            accion := 'editar';
            dataantigua := row_to_json(OLD);
        ELSE
            accion := 'eliminar';
            dataantigua := row_to_json(OLD);
        END IF;
        datanueva := row_to_json(NEW);
        SELECT MAX(idauditoria) into nuevoid FROM app_auditoria;
        IF nuevoid IS NULL THEN
            nuevoid := 0;
        END IF;
        nuevoid := nuevoid + 1;
        INSERT INTO app_auditoria(
            idauditoria, idusuario, tabla, accion, fecha, dataantigua, datanueva)
            VALUES (nuevoid, NEW.idusuarioauditado, 'Planta', accion, now(), dataantigua, datanueva);
        RETURN NEW;
    END;
$audit_planta$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS audit_planta ON app_planta;

CREATE TRIGGER audit_planta AFTER INSERT OR UPDATE ON app_planta
    FOR EACH ROW EXECUTE PROCEDURE audit_planta();
    
-- Auditoria Modulosemilla

CREATE OR REPLACE FUNCTION audit_modulosemilla() RETURNS trigger AS $audit_modulosemilla$
    DECLARE
        accion varchar;
        nuevoid integer;
        dataantigua varchar;
        datanueva varchar;
    BEGIN
        IF TG_OP = 'INSERT' THEN
            accion := 'crear';
            dataantigua := '';
        ELSIF NEW.habilitado = OLD.habilitado THEN
            accion := 'editar';
            dataantigua := row_to_json(OLD);
        ELSE
            accion := 'eliminar';
            dataantigua := row_to_json(OLD);
        END IF;
        datanueva := row_to_json(NEW);
        SELECT MAX(idauditoria) into nuevoid FROM app_auditoria;
        IF nuevoid IS NULL THEN
            nuevoid := 0;
        END IF;
        nuevoid := nuevoid + 1;
        INSERT INTO app_auditoria(
            idauditoria, idusuario, tabla, accion, fecha, dataantigua, datanueva)
            VALUES (nuevoid, NEW.idusuarioauditado, 'Modulosemilla', accion, now(), dataantigua, datanueva);
        RETURN NEW;
    END;
$audit_modulosemilla$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS audit_modulosemilla ON app_modulosemilla;

CREATE TRIGGER audit_modulosemilla AFTER INSERT OR UPDATE ON app_modulosemilla
    FOR EACH ROW EXECUTE PROCEDURE audit_modulosemilla();
    
-- Auditoria Semilla

CREATE OR REPLACE FUNCTION audit_semilla() RETURNS trigger AS $audit_semilla$
    DECLARE
        accion varchar;
        nuevoid integer;
        dataantigua varchar;
        datanueva varchar;
    BEGIN
        IF TG_OP = 'INSERT' THEN
            accion := 'crear';
            dataantigua := '';
        ELSIF NEW.habilitado = OLD.habilitado THEN
            accion := 'editar';
            dataantigua := row_to_json(OLD);
        ELSE
            accion := 'eliminar';
            dataantigua := row_to_json(OLD);
        END IF;
        datanueva := row_to_json(NEW);
        SELECT MAX(idauditoria) into nuevoid FROM app_auditoria;
        IF nuevoid IS NULL THEN
            nuevoid := 0;
        END IF;
        nuevoid := nuevoid + 1;
        INSERT INTO app_auditoria(
            idauditoria, idusuario, tabla, accion, fecha, dataantigua, datanueva)
            VALUES (nuevoid, NEW.idusuarioauditado, 'Semilla', accion, now(), dataantigua, datanueva);
        RETURN NEW;
    END;
$audit_semilla$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS audit_semilla ON app_semilla;

CREATE TRIGGER audit_semilla AFTER INSERT OR UPDATE ON app_semilla
    FOR EACH ROW EXECUTE PROCEDURE audit_semilla();
    
-- Auditoria Tipoplanta

CREATE OR REPLACE FUNCTION audit_tipoplanta() RETURNS trigger AS $audit_tipoplanta$
    DECLARE
        accion varchar;
        nuevoid integer;
        dataantigua varchar;
        datanueva varchar;
    BEGIN
        IF TG_OP = 'INSERT' THEN
            accion := 'crear';
            dataantigua := '';
        ELSIF NEW.habilitado = OLD.habilitado THEN
            accion := 'editar';
            dataantigua := row_to_json(OLD);
        ELSE
            accion := 'eliminar';
            dataantigua := row_to_json(OLD);
        END IF;
        datanueva := row_to_json(NEW);
        SELECT MAX(idauditoria) into nuevoid FROM app_auditoria;
        IF nuevoid IS NULL THEN
            nuevoid := 0;
        END IF;
        nuevoid := nuevoid + 1;
        INSERT INTO app_auditoria(
            idauditoria, idusuario, tabla, accion, fecha, dataantigua, datanueva)
            VALUES (nuevoid, NEW.idusuarioauditado, 'Tipoplanta', accion, now(), dataantigua, datanueva);
        RETURN NEW;
    END;
$audit_tipoplanta$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS audit_tipoplanta ON app_tipoplanta;

CREATE TRIGGER audit_tipoplanta AFTER INSERT OR UPDATE ON app_tipoplanta
    FOR EACH ROW EXECUTE PROCEDURE audit_tipoplanta();