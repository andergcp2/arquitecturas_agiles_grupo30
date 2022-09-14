from datetime import datetime
import json
from random import randint
import time
import redis

print("sensor vigilant init ..")
#redis_cli = redis.Redis(host="localhost", password="redispw", port=49153, decode_responses=True, encoding="utf-8", )
redis_cli = redis.Redis(host="localhost", password="", port=6379, decode_responses=True, encoding="utf-8", )
pubsub = redis_cli.pubsub()
pubsub.subscribe('ping')
print("sensor vigilant init ok")

while True:
    ping = pubsub.get_message(ignore_subscribe_messages=True)
    #time.sleep(1)
    random_number = randint(1, 3)
    if ping is None:
        continue
    if random_number != 1:
        eco = {"id": ping['data'], "service" : "SV-1"}
        redis_cli.publish('eco', json.dumps(eco))
        #print(datetime.now(), eco)
        ping = None
    elif random_number == 1:        
        with open('fails_generated.log', 'a+') as file:
            file.write('{} - Falla generada id: {}\n'.format(datetime.now(), ping['data']))
