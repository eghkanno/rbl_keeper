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
if path.exists(dir_path+"stop"): remove(dir_path+"stop")
auth = rq.auth.HTTPBasicAuth(CALLCENTER_USER, CALLCENTER_PASS)
if path.exists(dir_path+"t_ref"):
    file_t_ref = open(dir_path+"t_ref", mode="r")
    t_ref = file_t_ref.readline()
    file_t_ref.close()
else:
    try:
        res = rq.get(CALLCENTER_URL+"now/", auth=auth, timeout=10)
        t_ref = res.json()["datetime"]
    except:
        t_ref = "1970-01-01 00:00:01"
    file_t_ref = open(dir_path+"t_ref", mode="w")
    file_t_ref.write(t_ref + "\n")
    file_t_ref.close()

# keep log files lines less than max_lines
def limitMaxLines(filename, max_lines):
    with open(filename) as f:
        num_lines = sum(1 for line in f)
    if num_lines > max_lines: # removes first line
        with open(filename) as f:
            f.readline() # throw away first line
            with open("temp", mode="w") as tmp:
                for l in f:
                    tmp.write(l) # copy every subsequent lines
        remove(dir_path+filename)
        rename("temp", filename)

while not path.exists(dir_path+"stop"):
    try:
        res = rq.get(CALLCENTER_URL, auth=auth, timeout=10)
        new_t = res.json()["datetime"] if res.ok else t_ref
        if new_t > t_ref:
            rblAlert(ROTATION_TIME)
            t_ref = new_t
            file_t_ref = open(dir_path+"t_ref", mode="w")
            file_t_ref.write(t_ref + "\n")
            file_t_ref.close()
    except Exception as ex:
        local_now = datetime.now()
        now_str = local_now.strftime("%Y/%m/%d %H:%M:%S")
        file_err_log = open(dir_path+"err_log", mode="a")
        file_err_log.write(now_st r+ ", " + str(ex) + "\n")
        file_err_log.close()
        limitMaxLines("err_log", 15)
    sleep(SLEEP_TIME)

remove(dir_path+"stop")
print("RBL stopped.")
