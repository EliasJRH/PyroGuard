import os
import webbrowser
from taipy import Gui
from taipy.gui import Markdown
import requests
import json
import base64
import numpy
import time

from htmlGetter import update_nasa_heat_map
# from rocketry import Rocketry   
# from rocketry.conds import every

# app = Rocketry()

# @app.task(every("30 seconds"))
# def do_continuously():
#   print("It's been 30 seconds")

update_nasa_heat_map()

def navigate_to_map(state):
  webbrowser.open_new_tab("http://127.0.0.1:5000/heatmap_map.html")


data = requests.get('https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.2009473/messages').text

data_Dict = json.loads(data)["messages"]

x=[]


for row in data_Dict:
    d =time.ctime(float(row["consensus_timestamp"]))
    s = base64.b64decode(row['message']).decode('utf-8')
    temp = (s).split(',')
    if(len(temp)==6):
        temp.append(d)
        x.append(temp)


Transmitters = {}

for item in x:
    if item[0] not in Transmitters:
        Transmitters[item[0]] = []
    
    Transmitters[item[0]].append(item)


Values = []

ChartValues = []

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

    Values.append(v)

    v = {
        #"Name":t[0],
        "Time": t[6],
        "Temperature":t[3],
        #"Lattitude":t[4],
        #"Longitude":t[5]
    }

    ChartValues.append(v)


page2_md = """

<|Transmitter A|expandable|expanded=true|
<|{ChartValues[0]}|chart|mode=lines|x=Time|y=Temperature|color=red|>
# 
Current Values
<|{Values[0]}|table|show_all|>
|>
# 
<|Transmitter B|expandable|expanded=false|
<|{ChartValues[1]}|chart|mode=lines|x=Time|y=Temperature|color=red|>
# 
Current Values
<|{Values[1]}|table|show_all|>
|>
"""

# Add a navbar to switch from one page to the other
root_md = """
<|navbar|>
<|NASA Map|button|on_action=navigate_to_map|>
<|layout|columns=1fr auto 1fr|class_name=container align_columns_center|
<|part|>
<|part|class_name=align_item_stretch|
# *Pyro-Guard*
|>
<|part|>
|>
"""
about_md = Markdown("about.md")

pages = {
    "/": root_md,
    "Data": page2_md,
    "About": about_md,
}
Gui(pages=pages).run(use_reloader=True)