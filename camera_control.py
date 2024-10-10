# camera_control.py
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import asyncio
import logging

# Configure logging for this module
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configuration Constants
SERVO_PINA = 11   # BCM GPIO pin for Servo A (Horizontal Movement)
SERVO_PINB = 9  # BCM GPIO pin for Servo B (Vertical Movement)

# Servo Angles
CENTER_ANGLE_A = 80    # Center position for Servo A
LEFT_ANGLE_A = 45      # Left position for Servo A
RIGHT_ANGLE_A = 135    # Right position for Servo A

CENTER_ANGLE_B = 75    # Center position for Servo B
BOTTOM_ANGLE_B = 55   # Bottom position for Servo B
TOP_ANGLE_B = 70       # Top position for Servo B

# PWM Frequency
PWM_FREQUENCY = 50  # 50Hz is standard for servos

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up GPIO pins for servos
GPIO.setup(SERVO_PINA, GPIO.OUT)
GPIO.setup(SERVO_PINB, GPIO.OUT)

# Initialize PWM for both servos
servoa_pwm = GPIO.PWM(SERVO_PINA, PWM_FREQUENCY)
servob_pwm = GPIO.PWM(SERVO_PINB, PWM_FREQUENCY)

# Start PWM with 0% duty cycle (servo not moving)
servoa_pwm.start(0)
servob_pwm.start(0)

def set_servoa_angle(angle):
    """
    Move Servo A (Horizontal) to the specified angle.
    
    :param angle: The angle to move Servo A to (0 to 180 degrees)
    """
    duty = 2 + (angle / 18)  # Convert angle to duty cycle
    logging.debug(f"Setting Servo A to {angle} degrees (Duty Cycle: {duty}%)")
    GPIO.output(SERVO_PINA, True)
    servoa_pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Allow time for the servo to move
    GPIO.output(SERVO_PINA, False)
    servoa_pwm.ChangeDutyCycle(0)  # Stop sending signal

def set_servob_angle(angle):
    """
    Move Servo B (Vertical) to the specified angle.
    
    :param angle: The angle to move Servo B to (0 to 180 degrees)
    """
    duty = 2 + (angle / 18)  # Convert angle to duty cycle
    logging.debug(f"Setting Servo B to {angle} degrees (Duty Cycle: {duty}%)")
    GPIO.output(SERVO_PINB, True)
    servob_pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Allow time for the servo to move
    GPIO.output(SERVO_PINB, False)
    servob_pwm.ChangeDutyCycle(0)  # Stop sending signal

async def look_around():
    """
    Asynchronously move the camera to look left and bottom, 
    then right and bottom, and finally return to center.
    """
    logging.info("Initiating look_around sequence.")

    # Move to Left and Bottom
    logging.info("Moving to Left and Bottom.")
    set_servoa_angle(LEFT_ANGLE_A)
    set_servob_angle(BOTTOM_ANGLE_B)
    await asyncio.sleep(1)  # Wait for the movement to complete
    set_servob_angle(TOP_ANGLE_B)
    await asyncio.sleep(1)  # Wait for the movement to complete

    # Move to Right and Bottom
    logging.info("Moving to Right and Bottom.")
    set_servoa_angle(RIGHT_ANGLE_A)
    set_servob_angle(BOTTOM_ANGLE_B)
    await asyncio.sleep(1)  # Wait for the movement to complete
    set_servob_angle(TOP_ANGLE_B)
    await asyncio.sleep(1)  # Wait for the movement to complete

    # Return to Center
    logging.info("Returning to Center.")
    set_servoa_angle(CENTER_ANGLE_A)
    set_servob_angle(CENTER_ANGLE_B)
    await asyncio.sleep(1)  # Wait for the movement to complete

    logging.info("look_around sequence completed.")

def cleanup():
    """
    Clean up the GPIO settings and stop PWM.
    """
    logging.info("Cleaning up GPIO and stopping PWM.")
    servoa_pwm.stop()
    servob_pwm.stop()
    GPIO.cleanup()
    logging.info("Cleanup completed.")
