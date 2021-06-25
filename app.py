import json

from pymongo import MongoClient
from suds.client import Client
from suds.sudsobject import asdict
from datetime import date
from datetime import  datetime
try:
    conn = MongoClient('mongodb://localhost:27017/')
    print("Conexion exitosa!")
except:
    print("No fue posible conectar a MongoDB")

db = conn['totaldoc']
collection = db['type_currency']
url="https://www.banguat.gob.gt/variables/ws/TipoCambio.asmx?WSDL"
cliente = Client(url)
# print(cliente)

today = date.today()
now = datetime.now()
print(now)
# Obtener la fecha de hoy con el formato correcto del SOAP
d1 = today.strftime("%d/%m/%Y")
print(d1)

# tipoCambioFechaInicial = cliente.service.TipoCambioFechaInicial(d1)
# print(tipoCambioFechaInicial)

cambioDia = cliente.service.TipoCambioDia()
print(cambioDia)
# print(cambioDia['CambioDolar'][0][0])
result = cambioDia['CambioDolar'][0][0]
print(result)
dictResult = asdict(cambioDia)
print(dictResult)
cambioDiaString = cliente.service.TipoCambioDiaString()
# print(dict(result))

# collection.insert_one(dict(result))

def basic_sobject_to_dict(obj):
    """Converts suds object to dict very quickly.
    Does not serialize date time or normalize key case.
    :param obj: suds object
    :return: dict object
    """
    if not hasattr(obj, '__keylist__'):
        return obj
    data = {}
    fields = obj.__keylist__
    for field in fields:
        val = getattr(obj, field)
        if isinstance(val, list):
            data[field] = []
            for item in val:
                data[field].append(basic_sobject_to_dict(item))
        else:
            data[field] = basic_sobject_to_dict(val)
    return data


def sobject_to_dict(obj, key_to_lower=False, json_serialize=False):
    """
    Converts a suds object to a dict.
    :param json_serialize: If set, changes date and time types to iso string.
    :param key_to_lower: If set, changes index key name to lower case.
    :param obj: suds object
    :return: dict object
    """
    import datetime

    if not hasattr(obj, '__keylist__'):
        if json_serialize and isinstance(obj, (datetime.datetime, datetime.time, datetime.date)):
            return obj.isoformat()
        else:
            return obj
    data = {}
    fields = obj.__keylist__
    for field in fields:
        val = getattr(obj, field)
        if key_to_lower:
            field = field.lower()
        if isinstance(val, list):
            data[field] = []
            for item in val:
                data[field].append(sobject_to_dict(item, json_serialize=json_serialize))
        elif isinstance(val, (datetime.datetime, datetime.time, datetime.date)):
            data[field] = val.isoformat()
        else:
            data[field] = sobject_to_dict(val, json_serialize=json_serialize)
    return data


def sobject_to_json(obj, key_to_lower=False):
    """
    Converts a suds object to json.
    :param obj: suds object
    :param key_to_lower: If set, changes index key name to lower case.
    :return: json object
    """
    import json
    data = sobject_to_dict(obj, key_to_lower=key_to_lower, json_serialize=True)
    return json.dumps(data)

workPls = sobject_to_json(cambioDia)
print(workPls)

workPls2 = sobject_to_dict(cambioDia)
print(workPls2)

workPls3 = basic_sobject_to_dict(cambioDia)
print(workPls3)
# if now.hour == 13 and now.minute == 36:
#     collection.insert_one(dict(result))
print(workPls3['CambioDolar']['VarDolar'][0])