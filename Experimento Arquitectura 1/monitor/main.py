from datetime import datetime, timedelta
import json
from operator import and_
import schedule
import time
import database
from modelos import MonitorLog
import redis

redis_cli = redis.Redis(host="localhost", password="redispw", port=49153, decode_responses=True, encoding="utf-8", )
pubsub = redis_cli.pubsub()
tiempo_maximo_respuesta = 3

def run():
    while True:
        schedule.run_pending()
        respuesta_eco = pubsub.get_message(ignore_subscribe_messages=True)
        if respuesta_eco is not None:
            respuesta_mensaje = json.loads(respuesta_eco['data'])
            log = MonitorLog(respuesta=True, servicio_monitoreado=respuesta_mensaje['service'], time_log=None)
            log.id = respuesta_mensaje['id']
            database.session.merge(log)
            database.session.commit()
            
def job():
    mensaje_eco = MonitorLog(False, "SensorVigilant1", datetime.now())
    database.session.add(mensaje_eco)
    database.session.commit()
    redis_cli.publish('ping', mensaje_eco.id)
    
def verificar_fallas():
    time_menos = datetime.now() - timedelta(seconds=tiempo_maximo_respuesta)
    mensajes_log = database.session.query(MonitorLog).filter(MonitorLog.reportada == False)\
                                            .filter(MonitorLog.respuesta == False)\
                                            .filter(MonitorLog.time_log < time_menos).all()
    if mensajes_log is not None:        
        for registro in mensajes_log:
            with open('log_fallas_reportadas.txt','a+') as file:
                file.write('{} - Falla reportada id: {}\n'.format(datetime.now(), registro.id))
            registro.reportada = True
            database.session.add(registro)
            database.session.commit()

if __name__ == '__main__':
    database.Base.metadata.create_all(database.engine)
    pubsub.subscribe('eco')
    schedule.every().second.do(job)
    schedule.every(tiempo_maximo_respuesta).seconds.do(verificar_fallas)
    run()






