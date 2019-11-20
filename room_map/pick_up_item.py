import json
import requests
from decouple import config
from time import sleep
import argparse
from goto import goto, get_current_room

def pick_up_item(current_room_id, item_name, can_fly=False, can_dash=False):
    TOKEN = config("TOKEN")
    room_details = []
    room_map = {}
    with open("room_details_copy.py", "r") as f:
        room_details = json.loads(f.read())
    with open("room_graph_copy.py", "r") as f:
        room_map = json.loads(f.read())

    # Go to item
    goto(current_room_id, item_name, can_fly, can_dash)
    # Pick up item
    data = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/take/", json={
                         "name": item_name}, headers={'Authorization': f"Token {TOKEN}"}).json()
    
    print(data)
    cooldown = data["cooldown"]
    sleep(cooldown)
    # Remove item from room_details
    current_room_id = get_current_room()
    for room_info in room_details:
        if str(room_info['room_id']) == current_room_id:
            if 'items' in room_info and item_name in room_info['items']:
                room_info['items'].remove(item_name)
    with open("room_details_copy.py", "w") as f:
        f.write(json.dumps(room_details))

    if 'Item not found: +5s CD' in data['errors']:
        return False
    else:
        return True

if __name__ == "__main__":
    # instantiate the argument parser
    parser = argparse.ArgumentParser()

    # add the filename argument to the parser
    parser.add_argument("item_name", help="The item you want to pick up")

    # parse to get the argument
    args = parser.parse_args()

    # get the player's current room
    current_room = get_current_room()

    # get the item_name
    item_name = args.item_name

    # call goto with the arg and current room
    pick_up_item(current_room, item_name)