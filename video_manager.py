import cv2
import datetime
import os
import logging
import requests
from concurrent.futures import ThreadPoolExecutor
import yaml
import time

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

video_settings = config['video_settings']
upload_settings = config['upload_settings']
logging_settings = config['logging']

# Initialize ThreadPoolExecutor for uploads
executor = ThreadPoolExecutor(max_workers=2)

def upload_video(file_path, token):
    """
    Uploads a video file to the specified endpoint with a bearer token.

    Args:
        file_path (str): The path to the video file to upload.
        token (str): Bearer token for authorization.
    """
    url = upload_settings['url']
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept-Language': 'en-US',
    }

    if not os.path.isfile(file_path):
        logging.error(f"File not found: {file_path}")
        return

    try:
        with open(file_path, 'rb') as f:
            files = {
                'file': (os.path.basename(file_path), f, upload_settings['mime_type'])
            }
            response = requests.post(url, headers=headers, files=files)

        if response.status_code in [200, 201]:
            logging.info(f"Successfully uploaded {file_path}")
            # Optionally delete the file after successful upload
            # os.remove(file_path)
        else:
            logging.error(f"Failed to upload {file_path}. Status Code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.error(f"An error occurred while uploading {file_path}: {e}")

def video_recording(recording_event, token):
    logging.info("Video recording thread started.")
    video_writer = None
    filename = None

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Could not open video capture device.")
        return

    videos_dir = video_settings['directory']
    os.makedirs(videos_dir, exist_ok=True)

    while True:
        if recording_event.is_set():
            if video_writer is None:
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = os.path.join(videos_dir, f"{timestamp}.mp4")
                fourcc = cv2.VideoWriter_fourcc(*video_settings['codec'])
                video_writer = cv2.VideoWriter(filename, fourcc, video_settings['fps'], tuple(video_settings['resolution']))
                logging.info(f"Recording started: {filename}")

            ret, frame = cap.read()
            if ret:
                video_writer.write(frame)
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                logging.error("Error reading from camera.")
                break
        else:
            if video_writer is not None:
                logging.info("Recording stopped.")
                video_writer.release()
                video_writer = None
                if filename:
                    executor.submit(upload_video, filename, token)
        time.sleep(0.1)  # Sleep briefly to avoid high CPU usage

    cap.release()
    if video_writer is not None:
        video_writer.release()
        if filename:
            executor.submit(upload_video, filename, token)
    cv2.destroyAllWindows()
    logging.info("Video recording thread terminated.")
