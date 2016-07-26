
# crime stats in geelong region

import pandas as pd
import folium

# make a pandas df with crime-postcode information

pdf = pd.read_csv("./data/postcode_data.txt", sep="\t")

OG_2014 = pdf[(pdf.Postcode == 3226) & (pdf.April_to_March == 2014)]


# tiles: "Cartodb Positron", "Stamen Toner", "Stamen Terrain", 
# "Mapbox Bright"

c_map = folium.Map(location=[-38.1417, 144.4265], tiles="Cartodb Positron",
                   zoom_start=11)
                   
# use function to cut down json file to Geelong region postcodes
                   
def cut_json(fl, region):
    with open(fl) as f:
        for line in f:
            if line.startswith('{ "type"'):
                cols = line.strip().split('"')
                postcode = cols[9]
                print postcode
                break

cut_json("./data/postcode_boundaries/POA_2011_VIC.json", 4)


#c_map.choropleth(geo_path="./data/postcode_boundaries/POA_2011_VIC.json")                   
                   
c_map.save("crime_map.html")