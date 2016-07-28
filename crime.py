
# crime stats in geelong region

import pandas as pd
import folium

# make a pandas df with crime-postcode information
# also need to convert to json for later plotting

pdf = pd.read_csv("./data/postcode_data.txt", sep="\t")
pdf_codes = pdf[["Postcode", "Rate_per_100000"]]
pdf_codes.columns = ["POA_CODE", "Rate_per_100000"]
pdf_codes = pdf_codes.set_index("POA_CODE")
print pdf_codes

pdf_codes.to_json("post_rate.json")
pdf_codes = pdf_codes.reset_index()

# tiles: "Cartodb Positron", "Stamen Toner", "Stamen Terrain", 
# "Mapbox Bright"

c_map = folium.Map(location=[-38.1417, 144.4265], tiles="Cartodb Positron",
                   zoom_start=11)
                   
# use function to cut down json file to Geelong region postcodes
                   
def cut_json(fl, out_fl, region):
    """
    function to cut downloaded postcodes into selected area.
    region can be the first few numbers of desired postcodes
    """
    with open(fl) as f:
        output = open(out_fl, "w")
        count = 0
        for line in f:
            if line.startswith('{ "type"'):
                cols = line.strip().split('"')
                postcode = cols[9]
                if postcode.startswith(region):
                    count += 1          
                    if count > 1:       # doing this so no comma attached to last entry
                        output.write(",\n")
                    output.write(line.rstrip(",\n"))
            else:
                output.write(line)                
                
cut_json("./data/postcode_boundaries/POA_2011_VIC.json", "edited_VIC.json", "32")

c_map.choropleth(geo_path="edited_VIC.json",
                 data_out = "post_rate.json",
                 data = pdf_codes,
                 columns = ["POA_CODE", "Rate_per_100000"],
                 key_on = "feature.properties.POA_CODE",
                 fill_color = "YlOrRd",
                 fill_opacity = 0.7,
                 line_opacity = 0.2)                   
                   
c_map.save("crime_map.html")






