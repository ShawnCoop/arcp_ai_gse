import random
import sumolib

# Load SUMO network
net = sumolib.net.readNet(".net.xml")

# Define zones
gates = ["edge_gate1", "edge_gate2", "edge_gate3"]
baggage = ["edge_baggage"]
fuel_depots = ["edge_fuel"]
pushback_parking = ["edge_pushback"]

# Function to pick a random edge from a zone
def pick_random(zone_list):
    return random.choice(zone_list)

# Function to get shortest path between two edges
def get_shortest_path(net, start_edge_id, end_edge_id):
    start = net.getEdge(start_edge_id)
    end = net.getEdge(end_edge_id)
    path = net.getShortestPath(start, end)
    return [edge.getID() for edge in path[0]] if path else []

# Generate vehicle routes
vehicles = []
for i in range(10):  # 10 luggage tugs as example
    from_edge = pick_random(baggage)
    to_edge = pick_random(gates)
    route = get_shortest_path(net, from_edge, to_edge)
    
    if route:
        vehicles.append({
            "id": f"luggage{i}",
            "type": "luggage_tug",
            "depart": i * 10,
            "route": route
        })

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
