import math
from jinja2 import Environment, FileSystemLoader

def grid_round_up(a):
    return math.ceil(a/2.54)*2.54

env = Environment(loader=FileSystemLoader('.'))

def render_template(templateName, data):
    template = env.get_template(templateName)
    return template.render(data)
