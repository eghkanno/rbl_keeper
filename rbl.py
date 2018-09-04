# coding: utf-8

from time import sleep
from os import path,remove

SLEEP_TIME=10

if path.exists("stop"): remove("stop")

while not path.exists("stop"):
    sleep(SLEEP_TIME)

remove("stop")
print("RBL stopped.")