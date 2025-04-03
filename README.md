# AI GSE Fleet Management Simulation

This project simulates airport GSE fleet traffic using SUMO and optimizes routing to reduce carbon emissions. 

- Download and install SUMO
- The .nod.xml and the .edg.xml files are used to create the .net.xml file containing edges and junctions
- Runn the following command to launch the gui for simulation
<<<<<<< HEAD
sumo-gui --net-file airport-net.net.xml --route-files routes.xml --delay 200

- Converting OSM file of airport to SUMO XML format
netconvert --osm-files map.osm -o seaTac.net.xml --geometry.remove --roundabouts.guess

- Edit the Map
netedit seaTac.net.xml

=======


sumo-gui --net-file airport-net.net.xml --route-files routes.xml --delay 20
>>>>>>> 5517bd0a3c018f826affc177a9a6f14578904b01
