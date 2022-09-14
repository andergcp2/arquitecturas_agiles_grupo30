from datetime import datetime, timedelta
import json
from operator import and_
import schedule
import time
import database
from modelos import MonitorLog
import redis

print("monitor init ..")
#redis_cli = redis.Redis(host="localhost", password="redispw", port=49153, decode_responses=True, encoding="utf-8", )
redis_cli = redis.Redis(host="localhost", password="", port=6379, decode_responses=True, encoding="utf-8", )
pubsub = redis_cli.pubsub()
pubsub.subscribe('eco')
print("monitor init ok")
eco_max_time = 2

def send_ping_job():
    ping = MonitorLog(False, "SensorVigilant1", datetime.now())
    database.session.add(ping)
    database.session.commit()
    redis_cli.publish('ping', ping.id)
    #print(datetime.now(), ping.id)

def run():
    while True:
        schedule.run_pending()
        resp = pubsub.get_message(ignore_subscribe_messages=True)
        if resp is not None:
            eco = json.loads(resp['data'])
            log = MonitorLog(respuesta=True, servicio_monitoreado=eco['service'], time_log=None)
            log.id = eco['id']
            database.session.merge(log)
            database.session.commit()

def check_fails_job():
    time_menos = datetime.now() - timedelta(seconds=eco_max_time)
    pings = database.session.query(MonitorLog).filter(MonitorLog.reportada == False)\
                                            .filter(MonitorLog.respuesta == False)\
                                            .filter(MonitorLog.time_log < time_menos).all()
    if pings is not None:        
        for ping in pings:
            with open('fails_reported.log', 'a+') as file:
                file.write('{} - Falla reportada id: {}\n'.format(datetime.now(), ping.id))
            ping.reportada = True
            database.session.add(ping)
            database.session.commit()

if __name__ == '__main__':
    database.Base.metadata.create_all(database.engine)
    schedule.every().second.do(send_ping_job)
    schedule.every(eco_max_time).seconds.do(check_fails_job)
    run()
