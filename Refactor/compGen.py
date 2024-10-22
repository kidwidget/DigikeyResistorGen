# problem to fix:
# run some test cases to check for errors.
# This is the main program

import pandas as pd
import sys
from classes import Resistor
from settings import resPreamble
from utils import saveFile, argumentParser

args = argumentParser()

match args.component:
    case "resistor":
        df = pd.read_csv(args.input, delimiter= ',', quotechar= '"')
        resistor = Resistor()
        saveFile(resPreamble, args.sym, 'w')
        for index, row in df.iterrows():
            resistor.parse(row)
            resistor.makeFootprint(args.footFolder, args)
            resistor.makeSymbol(args.sym)
            # write the final )
            saveFile(')', args.sym, 'a')        

    case "capacitor":
        print('capacitor - not implemented yet')
        # capacitor.parser
        # capacitor.footprint
        # capacitor.symbol
        sys.exit(1)
    case "diode":
        print('diode - not implemented yet')
        # diode.parser
        # doide.footprint
        # diode.symbol
        sys.exit(1)
    case _:
        print("I'm sorry, Dave. I’m afraid I can’t do that. - HAL 9000\n"
              "This software can only do resistor, capacitors, and diodes.")
        sys.exit(1)

print('We are done')


