import RPi.GPIO as GPIO
import logging
from configparser import ConfigParser
import yaml

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

SENSOR_PINS = config['sensor_pins']

# Initialize sensor pins
for pin in SENSOR_PINS.values():
    GPIO.setup(pin, GPIO.IN)

def get_sensor_state():
    TrackSensorLeftValue1  = GPIO.input(SENSOR_PINS['TrackSensorLeftPin1'])
    TrackSensorLeftValue2  = GPIO.input(SENSOR_PINS['TrackSensorLeftPin2'])
    TrackSensorRightValue1 = GPIO.input(SENSOR_PINS['TrackSensorRightPin1'])
    TrackSensorRightValue2 = GPIO.input(SENSOR_PINS['TrackSensorRightPin2'])

    state = (TrackSensorLeftValue1, TrackSensorLeftValue2, TrackSensorRightValue1, TrackSensorRightValue2)
    logging.debug(f"Sensor state: {state}")
    return state

def is_robot_on_track(state):
    return state != (1, 1, 1, 1)
