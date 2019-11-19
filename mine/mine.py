import requests
import time
import hashlib
from decouple import config

TOKEN = config("TOKEN")

auth = {"Authorization": "Token " + TOKEN}


def get_last_proof():
    res = requests.get(
        "https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/",
        headers=auth
    )
    return res.json()


def mine(new_proof):
    res = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/",
        headers=auth,
        json={"proof": new_proof}
    )
    print(res)
    return res.json()


def valid_proof(last_proof, proof, difficulty):
    checksum = '0' * difficulty
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:difficulty] == checksum


last_proof_obj = get_last_proof()
last_proof = last_proof_obj['proof']
diff = last_proof_obj['difficulty']
time.sleep(last_proof_obj['cooldown'])


def proof_of_work(start_point):
    print("Mining new block")

    start_time = time.time()
    proof = int(start_point)
    while valid_proof(last_proof, proof, diff) is False:
        proof += 1

    end_time = time.time()
    print(
        f'Block mined in {round(end_time-start_time, 2)}sec. Nonce: {str(proof)}')

    print("Mining with proof...")
    response = mine(proof)
    return response


if __name__ == "__main__":
    while True:
        res = proof_of_work(0)
        time.sleep(res["cooldown"])
