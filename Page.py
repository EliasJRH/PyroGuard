from taipy import Gui
import requests
import json
import base64
import numpy

data = requests.get('https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.2009473/messages').text

data_Dict = json.loads(data)["messages"]

x = []

for row in data_Dict:
    s = base64.b64decode(row['message']).decode('utf-8')
    temp = (s).split(',')
    if(len(temp)==6):
        x.append(temp)

Transmitters = {}

for item in x:
    if item[0] not in Transmitters:
        Transmitters[item[0]] = []
    
    Transmitters[item[0]].append(item)


Values = []

for key in Transmitters:
    t = Transmitters[key]
    t = numpy.transpose(t)

    v = {
        #"Name":t[0],
        "CO2":[t[1][0]],
        "TVOC":[t[2][0]],
        "Temperature":[t[3][0]],
        "Lattitude":[t[4][0]],
        "Longitude":[t[5][0]]
    }
    print(v)
    Values.append(v)

list_to_display = [100/i for i in range(1, 100)]


page = """
# *PyroGuard*

<|Transmitter A|expandable|
<|{list_to_display}|chart|>
<|{Values[0]}|table|>
|>

<|Transmitter B|expandable|
<|{list_to_display}|chart|>
<|{Values[1]}|table|>
|>
"""


Gui(page).run(use_reloader=True)