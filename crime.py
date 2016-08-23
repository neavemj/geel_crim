
# crime stats in geelong region

import pandas as pd
import folium

# make a pandas df with crime-postcode information
pdf = pd.read_csv("./data/postcode_data.txt", sep="\t")

# subset to Geelong postcodes, which mostly start with 32
pdf_geel = pdf[(pdf.Postcode > 3199) & (pdf.Postcode <  3300)]

# now get average crime rate for each postcode
pdf_geel_post = pdf_geel["Rate_per_100000"].groupby(pdf_geel["Postcode"]).mean().astype(float)

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
c_map.choropleth(geo_path="edited_VIC.json",
                 data = pdf_geel_post,
                 columns = ["POA_CODE", "Rate_per_100000"],
                 key_on = "feature.properties.POA_CODE",
                 fill_color = "YlOrRd",
                 fill_opacity = 0.7,
                 line_opacity = 0.2)                   
                   
c_map.save("crime_map.html")