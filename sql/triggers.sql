CREATE EXTENSION IF NOT EXISTS plpythonu;


-- modulo semilla

CREATE OR REPLACE FUNCTION mail_historia_modulo() RETURNS trigger AS '
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


temperatura = TD["new"]["temperatura"]
humedadTierra = TD["new"]["humedadtierra"]
humedadAmbiente = TD["new"]["humedadambiente"]
nivelAgua = TD["new"]["nivelagua"]
concentracionCO2 = TD["new"]["concentracionco2"]
idModulo = TD["new"]["idmodulo"]
fechaRegistro = TD["new"]["fecharegistro"]


prep_q = plpy.prepare("SELECT * from app_modulosemilla WHERE idmodulo = $1", ["int"])
vals= plpy.execute(prep_q, [idModulo])

mailFlag=False
msgBody= "\nValores fuera de rango detectados:\n\n"

if temperatura > vals[0]["temperaturamax"] or temperatura < temperatura < vals[0]["temperaturamin"]:
	mailFlag=True
	msgBody += "Temperatura: "+str(temperatura)+" °C\n"
if humedadTierra > vals[0]["humedadtierramax"] or humedadTierra < vals[0]["humedadtierramin"]:
	mailFlag=True
	msgBody += "Humedad de la tierra: "+ str(humedadTierra)+" %\n"
if humedadAmbiente > vals[0]["humedadambientemax"] or humedadAmbiente < vals[0]["humedadambientemin"]:
	mailFlag=True
	msgBody += "Humedad del ambiente: "+str(humedadAmbiente)+" %\n"
if concentracionCO2 > vals[0]["concentracionco2max"] or concentracionCO2 < vals[0]["concentracionco2min"]:
	mailFlag=True
	msgBody += "Concentración de CO2: "+str(concentracionCO2)+" %\n"
if nivelAgua > vals[0]["nivelaguamax"] or nivelAgua < vals[0]["nivelaguamin"]:
	mailFlag=True
	msgBody += "Nivel de agua: "+str(nivelAgua)+" %\n"

msgBody += "\nValores recuperados el "+str(fechaRegistro)+"\n"

prep_q = plpy.prepare("SELECT DISTINCT u.correo, i.nombre as nombrei, z.nombre as nombrez, ms.nombre as nombrem from app_usuario u INNER JOIN app_usuarioxinvernadero ui on u.idusuario = ui.idusuario INNER JOIN app_invernadero i on ui.idinvernadero = i.idinvernadero INNER JOIN app_zona z on i.idinvernadero = z.idinvernadero INNER JOIN app_modulosemilla ms on z.idzona = ms.idzona WHERE ms.idmodulo = $1", ["int"])
infoMails= plpy.execute(prep_q, [idModulo])

fromaddr = "alertas.invernaderos.pucp@gmail.com"

if mailFlag:
	for dest in infoMails:
		
		msg = MIMEMultipart()
		msg["From"] = fromaddr
		toaddr = dest["correo"]
		msg["To"] = toaddr
		msg["Subject"] = "[ALERTA] Monitoreo de condiciones en " + dest["nombrei"] + ", Zona: "+ dest["nombrez"]+", Módulo: " + dest["nombrem"]
		 
		body = msgBody
		msg.attach(MIMEText(body, "plain"))
		 
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login(fromaddr, "invernadeiro2018")
		text = msg.as_string()
		try:
			server.sendmail(fromaddr, toaddr, text)
		except Exception as e:
			print(e)
		server.quit()
 
' 
LANGUAGE plpythonu;


DROP TRIGGER IF EXISTS mail_modulo ON app_historiamodulo;

CREATE TRIGGER mail_modulo
AFTER INSERT ON app_historiamodulo
FOR EACH ROW
EXECUTE PROCEDURE mail_historia_modulo();


--zona

CREATE OR REPLACE FUNCTION mail_historia_zona() RETURNS trigger AS '
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


temperatura = TD["new"]["temperatura"]
ph = TD["new"]["ph"]
concentracionCO2 = TD["new"]["concentracionco2"]
idZona = TD["new"]["idzona"]
fechaRegistro = TD["new"]["fecharegistro"]

prep_q = plpy.prepare("SELECT * from app_zona WHERE idzona = $1", ["int"])
vals= plpy.execute(prep_q, [idZona])

mailFlag=False
msgBody= "\nValores fuera de rango detectados:\n\n"

if temperatura > vals[0]["temperaturamax"] or temperatura < temperatura < vals[0]["temperaturamin"]:
	mailFlag=True
	msgBody += "Temperatura: "+str(temperatura)+" °C\n"
