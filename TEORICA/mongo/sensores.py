import threading
import random
import time
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['bancoiot']
collection = db['sensores']


sensores = [
    {"nomeSensor": "Temp1", "unidadeMedida": "C°"},
    {"nomeSensor": "Temp2", "unidadeMedida": "C°"},
    {"nomeSensor": "Temp3", "unidadeMedida": "C°"}
]



def simular_sensor(nome_sensor):
    while True:
        doc = collection.find_one({"nomeSensor": nome_sensor})
        if doc["sensorAlarmado"]:
            print(f"Atenção! Temperatura muito alta! Verificar Sensor {nome_sensor}!")
            break
        temp = round(random.uniform(30, 40), 2)
        print(f"{nome_sensor} - Temperatura: {temp} C°")
        alarmado = temp > 38
        collection.update_one(
            {"nomeSensor": nome_sensor},
            {"$set": {
                "valorSensor": temp,
                "sensorAlarmado": alarmado
            }}
        )
        if alarmado:
            print(f"Atenção! Temperatura muito alta! Verificar Sensor {nome_sensor}!")
            break
        time.sleep(2) 

threads = []
for sensor in sensores:
    t = threading.Thread(target=simular_sensor, args=(sensor["nomeSensor"],))
    t.start()
    threads.append(t)

for t in threads:
    t.join()