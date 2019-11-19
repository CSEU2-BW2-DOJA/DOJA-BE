import json
import requests
from decouple import config
from time import sleep
from util import Queue

def directionToRoom(room_map, current_room_id, room_id):
    for d, r in room_map[current_room_id].items():
        if r == room_id:
            return d
    return None

def find_path(room_map, current_room_id, destination_room_id):
    visited = set()
    paths = {}
    q = Queue()
    q.enqueue(current_room_id)
    paths[current_room_id] = [current_room_id]
    while q.size() > 0:
        room = q.dequeue()
        visited.add(room)
        for searched_room_id in room_map[room].values():
            if searched_room_id in visited or searched_room_id == '?':
                continue
            newPath = paths[room][:]
            newPath.append(searched_room_id)
            paths[searched_room_id] = newPath
            if searched_room_id == destination_room_id:
                correct_path = paths[searched_room_id]
                directions = []
                for i in range(len(correct_path) - 1):
                    directions.append(directionToRoom(room_map, correct_path[i], correct_path[i + 1]))
                return directions
            q.enqueue(searched_room_id)
    return None

def goto(current_room_id, destination_room_id_or_title):
    TOKEN = config("TOKEN")
    room_details = []
    room_map = {}
    with open("room_details.py", "r") as f:
        room_details = json.loads(f.read())
    with open("room_graph.py", "r") as f:
        room_map = json.loads(f.read())
    destination_room_id = destination_room_id_or_title
    # if room id not in room_graph
    if destination_room_id not in room_map:
        # find room with specified name in room_details
        destination_room_id_or_title = destination_room_id_or_title.lower()
        for room_info in room_details:
            if room_info['title'].lower() == destination_room_id_or_title:
                destination_room_id = str(room_info['room_id'])
                break

    # Traverse the map to find the path
    path = find_path(room_map, current_room_id, destination_room_id)
    # If path not found, print "path to {destination_room_id} not found"
    if not path:
        print(f"path to {destination_room_id} not found")
        return
    # If path found, go through each room to the destination room
    for direction in path:
        data = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/move/", json={
                             "direction": direction}, headers={'Authorization': f"Token {TOKEN}"}).json()
        cooldown = data["cooldown"]
        sleep(cooldown)