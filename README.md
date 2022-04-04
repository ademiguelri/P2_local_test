# P2 project

This project makes server/client connection between n thermostats and a docker with timescaledb.

The connection is made via OPC UA protocol where the server part is sending all information of the thermostats and sending to the client that inserts that into a timescaledb docker.

Thermostats are simulated using a state machine, helped by python transitions package.

Once timescale is receiving data, these data is visualiced on Grafana.

Thermostat.py creates a instance of the object stateMachine. This instance creates a state machine and will simulate a working thermostat that will warm or cool based on the target temperature.


## Use guide

+ Start docker-compose
    * Browse http://localhost:3000/ for Grafana
    * Browse http://localhost:5050/ for PgAdmin4
    * Inspect Timescaledb docker to connect services to the gateway
+ Run lab.py
    * Select cuantity of thermostats
+ Run app.py
+ Use UaExpert to control target and power

## Usefull code

Visualize docker container IDs:

    docker ps

Ispect container info:

    docker inspect <dockerID>

Open postgres terminal inside the docker:

    docker exec -it <dockerID> psql -U postgres
