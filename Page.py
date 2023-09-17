from taipy import Gui
import requests
import json
import base64
import numpy

data = requests.get('https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.2006098/messages').text

data_Dict = json.loads(data)["messages"]

x = []

for row in data_Dict:
    s = base64.b64decode(row['message']).decode('utf-8')
    temp = (s).split(',')
    if(len(temp)==4):
        x.append(temp)

columns = "Name;val;val;val"

column_orders = [("X;Y;Z;W", "Squared"), ("Y;X", "Square root")]


page = """
# *PyroGuard*

<|{x}|table|columns={x[0]}|show_all|>

"""

Gui(page).run(use_reloader=True)