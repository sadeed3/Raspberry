import requests
import cv2  # OpenCV for USB Webcam
from picamera import PiCamera
from time import sleep

# Replace with your Windows PC's public IP
SERVER_IP = "YOUR_PUBLIC_IP"  # e.g., "203.0.113.45"
PORT = 5000

# Use either PiCamera or OpenCV
USE_PICAMERA = False  # Set to True if using Raspberry Pi Camera Module


def capture_image(image_path="image.jpg"):
    if USE_PICAMERA:
        # Capture image using Raspberry Pi Camera Module
        camera = PiCamera()
        camera.start_preview()
        sleep(2)  # Give camera time to adjust
        camera.capture(image_path)
        camera.stop_preview()
        camera.close()
    else:
        # Capture image using USB Webcam
        cap = cv2.VideoCapture(0)  # 0 for the first camera
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(image_path, frame)
        cap.release()


# Capture live image
image_filename = "live_image.jpg"
capture_image(image_filename)

# Send text + live image
data = {"message": "Hello from Raspberry Pi!"}
files = {'file': open(image_filename, 'rb')}

response = requests.post(f"http://{SERVER_IP}:{PORT}/upload", data=data, files=files)

# Print response from Windows PC
if response.status_code == 200:
    response_json = response.json()
    print("Received from server:", response_json.get("response"))
else:
    print("Failed to receive response")
