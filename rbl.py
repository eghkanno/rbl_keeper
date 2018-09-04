# coding: utf-8

from time import sleep
from os import path,remove
import yaml

CONFIG_FILENAME = "config.yml"
config = yaml.load(open(CONFIG_FILENAME))

SLEEP_TIME=10

if path.exists("stop"): remove("stop")

while not path.exists("stop"):
    sleep(SLEEP_TIME)

remove("stop")
print("RBL stopped.")