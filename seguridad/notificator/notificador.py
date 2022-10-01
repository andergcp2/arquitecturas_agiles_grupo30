from array import array
import json
from notify import MailNotificator

mail_notificador = MailNotificator()

message_dummy = {"status": "403", "mensaje": "security check suspicious time: 12-13-14 11:11:11", "receptores": ['cesar_s2005@hotmail.com', 'c.solanor@uniandes.edu.co']}
messagestring = json.dumps(message_dummy)
message_decoded = json.loads(messagestring)
message = message_decoded['mensaje']
receptores = message_decoded['receptores']

for receptor in receptores:
    mail_notificador.send_mail(receptor ,message)


