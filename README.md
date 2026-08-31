*This project has been created as part of the 42 curriculum by cyakisan*

- Description:

Fly-in is a 42 Common Core Python project about simulating drones traveling from a starting point to an endpoint, turn by turn, through custom maps with specific rules and restrictions, while minimizing the total number of turns. The program first reads a .txt file containing the map configuration, then runs the simulation and guides the drones through the map. Finally, it displays a graphical representation of the simulation in a dedicated window.

- In-depth look at the project:

More detailed description:

As said previously, Fly-in is about drones going from a start to an end. However, it is definitely an oversimplification of how maps are built, here is a more in-depth look at the different elements composing a map:
```
Hub: defines a zone that drones can use as part of their route, both the start point and end point are hubs.

Connection: defines a bidirectional link between two zones.

Drones: active object going through the map as fast as possible.
```
These are the three main components of a map, but they can also have differents types of metadata precising their behavior in the simulation. Here's a look at all of the possibilites:

Hub metadata:

```
color: color of the drone in the graphical representation of the simulation

max_drones: maximum number of drones allowed in the hub

zone: the 'type' of the hub, here are what each do:

normal: regular hub, by default

priority: the hub must be prioritized in pathfinding if possible

restricted: it costs two turns to get to this hub, the drone will have to wait one turn in the connection

blocked: unaccessible hub
```
Connection metadata:
```
max_link_capacity: maximum number of drones allowed in the connection
```
Map file example:
```
nb_drones: 4

start_hub: start 0 0 [color=green]
hub: bottleneck 1 0 [color=orange max_drones=2]
hub: wide_area 2 0 [color=blue max_drones=3]
end_hub: goal 3 0 [color=red]

connection: start-bottleneck [max_link_capacity=4]
connection: bottleneck-wide_area [max_link_capacity=4]
connection: wide_area-goal [max_link_capacity=4]
```

Architecture of the project:

```
Controller                         (source/controller/Controller.py)            — creates all primary objects and dictates their behaviors
  ├── MapConfig                    (source/parser/MapConfig.py)                 — reads and validates the map file
  ├── Simulation                   (source/model/Simulation.py)                 — creates all simulation related objects and dictates their behaviors
  │       ├── Place                (source/model/Place.py)                      — duck typing class for Hub and Connection both being places that drones are going through
  │       ├── Hub                  (source/model/Hub.py)                        — hub with type, capacity, coordinates
  │       ├── Connection           (source/model/connection.py)                 — link between hubs with throughput limit
  │       ├── Drone                (source/model/Drone.py)                      — object with id, path, place, going through hubs and connection to see the end of the map
  │       ├── MovementError        (source/utils/MovementError.py)              — special error that is getting raised when a drone tries moving to non-available places
  │       └── Pathfinder           (source/model/Pathfinder.py)                 — weighted shortest path finder
  └── Renderer                     (source/renderer/Renderer.py)                — renders both graphical and text output, also creates Sprite inheriting classes for the graphical side
          ├── Sprite               (source/render/model/Sprite.py)             — abstract class possessing all of the needed attributs for shape drawing
          ├── ConnectionSprite     (source/render/model/ConnectionSprite.py)   — inherits from Sprite, graphical representation of the Connection class
          ├── DroneSprite          (source/render/model/DroneSprite.py)        — inherits from Sprite, graphical representation of the Drone class
          └── HubSprite            (source/render/model/HubSprite.py)          — inherits from Sprite, graphical representation of the Hub class
```

- Instructions:

Running the project is quite simple, in a terminal located at the root of this repository, use:

```bash
make install
```
(To install the dependencies needed for the project to run).

Then:

```bash
make run MAP='path of the map'
```
(To run the program with the chosen map, a few are already given by the subject and are found at the root of this repository).

Here are other commands if needed:

```bash
make clean
```
(Destroys all newly created cache files during runtime for a fresh start).

```bash
make fclean
```
(The same as clean except it also suppresses all the virtual environnement related files).

```bash
make lint
```
(Checks flake8 and mypy norm).

```bash
make lint-strict
```
(The same as lint except mypy runs with the --strict flag).

```bash
make debug
```
(Runs the program with the debugger tool pdb)

- Resources:

Only resource used for this project was AI which was only used for learning about pygame and the Dijkstra algorithm.
