from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["dbiot"]

sensors = db["sensors"]

leitura = {
    'id':1, 
    'value': 23.2,
    'date': '2025-01-01',
    'time': '12:00:00'
}


result = sensors.insert_one(leitura)

if result.acknowledged:
    print(f"Inserido com sucesso")
else:
    print(f"Erro ao inserir")


result = sensors.find()

for r in result:
    print(r)

