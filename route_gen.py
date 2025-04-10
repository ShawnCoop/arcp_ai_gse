import random
import sumolib

# Load your SUMO network (replace with your actual filename)
net = sumolib.net.readNet("seaTac.net.xml")

# Terminal gate edges (from your data)
terminal_edges = {
    "A": ["1104889261", "1104889258", "1166079478", "1166079481"],
    "B": ["1104927015", "1104927020", "1104927024", "1104927030"],
    "S": ["437909059#1", "437909064#1", "437909065#1", "1104911633#2"]
}

# Temporary baggage edge (replace with real one once identified)
baggage_edges = ["98374666#10"]

# Helper: pick a random edge from a zone
def pick_random(zone_list):
    return random.choice(zone_list)

# Helper: get shortest path route between two edges
def get_shortest_path(net, start_edge_id, end_edge_id):
    try:
        start = net.getEdge(start_edge_id)
        end = net.getEdge(end_edge_id)
        path = net.getShortestPath(start, end)
        return [edge.getID() for edge in path[0]] if path else []
    except Exception as e:
        print(f"Error generating path from {start_edge_id} to {end_edge_id}: {e}")
        return []

# Generate luggage tug vehicles going from baggage to random terminal gates
vehicles = []

for i in range(15):
    from_edge = pick_random(baggage_edges)
    terminal_choice = pick_random(list(terminal_edges.keys()))
    to_edge = pick_random(terminal_edges[terminal_choice])
    
    route = get_shortest_path(net, from_edge, to_edge)
    
    if route:
        vehicles.append({
            "id": f"luggage{i}",
            "type": "luggage_tug",
            "depart": i * 10,
            "route": route
        })
    else:
        print(f"⚠️ No valid route from {from_edge} to {to_edge}")

# Write routes to XML
def write_routes_to_xml(vehicles, filename="generated_routes.xml"):
    with open(filename, "w") as f:
        f.write('<routes>\n')
        f.write('  <vType id="luggage_tug" accel="1.0" decel="4.5" sigma="0.5" length="3.0" maxSpeed="10" vClass="truck"/>\n')
        
        for v in vehicles:
            route_id = f"route_{v['id']}"
            route_str = " ".join(v["route"])
            f.write(f'  <route id="{route_id}" edges="{route_str}"/>\n')
            f.write(f'  <vehicle id="{v["id"]}" type="{v["type"]}" depart="{v["depart"]}" route="{route_id}"/>\n')
        
        f.write('</routes>\n')
    print(f"✅ Wrote {len(vehicles)} vehicles to {filename}")

# Run the writer
write_routes_to_xml(vehicles)
