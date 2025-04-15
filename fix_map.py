from lxml import etree

# Files
input_file = "seaTac_main_component.net.xml"
output_file = "seaTac_cleaned.net.xml"

# Load the XML
tree = etree.parse(input_file)
root = tree.getroot()

# Build a set of existing edge IDs
existing_edges = set(edge.get("id") for edge in root.findall("edge") if edge.get("id"))

# Remove <connection> elements with unknown from/to edges
for connection in root.findall("connection"):
    from_edge = connection.get("from")
    to_edge = connection.get("to")
    if from_edge not in existing_edges or to_edge not in existing_edges:
        root.remove(connection)

# Remove <roundabout> elements that reference missing edges
for roundabout in root.findall("roundabout"):
    edges = roundabout.get("edges", "").split()
    if any(edge_id not in existing_edges for edge_id in edges):
        root.remove(roundabout)

# Save cleaned network
tree.write(output_file, pretty_print=True, encoding="UTF-8", xml_declaration=True)

output_file
