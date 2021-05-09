

"""

Estas son las librerías necesarias para que funcione el Bot

"""
from email_ini import *



import mimetypes
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders


from apiclient import errors, discovery


from datetime import date
import os
import base64




def create_message(sender, to, subject, message_text, files = None, cc = None):

	"""
		
	create_message es la función encargada de administrar todas las cabeceras necesarias en el cuerpo del correo para que puedan
	ser enviados mediante Gmail. Las variables que usa son las siguientes:

	-	sender (obligatoria): El correo del que se va a enviar el correo.
		o	Tipo variable= str
		o	Ejemplo= “micorreo@gmail.com”  

	-	to (obligatoria): Los correos a los que se va a enviar el mensaje. 
		o	Tipo variable= str
		o	Ejemplo1= “persona1@gmail.com”
		o	Ejemplo2= “persona1@gmail.com, persona2@empresa.com”

	-	subject (obligatoria): El asunto con el que se va a enviar el mensaje
		o	Tipo variable= str
		o	Ejemplo= “BOT-correo automático 2021-05-09”

	-	message_text (obligatoria): El cuerpo escrito del mensaje, se puede hacerse uso de HTML para formar la estructura del mensaje:
		o	Tipo variable= str
		o	Ejemplo1= ”Un cordial saludo,\nEste es el ejemplo de cómo enviar un correo automático por Gmail\n”
		o	Ejemplo2= “<head><title>Correo ejemplo</title></head><body><div>Un cordial saludo,<div>
					   <br><p>Este es el ejemplo de cómo enviar un correo automático por Gmail</p><br></body>”

	-	files (por defecto= None): La dirección (path) de los archivos que se quieren adjuntar.
		o	Tipo variable= list
		o	Ejemplo1= [“./mi_archivo_a_adjuntar.xlsx”]
		o	Ejemplo2= [“./mi_archivo_a_adjuntar.xlsx”, “C:/la/direccion/del/archivo/a_adjuntar.docx”]

	-	Cc (por defecto= None): Los correos a los que se va a enviar el mensaje como copia.
		o	Tipo variable= str
		o	Ejemplo1= “persona1@gmail.com”
		o	Ejemplo2= “persona1@gmail.com, persona2@empresa.com”


	"""

	message = MIMEMultipart()
	
	message['to'] = to
	message['from'] = sender
	message['subject'] = subject

	
	if cc != None:
		message['cc'] = cc

	message.attach(MIMEText(message_text, 'html'))

	
	if files != None:
		for file in files:
			content_type, encoding = mimetypes.guess_type(file)
			main_type, sub_type = content_type.split('/', 1)

			print(file, main_type, sub_type)
			file_name_ = os.path.basename(file)

			f = open(file, "rb")

			part = MIMEBase(main_type, sub_type)
			part.set_payload(f.read())
			part.add_header('Content-Disposition', 'attachment', filename=file_name_)
			encoders.encode_base64(part)
			f.close()

			message.attach(part)



	raw = base64.urlsafe_b64encode(message.as_bytes())
	raw = raw.decode()

	return {'raw': raw}




def send_message(service, user_id, message):

	"""

	send_message esta función se encarga de enviar el mensaje “message” usando la sesión iniciada desde email_ini, mediante el id de usuario “me”.	
	
	"""
	
	try:
		message = (results.messages().send(userId=user_id, body=message).execute())
		print('Message Id: %s' % message['id'])

		return message
	
	except errors.HttpError as error:
		print('An error occurred: %s' % error)






results = main()


# Remplaza 'micorreo@gmail.com' en "from_email" por tu correo electronico

from_email = 'micorreo@gmail.com'





# Remplaza 'persona1@gmail.com, persona2@empresa.com' en "to" por los correos a los que deseas enviar el correo.
# Recuerda mantener la estructura que se sugiere. Si deseas más información, chequea a partir de la línea 31 de este script
# como deben ser pasadas estas variables para poder hacer uso correcto del código

to = 'persona1@gmail.com, persona2@empresa.com'




# Remplaza el contenido de la variable "text" por el mensaje que quieres tenga el cuerpo del correo.
# Recuerda mantener la estructura que se sugiere. Si deseas más información, chequea a partir de la línea 31 de este script
# como deben ser pasadas estas variables para poder hacer uso correcto del código

text = f'''
	<head>
		<title>Correo ejemplo</title>
	</head>
	<body>
		<div>Un cordial saludo,<div>
		<br>
		<p>Este es el ejemplo de cómo enviar un correo automático por Gmail</p>
		<br>
	</body>
	'''



# Remplaza ["./mi_archivo_a_adjuntar.xlsx", "C:/la/direccion/del/archivo/a_adjuntar.docx"] en "file_attach" por el path de 
# los archivos que deseas adjuntar en el correo y des comenta la línea 175 de este script. No olvides agregar también la variable 
# A la función "create_message" en la línea 204 de este script.
# Recuerda mantener la estructura que se sugiere. Si deseas más información, chequea a partir de la línea 31 de este script
# como deben ser pasadas estas variables para poder hacer uso correcto del código

# file_attach = ["./mi_archivo_a_adjuntar.xlsx", "C:/la/direccion/del/archivo/a_adjuntar.docx"]





# Remplaza 'persona1@gmail.com' en "cc" por los correos a los que deseas enviar el correo como copia y des comenta la línea 186 de este 
# script. No olvides agregar también la variable a la función "create_message" en la línea 204 de este script.
# Recuerda mantener la estructura que se sugiere. Si deseas más información, chequea a partir de la línea 31 de este script
# como deben ser pasadas estas variables para poder hacer uso correcto del código

# cc = 'persona1@gmail.com'





print('\nDesde: ', from_email, 
	  '\nCorreo será enviando a: ', to)


current_date = date.today().strftime("%B %d, %Y")
subject_txt = f'BOT-correo automático {current_date}'


print('\n','#'*40)
print('\t\tCREANDO MENSAJE')
print('#'*40)

message = create_message(from_email, to, subject_txt, text)	    		
sent = send_message(results,'me', message)

print('\n','#'*40)
print('\t\tMENSAJE ENVIADO')
print('#'*40)