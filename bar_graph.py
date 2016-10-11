
# line graph of crime stats in geelong region

import pandas as pd
import seaborn as sb

# make a pandas df with crime-postcode information
pdf = pd.read_csv("./data/postcode_data.txt", sep="\t")

#pdf_OG = pdf[(pdf.Postcode > 3200) & (pdf.Postcode <  3300)]
#pdf_OG = pdf[pdf.Postcode == 3250]

pdf_OG = pdf

sb.pointplot(x="April_to_March", y="Rate_per_100000", hue="Offence_Division",
             data=pdf_OG, order=[2012, 2013, 2014, 2015, 2016])
             
sb.plt.show()

