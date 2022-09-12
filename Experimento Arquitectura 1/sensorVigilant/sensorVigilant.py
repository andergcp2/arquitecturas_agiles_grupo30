from datetime import datetime
import json
from random import randint
import time
import redis

redis_cli = redis.Redis(host="localhost", password="redispw", port=49153, decode_responses=True, encoding="utf-8", )

pubsub = redis_cli.pubsub()
pubsub.subscribe('ping')

while True:
    res = pubsub.get_message(ignore_subscribe_messages=True)
    time.sleep(1)
    random_number = randint(1, 20)
    if res is None:
        continue
    if random_number != 1:
        respuesta = {"id": res['data'], "service" : "sensorVigilant1"}
        redis_cli.publish('eco', json.dumps(respuesta))
        res = None
    elif random_number == 1:
        id_reportado = res['data']
        with open('log_fallas.txt','a+') as file:
            file.write('{} - Falla generada id: {}\n'.format(datetime.now(), id_reportado))
