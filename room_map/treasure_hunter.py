import json
import requests
from decouple import config
from time import sleep
from random import randint
from util import Queue
from goto import goto, find_path


def goto_treasure(current_room_id, destination_room_id_or_title, can_fly=False, can_dash=False):
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

        # get the items in the current room
        items = data["items"]
        # determines if current room has treasure or not
        has_treasure = False

        # loop through every item in the room
        for item in items:
            # if it is a treasure
            if item == "tiny treasure":
                # set has_treasure to true
                has_treasure = True

        # if a treasure has been found
        if has_treasure:
            # take the treasure
            response = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/take/", json={
                "name": "treasure"}, headers={'Authorization': f"Token {TOKEN}"}).json()

            # get cooldown and sleep for the cooldown period
            cooldown = response["cooldown"]
            sleep(cooldown)

            print("\n******  Picked up a treasure  ******\n")

            # return True to signify that a treasure has been found
            return True


def get_current_room():
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
    TOKEN = config("TOKEN")

    # keep hunting until the user stops the script
    while True:
        # get the player's current room
        current_room = get_current_room()
        # set variable found_treasure to None
        found_treasure = None
        # while found_treasure is None
        while found_treasure is None:
            # generate a random interval between 2 and 500
            target_room = str(randint(2, 499))
            # call goto_treasure
            found_treasure = goto_treasure(current_room, target_room)
            # get current room
            current_room = get_current_room()

        # call goto and pass current location and 1
        goto(current_room, "1")
        # sell the treasure
        response = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/", json={
            "name": "treasure"}, headers={'Authorization': f"Token {TOKEN}"}).json()

        # get cooldown and sleep for the cooldown period
        cooldown = response["cooldown"]
        sleep(cooldown)

        # sell the treasure
        response = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/", json={
            "name": "treasure", "confirm": "yes"}, headers={'Authorization': f"Token {TOKEN}"}).json()

        # get cooldown and sleep for the cooldown period
        cooldown = response["cooldown"]
        sleep(cooldown)

        # confirm sale
        response = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/status/",
                                 headers={'Authorization': f"Token {TOKEN}"}).json()

        # get cooldown and sleep for the cooldown period
        cooldown = response["cooldown"]
        sleep(cooldown)

        print("\n******  Sold a coin  ******\n")
        print(response)
