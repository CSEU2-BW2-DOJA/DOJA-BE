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

### create_map.py

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
