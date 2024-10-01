# Real-Time Robot Control System
## Watch the Video
[Watch the video on Google Drive](https://drive.google.com/file/d/1KT3zfMxrSUyNrONq2Dl1u-8bTKiKahBC/view?usp=sharing)

## Overview

This project demonstrates a real-time robot control system using Raspberry Pi and various sensors, motors, and cameras. It is designed to navigate autonomously, avoid obstacles, track black lines, and stream real-time video for AI-based analysis using YOLO and GPT-4V. The project was developed by **Haim Ozer** and **Shon Pazarker** to showcase skills in real-time embedded systems, robotics, and AI integration.

## Features

- **Motor Control**: The robot uses two DC motors controlled via an H-Bridge module for forward, backward, and directional movements.
- **Servo Motors**: Three servo motors control the ultrasonic sensor for obstacle avoidance and a camera for panoramic view (horizontal and vertical movements).
- **Camera Module**: A USB camera streams real-time video which is uploaded via Wi-Fi to a remote server for AI processing.
- **Obstacle Avoidance**: An ultrasonic sensor mounted on a servo detects obstacles and adjusts the robot's path.
- **Line Tracking**: Four infrared sensors enable the robot to follow a black line on the ground.
- **AI Integration**: Video streams are processed by a remote server using YOLO and GPT-4V for object detection and analysis. A PDF report is generated with a frame-by-frame timeline of detected objects.

## Hardware Components

1. **3 Servo Motors**: 
    - 1 for obstacle avoidance (ultrasonic sensor rotation).
    - 2 for the camera's horizontal and vertical movement.
2. **2 DC Motors**: Controlled via H-Bridge for movement.
3. **USB Camera**: Streams video for remote AI processing.
4. **Ultrasonic Sensor**: Mounted on a servo motor for real-time obstacle detection.
5. **4 Infrared Line Tracking Sensors**: Constantly monitor the robot's position on a black line.

## Software Components

- **Real-time Motor Control**: The robot uses GPIO pins to control the motors, ensuring precise movement based on sensor input.
- **Video Streaming**: A threading mechanism captures video from the camera and uploads it via Wi-Fi to a remote server.
- **AI Video Processing**: YOLO and GPT-4V analyze the uploaded video, generating a PDF report summarizing detected objects with a timeline.
- **Obstacle Avoidance Algorithm**: The ultrasonic sensor rotates to scan for obstacles and adjust the robot’s direction in real-time.
- **Line Tracking Algorithm**: The robot stays on track by constantly adjusting its direction based on input from the infrared sensors.

## System Architecture

- **Real-time Control Loop**: The robot constantly processes sensor data and adjusts its movement based on the detected environment, ensuring smooth navigation.
- **Wi-Fi Video Upload**: Real-time video is captured and uploaded to a cloud server for AI analysis.
- **Remote Processing**: The video is analyzed using YOLO for object detection and GPT-4V for frame-by-frame commentary, generating a detailed PDF report.
- **PID Control for Motors**: Ensures accurate motor control, maintaining the robot's speed and direction in response to sensor feedback.

## Key Technologies

- **Raspberry Pi GPIO for Motor and Sensor Control**
- **Real-time Multithreading for Video Capture and Upload**
- **OpenCV for Video Processing**
- **Wi-Fi Communication for Video Upload**
- **YOLO & GPT-4V for AI Processing**
