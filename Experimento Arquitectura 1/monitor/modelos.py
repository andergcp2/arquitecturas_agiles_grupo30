from email.policy import default
import database
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

class MonitorLog(database.Base):
    __tablename__ = 'eco'
    id = Column(Integer, primary_key=True)
    respuesta = Column(Boolean, default=False)
    servicio_monitoreado = Column(String, nullable=False)
    reportada = Column(Boolean, default=False)
    time_log = Column(DateTime)
    
    def __init__(self, respuesta, servicio_monitoreado ,time_log):
        self.respuesta = respuesta
        self.servicio_monitoreado = servicio_monitoreado
        if time_log is not None: 
            self.time_log = time_log
    
    def __repr__(self):
        return f'MonitorLog({self.id})'