
# crime stats in geelong region

import pandas as pd
import folium
import json

# read json file of postcode boundaries in Victoria
with open("data/postcode_boundaries/POA_2011_VIC.json") as json_data:
    loaded = json.load(json_data)
    print "init_len", len(loaded["features"])
    count_if = 0
    count_else = 0
    for entry in loaded["features"]:
        print entry["properties"]["POA_NAME"]
        #break
        if entry["properties"]["POA_NAME"] == "3226":
            print entry
            count_if += 1
        else:
            loaded["features"].remove(entry)
            count_else += 1
    print "final_len", len(loaded["features"])
    print count_if, count_else
    for entry in loaded["features"]:
        print entry["properties"]["POA_NAME"]

# make a pandas df with crime-postcode information
pdf = pd.read_csv("./data/postcode_data.txt", sep="\t")

# subset to Geelong postcodes, which mostly start with 32
pdf_geel = pdf[(pdf.Postcode > 2999) & (pdf.Postcode <  4000)]

# subset by crime type
## TODO: problem here is that this causes a KeyError because not all postcodes have data for these specific crimes
#pdf_geel = pdf_geel[pdf_geel.Offence_Group == "F99_Other_miscellaneous_offences"]

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

# different tile options: "Cartodb Positron", "Stamen Toner", "Stamen Terrain", 
# "Mapbox Bright"

# create blank map with centre point and tile theme
c_map = folium.Map(location=[-38.1417, 144.4265], tiles="Cartodb Positron",
                   zoom_start=11)
                 
# now add choropleth overlay containing crime data                
c_map.choropleth(geo_path="data/postcode_boundaries/POA_2011_VIC.json",
                 data = pdf_geel_post,
                 columns = ["POA_CODE", "Rate_per_100000"],
                 key_on = "feature.properties.POA_CODE",
                 fill_color = "YlOrRd",
                 fill_opacity = 0.7,
                 line_opacity = 0.2)                   
                   
c_map.save("crime_map.html")