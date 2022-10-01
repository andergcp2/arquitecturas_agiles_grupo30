from datetime import datetime
import json
import time
import redis
from notify import MailNotificator

colaredis = redis.Redis(host="localhost", port=6379, decode_responses=True, encoding="utf-8", )
consumer = colaredis.pubsub()
consumer.subscribe('sec')
mail_notificador = MailNotificator()

while True:
    message = colaredis.get_message(ignore_subscribe_messages=True)
    time.sleep(1)
    if message is None:
        continue

    print(str(datetime.now()) +"topic-sec: ", message)
    message_decoded = json.loads(message)
    message_body = message_decoded['mensaje']
    receptores = message_decoded['receptores']

    for receptor in receptores:
        mail_notificador.send_mail(receptor, message)
