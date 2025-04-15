from lxml import etree

component_file = "connected_components/component_1.txt"
original_net = "seaTac.net.xml"
output_net = "seaTac_main_component.net.xml"

# Load list of edge IDs to keep
with open(component_file, "r") as f:
    keep_edges = set(line.strip() for line in f if line.strip())

# Parse original .net.xml
tree = etree.parse(original_net)
root = tree.getroot()

# Filter out unwanted edges
for edge in root.findall("edge"):
    edge_id = edge.get("id")
    if edge_id and not edge_id.startswith(":") and edge_id not in keep_edges:
        root.remove(edge)

# Save to new network file
tree.write(output_net, pretty_print=True, encoding="UTF-8", xml_declaration=True)
print(f"✅ Wrote trimmed network to {output_net}")