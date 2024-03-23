from jinja2 import Environment, FileSystemLoader

# Set up Jinja environment
env = Environment(loader=FileSystemLoader(''))

# Load the template
template = env.get_template('main.html')

# Define data
data = {'content': 'woajguughsiuydhiu, 2213'}

# Render the template
rendered_html = template.render(data)

# Save the rendered HTML to a file
with open('main.html', 'w') as output_file:
    output_file.write(rendered_html)