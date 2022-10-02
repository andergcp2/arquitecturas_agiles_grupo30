from datetime import datetime
import json
import time
import redis
from notifySms import SmsNotificator

colaredis = redis.Redis(host="localhost", port=6379, decode_responses=True, encoding="utf-8", )
consumer = colaredis.pubsub()
consumer.subscribe('code-sec')
sms_notificador = SmsNotificator()

while True:
    message = consumer.get_message(ignore_subscribe_messages=True)
    time.sleep(1)
    if message is None:
        continue

    print(str(datetime.now()) +"topic-sec: ", message)
    message_decoded = json.loads(message['data'])
    message_body = message_decoded['mensaje']
    receptores = message_decoded['receptores'].split(", ")

    for receptor in receptores:
        sms_notificador.send_sms("573156029459", message_body)
