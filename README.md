# AI GSE Fleet Management Simulation

This project simulates airport GSE fleet traffic using SUMO and optimizes routing to reduce carbon emissions. 

- Download and install SUMO
- The .nod.xml and the .edg.xml files are used to create the .net.xml file containing edges and junctions
- Runn the following command to launch the gui for simulation
sumo-gui --net-file airport-net.net.xml --route-files routes.xml --delay 20