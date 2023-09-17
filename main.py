import os
import webbrowser
from taipy import Gui
from taipy.gui import Markdown
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

# Add a navbar to switch from one page to the other
root_md = """
<|navbar|>
<|NASA Map|button|on_action=navigate_to_map|>
<|layout|columns=1fr auto 1fr|class_name=container align_columns_center|
<|part|>
<|part|class_name=align_item_stretch|
# Pyro-Guard
|>
<|part|>
|>
"""
about_md = Markdown("about.md")
page2_md = "## This is page 2"

pages = {
    "/": root_md,
    "about": about_md,
    "Transmitter-A": page2_md,
    "Transmitter-B": page2_md,
}
Gui(pages=pages).run(use_reloader=True)