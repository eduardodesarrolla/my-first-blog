import hashlib
from datetime import datetime
import requests
import json

apikey = "c4fb951e-620c-4359-a3a9-f1e79e1d7392"
hora_actual = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
firma = apikey+",0d1a7366-a9db-444e-84f0-41539993b16e,"+hora_actual
h = hashlib.sha256(firma.encode('utf-8'))
apikey2 = "a014de3f594f4f78b44088137cdef12fb1539577"
forma = "json"

response= requests.get("https://intcomex-prod.apigee.net/v1/getcatalog?", params = {"apiKey":apikey,"utcTimeStamp":hora_actual,"signature":h.hexdigest()})
dataJson=response.json
#print(response.content)
jsonToPython = json.loads(response.content)

response2= requests.get("http://api.cmfchile.cl/api-sbifv3/recursos_api/dolar?", params = {"apikey":apikey2,"formato":forma})
dataJson2=response2.json
#print(response.content)
jsonToPython2 = json.loads(response2.content)
valor_dolar=jsonToPython2['Dolares'][0]['Valor'].replace(",",".")

response3= requests.get("https://intcomex-prod.apigee.net/v1/downloadextendedcatalog?", params = {"apiKey":apikey,"utcTimeStamp":hora_actual,"signature":h.hexdigest()})
dataJson3=response3.json
#print(response.content)
jsonToPython3 = json.loads(response3.content)
    

