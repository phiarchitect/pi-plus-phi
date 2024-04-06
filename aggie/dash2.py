from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

svg = Element('svg', width='1000', height='600', version='1.1', xmlns='http://www.w3.org/2000/svg')

# Define the style for the dashboard elements
style = SubElement(svg, 'style')
style.text = """
    .blue-fill { fill: #00f; }
    .black-fill { fill: #000; }
    .blue-stroke { stroke: #00f; stroke-width: 2; }
    .dashed { stroke-dasharray: 5, 5; }
    .glitchy-text { font-family: 'Arial', sans-serif; fill: #0ff; font-size: 14px; }
"""

# Background
background = SubElement(svg, 'rect', x='0', y='0', width='1000', height='600', class_='black-fill')

# Network Diagram
network = SubElement(svg, 'g')
network_diagram = SubElement(network, 'circle', cx='250', cy='300', r='100', class_='blue-fill')
network_lines = SubElement(network, 'line', x1='250', y1='300', x2='500', y2='300', class_='blue-stroke dashed')
network_text = SubElement(network, 'text', x='210', y='295', class_='glitchy-text')
network_text.text = 'AGI Network'

# Engineering Metrics
metrics = SubElement(svg, 'g')
metrics_box = SubElement(metrics, 'rect', x='550', y='100', width='400', height='200', class_='blue-stroke')
metrics_lines = SubElement(metrics, 'line', x1='550', y1='250', x2='950', y2='250', class_='blue-stroke')
metrics_text = SubElement(metrics, 'text', x='560', y='145', class_='glitchy-text')
metrics_text.text = 'Metrics'

# Save to file
svg_data = prettify(svg)

# Writing to an SVG file
svg_filename = 'dash2.svg'
with open(svg_filename, 'w') as f:
    f.write(svg_data)

svg_filename