if ph > vals[0]["phmax"] or ph < vals[0]["phmin"]:
	mailFlag=True
	msgBody += "pH: "+ str(ph)+"\n"
if concentracionCO2 > vals[0]["concentracionco2max"] or concentracionCO2 < vals[0]["concentracionco2min"]:
	mailFlag=True
	msgBody += "Concentración de CO2: "+str(concentracionCO2)+" %\n"

msgBody += "\nValores recuperados el: "+str(fechaRegistro)+"\n"

prep_q = plpy.prepare("SELECT DISTINCT u.correo, i.nombre as nombrei, z.nombre as nombrez from app_usuario u INNER JOIN app_usuarioxinvernadero ui on u.idusuario = ui.idusuario INNER JOIN app_invernadero i on ui.idinvernadero = i.idinvernadero INNER JOIN app_zona z on i.idinvernadero = z.idinvernadero WHERE z.idzona = $1", ["int"])
infoMails= plpy.execute(prep_q, [idZona])

fromaddr = "alertas.invernaderos.pucp@gmail.com"

if mailFlag:
	for dest in infoMails:
		msg = MIMEMultipart()
		msg["From"] = fromaddr
		toaddr = dest["correo"]
		msg["To"] = toaddr
		msg["Subject"] = "[ALERTA] Monitoreo de condiciones en " + dest["nombrei"] + ", Zona: " + dest["nombrez"]
		 
		body = msgBody
		msg.attach(MIMEText(body, "plain"))
		 
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login(fromaddr, "invernadeiro2018")
		text = msg.as_string()
		try:
			server.sendmail(fromaddr, toaddr, text)
		except Exception as e:
			print(e)
		server.quit()
 
' 
LANGUAGE plpythonu;

DROP TRIGGER IF EXISTS mail_zona ON app_historiazona;

CREATE  TRIGGER mail_zona
AFTER INSERT ON app_historiazona
FOR EACH ROW
EXECUTE PROCEDURE mail_historia_zona();


--plantas

CREATE OR REPLACE FUNCTION mail_historia_planta() RETURNS trigger AS '
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


humedad = TD["new"]["humedad"]
idZona = TD["new"]["idzona"]
idPlanta = TD["new"]["idplanta"]
fechaRegistro = TD["new"]["fecharegistro"]

prep_q = plpy.prepare("SELECT * from app_planta WHERE idplanta = $1", ["int"])
vals= plpy.execute(prep_q, [idPlanta])

mailFlag=False
msgBody= "\nValores fuera de rango detectados:\n\n"


if humedad > vals[0]["humedadmax"] or humedad < vals[0]["humedadmin"]:
	mailFlag=True
	msgBody += "Humedad: "+str(humedad)+" %\n"

msgBody += "\nValores recuperados el: "+str(fechaRegistro)+"\n"

prep_q = plpy.prepare("SELECT DISTINCT u.correo, i.nombre as nombrei, z.nombre as nombrez, tp.nombrecomun from app_usuario u INNER JOIN app_usuarioxinvernadero ui on u.idusuario = ui.idusuario INNER JOIN app_invernadero i on ui.idinvernadero = i.idinvernadero INNER JOIN app_zona z on i.idinvernadero = z.idinvernadero INNER JOIN app_planta p on z.idzona = p.idzona INNER JOIN app_tipoplanta tp on p.idtipoplanta = tp.idtipoplanta WHERE p.idplanta = $1" , ["int"]  )
infoMails= plpy.execute(prep_q, [idPlanta])

fromaddr = "alertas.invernaderos.pucp@gmail.com"

if mailFlag:
	for dest in infoMails:
		msg = MIMEMultipart()
		msg["From"] = fromaddr
		toaddr = dest["correo"]
		msg["To"] = toaddr
		msg["Subject"] = "[ALERTA] Monitoreo de condiciones en " + dest["nombrei"] + ", Zona: " + dest["nombrez"]+ ", Planta: "+ dest["nombrecomun"]
		 
		body = msgBody
		msg.attach(MIMEText(body, "plain"))
		 
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login(fromaddr, "invernadeiro2018")
		text = msg.as_string()
		try:
			server.sendmail(fromaddr, toaddr, text)
			break
		except Exception as e:
			print(e)
		server.quit()
 
' 
LANGUAGE plpythonu;

DROP TRIGGER IF EXISTS mail_planta ON app_historiaplanta;

CREATE  TRIGGER mail_planta
AFTER INSERT ON app_historiaplanta
FOR EACH ROW
EXECUTE PROCEDURE mail_historia_planta();