*This project has been created as part of the 42 curriculum by cyakisan.*

## Description

Fly-in is a 42 Common Core Python project about simulating drones traveling from a starting point to an endpoint, turn by turn, through custom maps with specific rules and restrictions, while minimizing the total number of turns.

The program first reads a `.txt` file containing the map configuration, then runs the simulation and guides the drones through the map. Finally, it displays a graphical representation of the simulation in a dedicated window.

## In-depth Look at the Project

### Map Components

As mentioned previously, Fly-in is about moving drones from a starting point to an endpoint. However, this is a simplification of how maps are built. Here is a more detailed look at the different elements composing a map:

```text
Hub: defines a zone that drones can use as part of their route. Both the
     starting point and endpoint are hubs. All hubs are required to have
     a name and coordinates.

Connection: defines a bidirectional link between two hubs.

Drone: an active object traveling through the map as quickly as possible.
       Each drone has a unique ID.
```

These are the three main components of a map, but they can also have different types of metadata that specify their behavior during the simulation.

### Hub Metadata

```text
color: color of the hub in the graphical representation of the simulation

max_drones: maximum number of drones allowed in the hub

zone: the type of the hub. The available types are:

normal: regular hub, by default

priority: hub that should be prioritized during pathfinding when possible

restricted: it costs two turns to reach this hub; the drone spends one
            turn in the connection before reaching it

blocked: inaccessible hub that drones cannot enter
```

### Connection Metadata

```text
max_link_capacity: maximum number of drones allowed to traverse the
                   connection simultaneously
```

### Map File Example

```text
nb_drones: 4

start_hub: start 0 0 [color=green]

hub: bottleneck 1 0 [color=orange max_drones=2]

hub: wide_area 2 0 [color=blue max_drones=3]

end_hub: goal 3 0 [color=red]

connection: start-bottleneck [max_link_capacity=4]

connection: bottleneck-wide_area [max_link_capacity=4]

connection: wide_area-goal [max_link_capacity=4]
```

The general syntax is:

```text
<data_type>: <mandatory_data> [<metadata>]
```

### Project Architecture

```text
Controller                         (source/controller/Controller.py)
— creates all primary objects and controls their behavior
│
├── MapConfig                      (source/parser/MapConfig.py)
│   — reads and validates the map file
│
├── Simulation                     (source/model/Simulation.py)
│   — creates all simulation-related objects and controls their behavior
│   │
│   ├── Place                      (source/model/Place.py)
│   │   — duck-typing class used by both Hub and Connection, as both
│   │     represent places through which drones can travel
│   │
│   ├── Hub                        (source/model/Hub.py)
│   │   — represents a hub with a type, capacity, and coordinates
│   │
│   ├── Connection                  (source/model/connection.py)
│   │   — represents a link between hubs with a throughput limit
│   │
│   ├── Drone                       (source/model/Drone.py)
│   │   — represents a drone with an ID and a path, traveling through
│   │     hubs and connections until it reaches the end of the map
│   │
│   ├── MovementError               (source/utils/MovementError.py)
│   │   — custom exception raised when a drone attempts to move to
│   │     an unavailable place
│   │
│   └── Pathfinder                  (source/model/Pathfinder.py)
│       — weighted shortest-path finder using Dijkstra's algorithm
│
└── Renderer                        (source/renderer/Renderer.py)
    — renders both graphical and text output and creates the sprites
      used by the graphical interface
    │
    ├── Sprite                      (source/render/model/Sprite.py)
    │   — abstract class containing the attributes required to draw
    │     a shape
    │
    ├── ConnectionSprite             (source/render/model/ConnectionSprite.py)
    │   — graphical representation of a Connection
    │
    ├── DroneSprite                  (source/render/model/DroneSprite.py)
    │   — graphical representation of a Drone
    │
    └── HubSprite                    (source/render/model/HubSprite.py)
        — graphical representation of a Hub
```

## Calculating and Simulation

After creating all necessary objects, each drone is assigned a shortest path from the start hub to the end hub using Dijkstra's algorithm.

Dijkstra's algorithm is a suitable choice for this project because different hub types have different movement costs. In particular, entering a restricted hub costs two turns, while entering a normal or priority hub costs one turn. Using a weighted shortest-path algorithm makes it possible to take these movement costs into account when calculating routes.

During the simulation, drones move along their assigned paths while respecting the occupancy limits of hubs and the capacity limits of connections. When a movement cannot be performed, a `MovementError` is raised and handled by the simulation so that the program can continue without crashing.

This allows the simulation to respect the movement constraints while allowing drones to progress as soon as the required space becomes available.

## Output and Visual Representation

The `Renderer` is responsible for displaying the simulation and its results. Using the `pygame` module, the program opens a dedicated window displaying a visual representation of the map.

The different elements are represented as follows:

```text
drone:      blue square displaying its ID
hub:        circle whose color depends on the hub configuration
connection: gray line connecting two hubs
```

The graphical representation makes it easier to understand the state of the simulation at a glance. The position of each drone can be followed throughout the map, while the hubs and connections make the structure of the network immediately visible.

The simulation can also be controlled using several keyboard shortcuts (see the Instructions section), allowing the user to progress through the simulation turn by turn or restart it entirely.

### Terminal Output

The terminal also displays each drone's movement on every turn. For example:

```text
Turn 1: D1-waypoint1
Turn 2: D1-waypoint2 D2-waypoint1
Turn 3: D1-goal D2-waypoint2
Turn 4: D2-goal
```

The syntax used is:

```text
D<drone_id>-<place_the_drone_moved_to>
```

Only drones that move during a given turn are reported.

## Instructions

Running the project is simple. From a terminal located at the root of the repository, run:

```bash
make install
```

This installs the dependencies required to run the project.

Then run:

```bash
make run MAP='path/to/the/map'
```

This launches the program using the selected map. Several map files are already provided with the project.

### Controls

While the program is running:

```text
SPACE:  advance to the next turn
R:      restart the simulation completely
ESC:    close the program
```

### Other Commands

Clean the cache files generated during execution:

```bash
make clean
```

Clean the cache files and remove the virtual environment:

```bash
make fclean
```

Check the project using Flake8 and Mypy:

```bash
make lint
```

Run the same checks with Mypy's strict mode enabled:

```bash
make lint-strict
```

Run the program using Python's built-in debugger:

```bash
make debug
```

## Resources

The main external resource used during this project was AI assistance.

AI was used as a learning and research tool, mainly for:

* understanding how `pygame` works and how to implement the graphical representation;
* understanding Dijkstra's algorithm and its application to weighted graphs;
* clarifying Python concepts encountered during the implementation.

AI-generated information was used only after being reviewed and tested to ensure that it was understood and correctly integrated into the project.
