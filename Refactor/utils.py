import argparse
import math
from jinja2 import Environment, FileSystemLoader
import os

def argumentParser():
    cmdArg = argparse.ArgumentParser(description='process some arguments.')

    cmdArg.add_argument("--input", help="This is the CSV file from digikey")
    cmdArg.add_argument("--footFolder", default='.', help="This is the folder you want your footprints to go to")
    cmdArg.add_argument("--sym", help="This is the file name of the symbols library")
    cmdArg.add_argument("--component", help="This is the type of component be created")

    return cmdArg.parse_args()

def grid_round_up(a):
    """
    Round the value to the next tenth of an inch.
    
    Parameters:
    a (int or float): value to be rounded

    Returns:
    int or float: the rounded value.
    """
    return math.ceil(a/2.54)*2.54

env = Environment(loader=FileSystemLoader('.'))

def render_template(pathToTemplate, data):
    """
    Fills in the template and render with Jinja2
    
    Parameters:
    pathToTemplate (string): path and file name of the template
    data (dictionary): The data the to use to fill in the template

    Returns:
    string: Filled in template
    """
    template = env.get_template(pathToTemplate)
    return template.render(data)

def checkForFootprint(fileName, pathToFootprint):
    """
    Checks if footprint already exist.
    
    Parameters:
    fileName (string): file name of the footprint
    pathToFootprint (string): path to the footprint 
    
    Returns:
    boolean: True if footprint exist, False if it doesn't
    """
    for existingFilename in os.listdir(pathToFootprint):
        if existingFilename == fileName:
            print("The footprint exist")
            return True
    return False

def saveFile(content, path, mode):
    """
    Saves file.
    
    Parameters:
    content (string): content to be written to file
    path (string): path to the save location including file name
    mode (string): writing type, IE w, r, a, etc

    Returns:
    Boolean: True if sucessfull, False if unsecessfull 
    """
    try:
            with open(path, mode) as file:
                file.write(content)
                return True
    except IOError as e:
        print(f"Could not open {path} for writing as '{mode}'.")
        return False
