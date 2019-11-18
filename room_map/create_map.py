import json
from time import sleep
import requests
from decouple import config
from util import Queue

TOKEN = config("TOKEN")

# will hold the traversal path
traversalPath = []

# shows the room mapping
room_map = {}

# shows room details
room_details = []

with open("room_graph.py", "r") as f:
    # read the map from the room_graph world
    room_map = json.loads(f.read())

with open("room_details.py", "r") as f:
    # read the room details
    room_details = json.loads(f.read())

# get the player's current room
# the current room is the last room in the room details
current_room_id = room_details[-1]["room_id"]

# reverses the direction
reverse_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}


def get_unexplored_room(queue):
    """Finds the next unexplored room in the players current room
    and adds it to the queue.

    Arguments:
        player {class} -- instance of the Player class
        queue {class} -- instance of the Queue class
    """
    current_room_id = str(room_details[-1]["room_id"])

    # get direction available in the player's current room
    current_room = room_map[current_room_id]
    # will hold the unexplored_paths
    unexplored_paths = []

    # loop through current room
    for d in current_room:
        # check if room direction is unexplored
        if current_room[d] == '?':
            # add to unexplored paths
            unexplored_paths.append(d)

    # if there are unexplored rooms here
    if unexplored_paths:
        # add the first room to the queue
        queue.enqueue(unexplored_paths[0])
    # otherwise
    else:
        # call bft_find_other_room to find other unexplored rooms
        unexplored_path = bft_find_other_room()

        # if there are unexplored rooms
        if unexplored_path is not None:
            # loop through the unexplored paths
            for path in unexplored_path:
                # for exit in current curroom
                for exit in current_room:
                    # if path is in current room, enqueue it
                    if current_room[exit] == path:
                        queue.enqueue(exit)


def bft_find_other_room():
    """Uses bft to find the path to the closest room with an unexplored
    direction. When it finds one it returns the path. Returns None
    when an unexplored direction can not be found

    Arguments:
        player {class} -- instance of the Player class

    Returns:
        list -- path to the room with an unexplored direction
    """
    current_room_id = str(room_details[-1]["room_id"])

    # create new room queue
    q = Queue()
    # hold the visited room
    visited = set()
    # enqueue the current room as a list
    q.enqueue([current_room_id])

    # while the queue is not empty
    while q.size() > 0:
        # get the rooms
        rooms = q.dequeue()
        # grab the last room
        last_room = rooms[-1]

        # if the last room has not been visited
        if last_room not in visited:
            # add it to the visited set
            visited.add(last_room)

            # loop through the exits in the last room
            for exit in room_map[last_room]:
                # if unexplored, return the current room set
                if room_map[last_room][exit] == '?':
                    return rooms
                # otherwise,
                else:
                    # add the exit direction to the path
                    new_path = list(rooms)
                    new_path.append(room_map[last_room][exit])
                    # enqueue the new path
                    q.enqueue(new_path)

    # return None if no unexplored room is found
    return None


# create a queue
q = Queue()

# call get_unexplored_room with queue and player
get_unexplored_room(q)

# while there is still an unexplored room
while q.size() > 0:
    with open("room_graph.py", "r") as f:
        # read the map from the room_graph world
        room_map = json.loads(f.read())

    with open("room_details.py", "r") as f:
        # read the room details
        room_details = json.loads(f.read())

    # current player position
    current_player_room = str(room_details[-1]["room_id"])

    # the next direction
    next_direction = q.dequeue()

    # move the player in that direction
    response = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/move/", json={
                             "direction": next_direction}, headers={'Authorization': f"Token {TOKEN}"})

    # add it to the traversal path
    traversalPath.append(next_direction)

    # get the response
    data = response.json()

    # set the player's destination room
    # add it to the room_datails
    room_details.append(data)

    # new player position
    destination_room = str(room_details[-1]["room_id"])

    # update the map with the new discovery
    room_map[current_player_room][next_direction] = destination_room

    # if the current room has not been added to the map
    if destination_room not in room_map:
        exits = data["exits"]
        directions = {}

        for d in exits:
            directions[d] = "?"

        # add it and set to empty dictionary
        room_map[destination_room] = directions

    # get reverse direction to set it in the previous room
    r_direction = reverse_directions[next_direction]
    # point the destination room to the previous room
    room_map[destination_room][r_direction] = current_player_room

    # write the new changes to the file
    with open("room_graph.py", "w") as f:
        f.write(json.dumps(room_map))

    with open("room_details.py", "w") as f:
        f.write(json.dumps(room_details))

    # sleep the thread for the cooldown period
    cooldown = data["cooldown"]
    sleep(cooldown)

    # call get_unexplored_room to add the next direction to the queue
    get_unexplored_room(q)
