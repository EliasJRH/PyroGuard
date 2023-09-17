import requests
import csv
from io import StringIO
import folium

# API URL
apiUrl = "https://firms.modaps.eosdis.nasa.gov/api/country/csv/96d927ec7c72c84e5330ff37458dd5c7/VIIRS_NOAA20_NRT/USA/1"

def update_nasa_heat_map():

    print("Getting NASA info")

    # Fetch data from the NASA API
    response = requests.get(apiUrl)

    if response.status_code == 200:
        csv_data = response.text

        # Create a CSV reader
        csv_reader = csv.DictReader(StringIO(csv_data))

        # Create a map centered at a specific location
        m = folium.Map(location=[34.0522, -118.2437], zoom_start=5)

        # Extract latitude and longitude from each data entry and add circles
        for row in csv_reader:
            latitude = float(row['latitude'])
            longitude = float(row['longitude'])

            # Add a red transparent circle to the map
            folium.Circle(
                location=[latitude, longitude],
                radius=1000,  # Adjust the radius as needed
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.5,
            ).add_to(m)

        # Save the map as an HTML file
        m.save("heatmap_map.html")

        print("Map created with circles.")
    else:
        print(f"Failed to retrieve data from the NASA API. Status code: {response.status_code}")
