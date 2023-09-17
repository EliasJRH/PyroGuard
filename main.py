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

# update_nasa_heat_map()


#Request data from server
data = requests.get('https://testnet.mirrornode.hedera.com/api/v1/topics/0.0.2010263/messages').text
data_Dict = list(reversed(json.loads(data)["messages"]))

#parse data into arrays with message and time stamps
x=[]
for row in data_Dict:
    d =time.ctime(float(row["consensus_timestamp"]))
    s = base64.b64decode(row['message']).decode('utf-8')
    temp = (s).split(',')
    temp.append(d)
    x.append(temp)

#organize data by transmitter
Transmitters = {}
for item in x:
    if item[0] not in Transmitters:
        Transmitters[item[0]] = []
    Transmitters[item[0]].append(item)

#Format data into taipy readable chart data
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
        "Longitude":[t[5][0]],
        "Latest Time Stamp":[t[6][0]]
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
#
Heatmap
<p align="center">
    <img src="heatmap.png" />
</p>
"""

# Add a navbar to switch from one page to the other
root_md = """
<|navbar|>
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