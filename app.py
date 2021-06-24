from pymongo import MongoClient
from suds.client import Client
from datetime import date
from lxml import etree

try:
    conn = MongoClient('mongodb://localhost:27017/')
    print("Conexion exitosa!")
except:
    print("No fue posible conectar a MongoDB")

db = conn['totaldoc']
collection = db['type_currency']
url="https://www.banguat.gob.gt/variables/ws/TipoCambio.asmx?WSDL"
cliente = Client(url)
print(cliente)

today = date.today()
# Obtener la fecha de hoy con el formato correcto del SOAP
d1 = today.strftime("%d/%m/%Y")

tipoCambioFechaInicial = cliente.service.TipoCambioFechaInicial(d1)
print(tipoCambioFechaInicial)

#collection.insert_one(tipoCambioFechaInicial)

root = etree.parse(tipoCambioFechaInicial)
print(root)

#variablesDisponibles = cliente.service.VariablesDisponibles()
#print(variablesDisponibles)