
# crime stats in geelong region

import pandas as pd
import folium
import json

# make a pandas df with crime-postcode information
pdf = pd.read_csv("./data/postcode_data.txt", sep="\t")

# subset to VIC postcodes
pdf_geel = pdf[(pdf.Postcode > 3000) & (pdf.Postcode <  4000)]

# look at a particular year
pdf_geel = pdf_geel[pdf_geel.April_to_March == 2015]
#print set(pdf_geel.Offence_Division)

# subset by crime type
pdf_geel = pdf_geel[pdf_geel.Offence_Division == "A_Crimes_against_the_person"]

# now get average crime rate for each postcode
# group by different variables to change crime type
pdf_geel_post = pdf_geel["Rate_per_100000"].groupby(pdf_geel["Postcode"]).median().astype(float)

# this creates series, want to reset index to get back to df
pdf_geel_post = pdf_geel_post.reset_index()

# re-label columns. POA_CODE needs to match with the Vic postcodes
pdf_geel_post.columns = ["POA_CODE", "Rate_per_100000"]

# took ages to figure out that this was called in as an int, causing a type error
# need to make this a str so will match vic postcode data
pdf_geel_post["POA_CODE"] = pdf_geel_post.POA_CODE.astype(str)

# read json file of postcode boundaries in Victoria
# create a new dict that contains only areas of interest
# use postcodes from crime data to keep only relavent areas

with open("data/postcode_boundaries/POA_2011_VIC.json") as json_data:
    json_dict = {}
    json_dict["features"] = []
    loaded = json.load(json_data)
    for entry in loaded["features"]:
        # needed to add a split because some postcodes have names attached
        post_int = entry["properties"]["POA_NAME"].split()[0]
        if post_int in list(pdf_geel_post["POA_CODE"]):        
            json_dict["features"].append(entry)

# now write json_dict back into json file
with open('edited_VIC.json', 'w') as output:
    json.dump(json_dict, output)

# different tile options: "Cartodb Positron", "Stamen Toner", "Stamen Terrain", 
# "Mapbox Bright"

# create blank map with centre point and tile theme
c_map = folium.Map(location=[-38.1417, 144.4265], tiles="Cartodb Positron",
                   zoom_start=11)
                 
# now add choropleth overlay containing crime data                
c_map.choropleth(geo_path="edited_VIC.json",
                 data = pdf_geel_post,
                 columns = ["POA_CODE", "Rate_per_100000"],
                 key_on = "feature.properties.POA_CODE",
                 fill_color = "YlOrRd",
                 fill_opacity = 0.7,
                 line_opacity = 0.2)                   
                   
c_map.save("crime_map.html")