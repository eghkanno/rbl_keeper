# coding: utf-8

import yaml
import RPi.GPIO as GPIO

CONFIG_FILENAME = "config.yml"
config = yaml.load(open(CONFIG_FILENAME))
GPIO_OUT = config["gpio_out"]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_OUT, GPIO.OUT)
GPIO.output(GPIO_OUT, False)
GPIO.cleanup()

print("manual break applied.")