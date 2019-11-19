import json

# to hold the rooms
room_details = []

with open("room_details.py", "r") as f:
    # read room_details.py into room_details list
    room_details = json.loads(f.read())

print("Length before cleaning is: ", len(room_details))

# will hold room ids
room_set = set()
# will contain a single copy of each room
cleaned_rooms = []

# loop through every room in room_details
for room in room_details:
    # check if the room id is not in the set
    if room["room_id"] not in room_set:
        # add the room id to set to remove repetition
        room_set.add(room["room_id"])
        # add it to the cleaned_room list
        cleaned_rooms.append(room)

print("Length after cleaning is: ", len(cleaned_rooms))

# write the result to the cleaned room_details file
with open("traverse_results/room_details.py", "w") as f:
    f.write(json.dumps(cleaned_rooms))
