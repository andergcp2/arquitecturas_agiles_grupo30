from flask import Flask
from flask_cors import CORS
from datetime import datetime
from random import randint
import json
import time
import redis

app = Flask(__name__)

colaredis = redis.Redis(host="localhost", password="redispw", port=49153, decode_responses=True, encoding="utf-8", )
consumer = colaredis.pubsub()
consumer.subscribe('sec')

while True:
    message = colaredis.get_message(ignore_subscribe_messages=True)
    #random_number = randint(1, 20)
    time.sleep(1)

    if message is None:
        continue
    #if random_number != 1:
    print(str(datetime.now()) +" topis-sec: ", message)
    message = None
 
   # send email