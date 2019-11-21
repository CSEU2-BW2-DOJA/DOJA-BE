# LAMBDA TREASURE HUNT

This repository contains a collection scripts to enable a player participate in the Lambda Treasure Hunt 💰. The scripts are all written in Python 🐍 and the Requests HTTP library is used to make HTTP requests to the treasure hunt and coin mining endpoints.

## Setup, Dependencies and Environment Variables

This project uses `Pipenv` to manage dependencies. To begin you need to create a virtual environment with:

```sh
pipenv shell
```

Then install dependencies with:

```sh
pipenv install
```

The scripts require that a `.env` file is added at the root of the directory. The `.env` file should have the following content:

```sh
TOKEN="[PLAYER'S TOKEN]"
NAME="[PLAYER'S NAME]"
```

## Scripts usage

### create_map.py 🌐

To make finding treasures and finding rooms to mine coin a little easier. The player is expected to have a comprehensive map of the game world and the details of the rooms available in the game. The `create_map.py` script does this. It reads from and writes to `room_details.py` and `room_graph.py`. To generate the world and get room details the content of the files should be as follows:

`room_details.py`

```py
[
    {
        "room_id": 0,
        "title": "A Dark Room",
        "description": "You cannot see anything.",
        "coordinates": "(60,60)",
        "exits": ["n", "s", "e", "w"],
        "cooldown": 1.0,
        "errors": [],
        "messages": []
    }
]
```

`room_graph.py`

```py
{0: {"n": "?", "s": "?", "e": "?", "w": "?"}}
```

To start the scripts, enter this command from the command line:

```sh
python create_map.py
```

This script will take a couple of hours to map out the entire game world so hang in there 😉.

### clean_room_details.py

This script reads from `room_details.py` and remove duplicate rooms. `room_details.py` itself contains rooms as they are visited by the `create_map.py` script so there are duplicates. To remove duplicates, run the script from the command line like this:

```sh
python clean_room_details.py
```

It writes the output of its operation to `traverse_results/room_details.py`.

### goto.py ✈️

With the rooms and map all mapped out. This handy script makes moving around the map quite easy. It reads the map from the files `room_graph_copy.py` which is just map of the world generated after the `create_map.py` script has run its course and `room_details_copy.py` which is the details generated by using the `clean_room_details.py` script.

This script takes a single command line argument which is the destination room. To use the script enter this command from the command line:

```sh
python goto.py <destination_room_id>
```

### treasure_hunter.py 💰

My favorite 🤗.

As the name implies, the script hunts for treasures and sells them when they are found. It is completely automated, so just start it from the command line and watch the output in the command. I guarantee, you will be rich and famous.

To start making money 💵, enter this from the command line:

```sh
python treasure_hunter.pu
```

### pick_up_item.py

There are so many awesome and mysterious artifacts lying around in the game. To pick up an item that catches your fancy, simply do:

```sh
python pick_up_item.py [name of item]
```

### change_name.py

After amassing up to 1000 gold, you have to take on your authentic name. Name change is a prerequisite to coin mining so you do not want to skip this step. First make sure you have added your name to the `.env` file.

Use the script like this:

```sh
python change_name.py
```
