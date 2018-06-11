CREATE EXTENSION IF NOT EXISTS plpythonu;

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


prep_q = plpy.prepare("SELECT * from app_modulosemilla WHERE idmodulo = $1", ["int"])
moduloVals= plpy.execute(prep_q, [idModulo])

mailFlag=False
msgBody= "\nValores fuera de rango detectados:\n\n"

if temperatura > moduloVals[0]["temperaturamax"] or temperatura < temperatura < moduloVals[0]["temperaturamin"]:
	mailFlag=True
	msgBody += "Temperatura: "+str(temperatura)+" °C\n"
if humedadTierra > moduloVals[0]["humedadtierramax"] or humedadTierra < moduloVals[0]["humedadtierramin"]:
	mailFlag=True
	msgBody += "Humedad de la tierra: "+ str(humedadTierra)+" %\n"
if humedadAmbiente > moduloVals[0]["humedadambientemax"] or humedadAmbiente < moduloVals[0]["humedadambientemin"]:
	mailFlag=True
	msgBody += "Humedad del ambiente: "+str(humedadAmbiente)+" %\n"
if concentracionCO2 > moduloVals[0]["concentracionco2max"] or concentracionCO2 < moduloVals[0]["concentracionco2min"]:
	mailFlag=True
	msgBody += "Concentración de CO2: "+str(concentracionCO2)+" %\n"
if nivelAgua > moduloVals[0]["nivelaguamax"] or nivelAgua < moduloVals[0]["nivelaguamin"]:
	mailFlag=True
	msgBody += "Nivel de agua: "+str(nivelAgua)+" %\n"

prep_q = plpy.prepare("SELECT u.correo, i.nombre as nombrei, ms.nombre as nombrem from app_usuario u INNER JOIN app_usuarioxinvernadero ui on u.idusuario = ui.idusuario INNER JOIN app_invernadero i on ui.idinvernadero = i.idinvernadero INNER JOIN app_zona z on i.idinvernadero = z.idinvernadero INNER JOIN app_modulosemilla ms on z.idzona = ms.idzona WHERE ms.idmodulo = $1", ["int"])
infoMails= plpy.execute(prep_q, [idModulo])

fromaddr = "alertas.invernaderos.pucp@gmail.com"

if mailFlag:
	for dest in infoMails:
		
		toaddr = dest["correo"]
		msg = MIMEMultipart()
		msg["From"] = fromaddr
		msg["To"] = toaddr
		msg["Subject"] = "[ALERTA] Monitoreo de condiciones en " + dest["nombrei"] + ", módulo: " + dest["nombrem"]
		 
		body = msgBody
		msg.attach(MIMEText(body, "plain"))
		 
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login(fromaddr, "invernadeiro2018")
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()
 
' 
LANGUAGE plpythonu;


CREATE  TRIGGER mail_modulo
AFTER INSERT ON app_historiamodulo
FOR EACH ROW
EXECUTE PROCEDURE mail_historia_modulo();