import requests
import time
from decouple import config
from goto import goto

TOKEN = config("TOKEN")
DESIRED_NAME = config("NAME")

auth = {"Authorization": "Token " + TOKEN}


def get_current_room():
    res = requests.get(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/",
        headers=auth
    )
    res_json = res.json()
    time.sleep(res_json["cooldown"])
    return res_json["room_id"]


def change_name():
    res = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/",
        headers=auth,
        json={"name": DESIRED_NAME, "confirm": "aye"}
    )
    return res.json()


if __name__ == "__main__":
    current_room = get_current_room()
    change_name_room = "467"
    goto(str(current_room), change_name_room)
    response = change_name()
    print(response)
