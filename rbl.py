# coding: utf-8

from time import sleep
from os import path,remove
import yaml
import requests as rq

CONFIG_FILENAME = "config.yml"
config = yaml.load(open(CONFIG_FILENAME))

# polling settings
SLEEP_TIME = float(config["sleep_time"])
CALLCENTER_URL = config["url"]
CALLCENTER_PORT = config["port"]

if path.exists("stop"): remove("stop")

while not path.exists("stop"):
    responce = rq.get(CALLCENTER_URL + ":" + CALLCENTER_PORT)
    latest_call = responce.json()["latest_call"]
    sleep(SLEEP_TIME)

remove("stop")
print("RBL stopped.")