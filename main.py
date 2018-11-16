# coding: utf-8

from time import sleep
from os import path, remove
import yaml, json
import requests as rq
from datetime import datetime
import RPi.GPIO as GPIO

dir_path = path.dirname(path.abspath(__file__))+"/"
CONFIG_FILENAME = dir_path+"config.yml"
config = yaml.load(open(CONFIG_FILENAME))

# polling settings
SLEEP_TIME = float(config["sleep_time"])
CALLCENTER_URL = config["url"]
CALLCENTER_USER = config["user"]
CALLCENTER_PASS = config["pass"]

# gpio settings
ROTATION_TIME = float(config["rotation_time"])
GPIO_OUT = config["gpio_out"]

def rblAlert(duration):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_OUT, GPIO.OUT)
    GPIO.output(GPIO_OUT, True)
    sleep(duration)
    GPIO.output(GPIO_OUT, False)
    GPIO.cleanup()

# initialize
if path.exists(dir_path+"stop"): remove(dir_path+"stop")
auth = rq.auth.HTTPBasicAuth(CALLCENTER_USER, CALLCENTER_PASS)
if path.exists(dir_path+"t_ref"):
    file_t_ref = open(dir_path+"t_ref", mode="r")
    t_ref = file_t_ref.readline()
    file_t_ref.close()
else:
    res = rq.get(CALLCENTER_URL+"now/", auth=auth)
    t_ref = res.json()["datetime"]
    file_t_ref = open(dir_path+"t_ref", mode="w")
    file_t_ref.write(t_ref + "\n")
    file_t_ref.close()

while not path.exists(dir_path+"stop"):
    res = rq.get(CALLCENTER_URL, auth=auth)
    new_t = res.json()["datetime"] if res.ok else t_ref
    if new_t > t_ref:
        rblAlert(ROTATION_TIME)
        t_ref = new_t
        file_t_ref = open(dir_path+"t_ref", mode="w")
        file_t_ref.write(t_ref + "\n")
        file_t_ref.close()
    sleep(SLEEP_TIME)

remove(dir_path+"stop")
print("RBL stopped.")
