import RPi.GPIO as GPIO
import logging
from configparser import ConfigParser

# Load configuration
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

MOTOR_PINS = config['motor_pins']
CarSpeedControl = 30  # Adjust this value as needed

# Initialize GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(MOTOR_PINS['IN1'], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(MOTOR_PINS['IN2'], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(MOTOR_PINS['IN3'], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(MOTOR_PINS['IN4'], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(MOTOR_PINS['ENA'], GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(MOTOR_PINS['ENB'], GPIO.OUT, initial=GPIO.HIGH)

# Initialize PWM
pwm_ENA = GPIO.PWM(MOTOR_PINS['ENA'], 2000)
pwm_ENB = GPIO.PWM(MOTOR_PINS['ENB'], 2000)
pwm_ENA.start(0)
pwm_ENB.start(0)

def run():
    GPIO.output(MOTOR_PINS['IN1'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN2'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN3'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN4'], GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)
    logging.info("Motor running forward.")

def back():
    GPIO.output(MOTOR_PINS['IN1'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN2'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN3'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN4'], GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)
    logging.info("Motor moving backward.")

def left():
    GPIO.output(MOTOR_PINS['IN1'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN2'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN3'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN4'], GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)
    logging.info("Motor turning left.")

def right():
    GPIO.output(MOTOR_PINS['IN1'], GPIO.HIGH)
    GPIO.output(MOTOR_PINS['IN2'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN3'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN4'], GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)
    logging.info("Motor turning right.")

def brake():
    GPIO.output(MOTOR_PINS['IN1'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN2'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN3'], GPIO.LOW)
    GPIO.output(MOTOR_PINS['IN4'], GPIO.LOW)
    logging.info("Motor braking.")

def cleanup():
    pwm_ENA.stop()
    pwm_ENB.stop()
    GPIO.cleanup()
    logging.info("Motor cleanup done.")
