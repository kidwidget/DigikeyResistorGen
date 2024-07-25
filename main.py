""" import csv



# Open the CSV file and read its contents
with open('data.csv', newline='') as csvfile:
    # Create a DictReader object with the specified delimiter and quote character
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    
    # Convert reader to a list to access specific rows by index
    rows = list(reader)
    
    # Check if there are at least 4 rows (excluding the header)

    for row in rows:
        print (row['Description'])
   """
from jinja2 import Environment, FileSystemLoader

# Set up the Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))

# Load the template
template = env.get_template('template.txt')

# Define the values for the placeholders
context = {
    'place': 'magical forest',
    'character': 'wizard',
    'activity': 'cast spells'
}

# Render the template with the context
rendered_text = template.render(context)

# Print or save the rendered text
print(rendered_text)
