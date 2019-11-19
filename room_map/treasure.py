import json
from time import sleep
import requests
from decouple import config

TOKEN = config("TOKEN")


def take_treasure(data):
    # Take treasure
    if len(data['items']) > 0:
        # sleep for the cooldown period before next request
        cooldown = data["cooldown"]
        sleep(cooldown)

        # take treasure
        take_response = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/take/", json={
            "name": "treasure"}, headers={'Authorization': f"Token {TOKEN}"})
        return take_response.json()


def sell_treasure(data):

    # Sell treasure
    if data['title'].lower() == 'shop':
        # sleep for the cooldown period before next request
        cooldown = data["cooldown"]
        sleep(cooldown)
        # sell treasure for riches and glory :)
        sell_response = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/", json={
            "name": "treasure"}, headers={'Authorization': f"Token {TOKEN}"})
        print(f"Sold Treasure: {sell_response.json()}")

        # sleep for the cooldown period before next request
        cooldown = data["cooldown"]
        sleep(cooldown)

        confirm_response = requests.post("https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/", json={
            "name": "treasure", "confirm": "yes"}, headers={'Authorization': f"Token {TOKEN}"})
        print(
            f"\n\n\n\n\nSale of Treasure Confirmed\n\n\n {confirm_response.json()}")
        return confirm_response.json()
