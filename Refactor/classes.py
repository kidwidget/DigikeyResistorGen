# classes used

import pandas as pd
import re
from settings import om, padSize
from utils import *

class Component:
    """Diodes, resistors, capacitors, maybe more"""
    
    def __init__(self):
        """Initiallize attributes"""
        self.mfrPart = None
        self.dkPart = None
        self.datasheet = None
        self.dimensions = None
        self.footprint = None
        self.price = None

    def parse(self, row):
        self.mfPart = row.get('Mfr Part')
        self.dkPart = row.get('DK Part #')
        self.datasheet = row.get('Datasheet')   
        self.dimensions = row.get('Size / Dimension')
        self.price = row.get('Price')
      
        # Check for not a URL
        if not re.match('http', self.datasheet):
            self.datasheet = 'FUBAR'



class Resistor(Component):
    """Resistor"""

    def __init__(self):
        super().__init__()
        self.symbol = None
        self.tolerance = None
        self.power = None
        self.diameter = None
        self.length = None
        self.pinPitch = None
        self.value = None

    def parse(self, row):
        # get the raw data
        super().parse(row)   
        self.value = row.get('Resistance')
        self.tolerance = row.get('Tolerance')
        self.power = row.get('Power (Watts)')
    
        # Make pretty
        if ',' in self.dkPart:
            match = re.findall(r'\b\w+CT-ND\b', self.dkPart)
            if match:
                self.dkPart = match[0]
        
        self.value = self.value.replace("Ohms", om)
        self.symbol = 'R_' + self.value
        self.power = re.sub(r'[0-9]+\.[0-9]+W,\s*', '', self.power)
        
        # check to see if dimension data is formated correctly
        match = re.searchmatch = re.search('([0-9]+\.[0-9]+)mm\sx\s([0-9]+\.[0-9]+)mm', self.dimensions)
        if match:
            self.diameter = round(float(match.group(1)), 3)
            self.length = round(float(match.group(2)),3)
            self.pinPitch = grid_round_up(self.length)
            
        else:
            print('Dimensions are muffled in line: ', str(row.name +2), '. Expected format: 0.071" Dia x 0.130" L (1.80mm x 3.30mm)')
            self.dimensions = 'FUBAR'
    
    def makeFootprint(self, path, args):
        if self.dimensions != 'FUBAR':
            # check to see if the footprint exist
            self.footprint = f"R_Axial_L{self.length}mm_D{self.diameter}mm_P{self.pinPitch}mm_Horizontal.kicad_mod"
            if (checkForFootprint(self.footprint, args.footFolder)):
                print("The footprint exist")
            else:
                # make foot print if it doesn't exist
                data = {
                    'padSize': float(padSize),
                    'length': float(self.length),
                    'diameter': self.diameter,
                    'pinPitch': self.pinPitch,
                    'powerRating': self.power,
                    'refOffsetX': 2.5,
                    'refOffsetY': -((float(self.diameter) / 2) + 1.0),
                    'valueOffsetX': 0.5,
                    'valueOffsetY': (float(self.diameter) / 2) + 0.5
                }
                output = render_template('TH_ResistorTemplate.kicad_mod', data)

                # write file
                path += path + self.footprint
                saveFile(output, path, 'w')
        else:
            print("Could not make footprint, dimensions are FUBAR")
    
    def makeSymbol(self, path):
        data = {
            'symbol': self.symbol,
            'value': self.value,
            'tolerance': self.tolerance,
            'footprint': self.footprint,
            'datasheet': self.datasheet,
            'dkPart': self.dkPart,
            'mfrPart': self.mfrPart,
            'price': self.price,
        }
        output = render_template('ResistorSymbolTemplate.txt', data)
        saveFile(output, path, 'a')
                      

class Capacitor(Component):
    """Capacitor"""
    def __init__(self, tolerance, voltage):
        self.tolerance = tolerance
        self.voltage = voltage

        