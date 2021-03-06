# coding: utf-8

from time import sleep
from os import path, remove, rename
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
if path.isfile(dir_path+"stop"): remove(dir_path+"stop")
auth = rq.auth.HTTPBasicAuth(CALLCENTER_USER, CALLCENTER_PASS)
if path.isfile(dir_path+"t_ref"):
    with open(dir_path+"t_ref", mode="r") as file_t_ref:
        t_ref = file_t_ref.readline()
else:
    try:
        res = rq.get(CALLCENTER_URL+"now/", auth=auth, timeout=10)
        t_ref = res.json()["datetime"]
    except:
        t_ref = "1970-01-01 00:00:01"
    with open(dir_path+"t_ref", mode="w") as file_t_ref:
        file_t_ref.write(t_ref + "\n")

# keep log files lines less than max_lines
def limitMaxLines(filepath, max_lines):
    if not path.isfile(filepath):
        return
    with open(filepath) as f:
        num_lines = sum(1 for line in f)
    if num_lines > max_lines: # removes first line
        with open(filepath) as f:
            for i in range(num_lines-max_lines):
                f.readline() # throw away first line
            with open(path.dirname(filepath) + "/temp", mode="w") as tmp:
                for l in f:
                    tmp.write(l) # copy every subsequent lines
        remove(filepath)
        rename(path.dirname(filepath) + "/temp", filepath)

while not path.isfile(dir_path+"stop"):
    try:
        res = rq.get(CALLCENTER_URL, auth=auth, timeout=10)
        new_t = res.json()["datetime"] if res.ok else t_ref
        if new_t > t_ref:
            rblAlert(ROTATION_TIME)
            t_ref = new_t
            with open(dir_path+"t_ref", mode="w") as file_t_ref:
                file_t_ref.write(t_ref + "\n")
    except Exception as ex:
        local_now = datetime.now()
        now_str = local_now.strftime("%Y/%m/%d %H:%M:%S")
        with open(dir_path+"err_log", mode="a") as file_err_log:
            file_err_log.write(now_str+ ", " + str(ex) + "\n")
        limitMaxLines(dir_path+"err_log", 15)
    sleep(SLEEP_TIME)

remove(dir_path+"stop")
print("RBL stopped.")
