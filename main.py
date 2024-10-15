# add arguments for device type
# separate function for parsing by device type
# refactor - put parsing function into separate file
# refactor - put make footprint into separate file
# refactor - put make symbol into separate filej

import sys
import argparse
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import re
from myFunctions import *
import os

# Take the name of the CSV file as the first command line argument
# Take the name of the output file as the second command line argument

# omega symbol
om = "\u03A9"
env = Environment(loader=FileSystemLoader('.'))
parser = argparse.ArgumentParser(description="Process some arguments.")

parser.add_argument("--input", help="This is the CSV from digikey")
parser.add_argument("--foot", help="This is the folder you want your footprints stored")
parser.add_argument("--sym", help="This is the file name of the symbols")

args = parser.parse_args()

dataFilePath = args.input
symbolOutputPath = args.sym
footPrintPath = args.foot

padSize = 1.4
preamble = '''(kicad_symbol_lib
\t(version 20231120)
\t(generator "kicad_symbol_editor")
\t(generator_version "8.0")\n'''
with open(args.sym, 'w') as file:
    file.write(preamble)


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
    # There are multiple part numbers, take the one with CT-ND at the end
        match = re.findall(r'\b\w+CT-ND\b', dkPart)
        if match:
            dkPart = match[0]
    mfrPart = df.loc[index, 'Mfr Part #']
    price = df.loc[index, 'Price']


#--------------Resistor specific---------------------
    resistance = df.loc[index, 'Resistance']
    # turn the ohms into 
    resistance = resistance.replace("Ohms", om)
    # resistance = resistance.replace(" ", "_")
    symbol = 'R_' + resistance 
    tolerance = df.loc[index, 'Tolerance']
    power = df.loc[index, 'Power (Watts)']
    # use the fraction syntax
    power = re.sub(r'[0-9]+\.[0-9]+W,\s*', '', power)
    
    dimensions = df.loc[index, 'Size / Dimension']
    match = re.search('([0-9]+\.[0-9]+)mm\sx\s([0-9]+\.[0-9]+)mm', dimensions)
    if match:
        diameter = round(float(match.group(1)),3)
        length = round(float(match.group(2)),3)
    else:
        print('dimensions are muffed in line: ', index+2, ' expected format: 0.071" Dia x 0.130" L (1.80mm x 3.30mm)')
        dimensions = 'FUBAR'
    # All needed info has been parsed
    pinPitch = grid_round_up(float(length))
    if dimensions != 'FUBAR':
        footprintData = {
            'padSize': float(padSize),
            'length': float(length),
            'diameter': diameter,
            'pinPitch': pinPitch,
            'powerRating': power,
            'refOffsetX': 2.5,
            'refOffsetY': -((float(diameter) / 2) + 1.0),
            'valueOffsetX': 0.5,
            'valueOffsetY': (float(diameter) / 2) + 0.5
        }
        output = render_template('TH_ResistorTemplate.kicad_mod', footprintData)
        footprintFilename = f"R_Axial_L{length}mm_D{diameter}mm_P{pinPitch}mm_Horizontal.kicad_mod"
        pathToFootprint = args.foot + footprintFilename
        pseudoPathToFootprint = 'DigikeyResistors:'+ f"R_Axial_L{length}mm_D{diameter}mm_P{pinPitch}mm_Horizontal"
        for existingFilename in os.listdir(args.foot):
            if existingFilename == footprintFilename:
                print("The footprint exist")
                break       
        else:
            with open(pathToFootprint, 'w') as file:
                file.write(output)
        

#------------footprints are made, make symbols---------------------------------
        symbolData = {
            'symbol': symbol,
            'value': resistance,
            'tolerance': tolerance,
            'power': power,
            'footprint': pseudoPathToFootprint,
            'datasheet': datasheetUrl,
            'dkPart': dkPart,
            'mfrPart': mfrPart,
            'price': price,
        }   

        output = render_template('ResistorSymbolTemplate.txt', symbolData)
        with open(args.sym, 'a') as file:
            file.write(output)
with open(args.sym, 'a') as file:
    file.write(')')        
        



    
