import json
import requests
from decouple import config
from time import sleep
import argparse
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
                    directions.append(directionToRoom(
                        room_map, correct_path[i], correct_path[i + 1]))
                return directions
            q.enqueue(searched_room_id)
    return None


def goto(current_room_id, destination_room_id_or_title, can_fly=False, can_dash=False):
    TOKEN = config("TOKEN")
    room_details = []
    room_map = {}
    with open("room_details_copy.py", "r") as f:
        room_details = json.loads(f.read())
    with open("room_graph_copy.py", "r") as f:
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
    for i in range(len(path)):
        used_flight = False
        used_dash = False
        data = {}
        # fly if can fly and terrain is elevated
        if can_fly:
            for room_info in room_details:
                if str(room_info['room_id']) == current_room_id:
                    if room_info['terrain'].lower() == "elevated":
                        data = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/fly/", json={
                            "direction": path[i]}, headers={'Authorization': f"Token {TOKEN}"}).json()
                        used_flight = True
                        break
                    else:
                        break
        # dash if can dash and didn't use fly and there is more rooms to dash through than 1
        if can_dash and not used_flight:
            directions_to_dash_through = [path[i]]
            j = i + 1
            while j < len(path):
                if path[j] == directions_to_dash_through[j - 1]:
                    directions_to_dash_through.append(path[j])
                else:
                    break
            if len(directions_to_dash_through) > 1:
                # get ids out of to_dash_through
                ids_to_dash_through = []
                cur = current_room_id
                for direction in directions_to_dash_through:
                    next_room_id = room_map[cur][direction]
                    ids_to_dash_through.append(next_room_id)
                    cur = next_room_id
                ids_to_dash_through = ','.join(ids_to_dash_through)
                data = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/dash/", json={
                    "direction": path[i], "next_room_ids": ids_to_dash_through}, headers={'Authorization': f"Token {TOKEN}"}).json()
                i += len(directions_to_dash_through) - 1
                used_dash = True
        # just walk if didn't use flight or dash
        if not used_flight and not used_dash:
            next_room_id = room_map[current_room_id][path[i]]
            data = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/move/", json={
                "direction": path[i], "next_room_id": next_room_id}, headers={'Authorization': f"Token {TOKEN}"}).json()

        cooldown = data["cooldown"]
        print(data)
        sleep(cooldown)
        current_room_id = str(data['room_id'])


def get_current_room():
    TOKEN = config("TOKEN")
    # make request to the init endpoint
    response = requests.get("https://lambda-treasure-hunt.herokuapp.com/api/adv/init/",
                            headers={'Authorization': f"Token {TOKEN}"}).json()

    # get room id
    room_id = response["room_id"]
    # get cooldown and sleep for the cooldown period
    cooldown = response["cooldown"]
    sleep(cooldown)

    # return the room_id in string format
    return str(room_id)


if __name__ == "__main__":
    # instantiate the argument parser
    parser = argparse.ArgumentParser()

    # add the filename argument to the parser
    parser.add_argument("destination", help="The room you want to go to")

    # parse to get the argument
    args = parser.parse_args()

    # get the player's current room
    current_room = get_current_room()

    # get the destination room
    destination_room = args.destination

    # call goto with the arg and current room
    goto(current_room, destination_room)
