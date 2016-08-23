
# crime stats in geelong region

import pandas as pd
import folium

# make a pandas df with crime-postcode information
# also need to convert to json for later plotting

pdf = pd.read_csv("./data/postcode_data.txt", sep="\t")

pdf_geel = pdf[(pdf.Postcode > 3199) & (pdf.Postcode <  3295)]

pdf_geel_post = pdf_geel["Rate_per_100000"].groupby(pdf_geel["Postcode"]).mean().astype(float)

pdf_geel_post.to_json("post_rate.json")

pdf_geel_post = pdf_geel_post.reset_index()

pdf_geel_post.columns = ["POA_CODE", "Rate_per_100000"]

pdf_geel_post["POA_CODE"] = pdf_geel_post.POA_CODE.astype(str)


# tiles: "Cartodb Positron", "Stamen Toner", "Stamen Terrain", 
# "Mapbox Bright"

c_map = folium.Map(location=[-38.1417, 144.4265], tiles="Cartodb Positron",
                   zoom_start=11)
                   
c_map.choropleth(geo_path="edited_VIC.json",
                 #data_out = "post_rate.json",
                 data = pdf_geel_post,
                 columns = ["POA_CODE", "Rate_per_100000"],
                 key_on = "feature.properties.POA_CODE",
                 fill_color = "YlOrRd",
                 fill_opacity = 0.7,
                 line_opacity = 0.2)                   
                   
c_map.save("crime_map.html")