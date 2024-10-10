import threading
import time
import logging
import os
import signal
import sys
from motor_control import run, back, left, right, brake, cleanup
from sensor_tracking import get_sensor_state, is_robot_on_track
from video_manager import video_recording
from camera_control import look_around  # Import the look_around function
import yaml
from dotenv import load_dotenv
import asyncio  # Import asyncio to handle async functions

load_dotenv()

# Load configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

logging_settings = config["logging"]

# Configure logging
logging.basicConfig(
    level=getattr(logging, logging_settings["level"].upper(), logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(logging_settings["file"]), logging.StreamHandler()],
)

# Retrieve the bearer token securely
token = os.getenv("BEARER_TOKEN")
if not token:
    logging.error(
        "Bearer token not found. Please set the BEARER_TOKEN environment variable."
    )
    sys.exit(1)

# Initialize threading events
recording_event = threading.Event()

is_on_track = False


def tracking_test():
    global is_on_track
    state = get_sensor_state()
    is_on_track = is_robot_on_track(state)

    # Decision tree for motor control based on sensor state
    if state == (0, 0, 0, 0):
        run()
    elif state in [
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (1, 1, 0, 0),
        (1, 0, 0, 1),
        (1, 1, 0, 1),
        (1, 1, 1, 0),
    ]:
        right()
    elif state in [
        (0, 0, 1, 0),
        (0, 0, 0, 1),
        (0, 0, 1, 1),
        (0, 1, 1, 0),
        (1, 0, 1, 0),
        (0, 1, 1, 1),
    ]:
        left()
    elif state == (1, 1, 1, 1):
        brake()


def robot_control():
    global is_on_track
    logging.info("Robot control thread started.")
    last_action_time = time.time()

    while True:
        tracking_test()
       

        if is_on_track:
            if not recording_event.is_set():
                logging.info("Starting recording...")
                time.sleep(0.5)
                recording_event.set()
            current_time = time.time()
            # Replace the existing pause logic with look_around
            if current_time - last_action_time >= 2:
                logging.info("Stopping robot for look around sequence.")
                try:
                    brake()
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(look_around())
                    loop.close()
                    logging.info("Look around sequence completed.")
                except Exception as e:
                    logging.error(f"Error during look around: {e}")
                finally:
                    last_action_time = time.time()
        else:
            if recording_event.is_set():
                logging.info("Stopping recording...")
                recording_event.clear()

        time.sleep(0.05)  # Shorter delay for finer control

    logging.info("Robot control thread terminated.")


def signal_handler(sig, frame):
    logging.info("Signal received. Shutting down...")
    recording_event.clear()
    cleanup()
    sys.exit(0)


if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the video recording thread
    recording_thread = threading.Thread(
        target=video_recording, args=(recording_event, token), daemon=True
    )
    recording_thread.start()

    # Start the robot control thread
    control_thread = threading.Thread(target=robot_control, daemon=True)
    control_thread.start()

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        logging.info("Interrupted by user. Shutting down...")
    finally:
        # Cleanup
        recording_event.clear()
        cleanup()
        logging.info("Cleanup done. Exiting.")
