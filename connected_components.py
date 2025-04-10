from sumolib import net
from collections import defaultdict, deque
import os

# === CONFIG ===
net_file = "seaTac.net.xml"  # Replace with your actual network file
output_dir = "connected_components"
poly_output_file = "components.poly.xml"
component_limit = 5  # Top N largest components to highlight

# === Load Network ===
print(f"📡 Loading network: {net_file}")
n = net.readNet(net_file)

# === Build Adjacency Graph ===
adjacency = defaultdict(list)
edges = n.getEdges()

for edge in edges:
    for succ in edge.getOutgoing():
        adjacency[edge.getID()].append(succ.getID())

# === Find Connected Components ===
def find_connected_components(edges):
    visited = set()
    components = []

    for edge in edges:
        edge_id = edge.getID()
        if edge_id in visited:
            continue

        component = []
        queue = deque([edge_id])
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            component.append(current)
            for neighbor in adjacency[current]:
                if neighbor not in visited:
                    queue.append(neighbor)

        components.append(component)
    return components

components = find_connected_components(edges)
components = sorted(components, key=len, reverse=True)

# === Write Edges to Files ===
os.makedirs(output_dir, exist_ok=True)
for i, comp in enumerate(components):
    with open(os.path.join(output_dir, f"component_{i+1}.txt"), "w") as f:
        for edge_id in comp:
            f.write(edge_id + "\n")

print(f"✅ Found {len(components)} components. Top {component_limit} saved to '{output_dir}'")

# === Write valid XML for edge highlighting in NETEDIT ===
colors = ["red", "green", "blue", "yellow", "cyan"]
with open(poly_output_file, "w", encoding="utf-8") as f:
    f.write("<additional>\n")
    for i, comp in enumerate(components[:component_limit]):
        color = colors[i % len(colors)]
        f.write(f'  <edges id="component_{i+1}" color="{color}" fill="1">\n')
        for edge_id in comp:
            f.write(f'    <edge id="{edge_id}"/>\n')
        f.write("  </edges>\n")
    f.write("</additional>\n")


print(f"🎨 Wrote {poly_output_file} for NETEDIT highlighting")
