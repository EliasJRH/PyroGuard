import os
import taipy as tp

# A dark mode is available in Taipy
# However, we will use the light mode for the Getting Started
gui = tp.Gui(page="# Getting started with *Taipy*").run(dark_mode=False)

tp.run(
    title="Taipy Demo",
    host='0.0.0.0',
    port=os.environ.get('PORT', '5000'),
)