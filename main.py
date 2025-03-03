import requests

# Replace with your Windows PC's public IP
SERVER_IP = "YOUR_PUBLIC_IP"  # e.g., "203.0.113.45"
PORT = 5000

# Send text + image
data = {"message": "Hello from Raspberry Pi!"}
files = {'file': open('image.jpg', 'rb')}

response = requests.post(f"http://{SERVER_IP}:{PORT}/upload", data=data, files=files)

# Print response from Windows PC
if response.status_code == 200:
    response_json = response.json()
    print("Received from server:", response_json.get("response"))
else:
    print("Failed to receive response")
