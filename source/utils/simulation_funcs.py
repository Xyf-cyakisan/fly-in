from ..model.Hub import Hub

def get_path_len(path: list):
    counter = 0
    for hub in path:
        try:
            hub.zone
        except AttributeError:
            counter += 1
        else:
            if hub.zone == "restricted":
                counter += 2
            else:
                counter += 1
    return counter


def check_restricted_connections(restricted_hub: Hub):
    counter = 0
    for connection in restricted_hub.connections:
        counter += len(connection.drones)
    return counter
