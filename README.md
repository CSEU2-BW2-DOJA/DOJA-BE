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
