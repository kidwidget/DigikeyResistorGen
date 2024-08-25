import sys
import jinja2
import pandas as pd
import re
import requests

# Take the name of the CSV file as the first command line argument
# Take the name of the output file as the second command line argument

# omega symbol
om = "\u03A9"

if len(sys.argv) < 3:
    print("Did you forget to type the input and/or output file names?")
    sys.exit(1)

dataFilePath = sys.argv[1]
symbolOutputPath = sys.argv[2]

# Open the data file
df = pd.read_csv(dataFilePath, delimiter = ',', quotechar = '"')

# Parse the file and assign variables
for index, row in df.iterrows():
    datasheetUrl =  df.loc[index, 'Datasheet']
    if not re.match('http', datasheetUrl):
        datasheetUrl = "FUBAR"

    # check for multiple part numbers, take CT if available   
    dkPart = df.loc[index, 'DK Part #']
    if ',' in dkPart:
        # there are multiple part numbers, take cut tape
        if 'CT-ND' in dkPart:
            dkPart = re.search('.*CT-ND', dkPart).group(0)
    
    mfrPart = df.loc[index, 'Mfr Part #']
    price = df.loc[index, 'Price']

    resistance = df.loc[index, 'Resistance']
    # turn the ohms into 
    resistance = resistance.replace("Ohms", om)
    tolerance = df.loc[index, 'Tolerance']
    power = df.loc[index, 'Power (Watts)']
    # use the fraction syntax
    power = re.sub(r'[0-9]+\.[0-9]+W,\s*', '', power)
    
    dimensions = df.loc[index, 'Size / Dimension']
