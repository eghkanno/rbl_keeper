# coding: utf-8

from time import sleep
from os import path, remove
import yaml
import requests as rq
from datetime import datetime
import RPi.GPIO as GPIO

CONFIG_FILENAME = "config.yml"
config = yaml.load(open(CONFIG_FILENAME))

# polling settings
SLEEP_TIME = float(config["sleep_time"])
CALLCENTER_URL = config["url"]
CALLCENTER_PORT = config["port"]

# gpio settings
ROTATION_TIME = config["rotation_time"]
GPIO_OUT = config["gpio_out"]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_OUT, GPIO.OUT)

def rblAlert(duration):
    GPIO.output(GPIO_OUT, True)
    sleep(duration)
    GPIO.output(GPIO_OUT, False)

# initialize
if path.exists("stop"): remove("stop")
t_ref = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

while not path.exists("stop"):
    responce = rq.get(CALLCENTER_URL + ":" + CALLCENTER_PORT)
    latest_call = responce.json()["latest_call"]
    if latest_call > t_ref:
        rblAlert(ROTATION_TIME)
        t_ref = latest_call
    sleep(SLEEP_TIME)

GPIO.output(GPIO_OUT, False)
GPIO.cleanup()
remove("stop")
print("RBL stopped.")