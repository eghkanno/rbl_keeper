# coding: utf-8

from time import sleep
from os import path, remove
import yaml
import requests as rq
from datetime import datetime

CONFIG_FILENAME = "config.yml"
config = yaml.load(open(CONFIG_FILENAME))

# polling settings
SLEEP_TIME = float(config["sleep_time"])
CALLCENTER_URL = "localhost:8080" #config["url"]
CALLCENTER_PASS = config["pass"]

# initialize
if path.exists("stop"): remove("stop")
t_ref = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

while not path.exists("stop"):
    headers={'pw': CALLCENTER_PASS}
    response = rq.get(CALLCENTER_URL, headers=headers)
    print(response)
    #latest_call = response.json()["latest_call"] if response.ok else t_ref
    sleep(SLEEP_TIME)

remove("stop")
print("RBL stopped.")