import speech_recognition as sr
import os
import requests
import pyttsx3
import time

# Set your Windows server IP (Change this to your actual server IP)
SERVER_URL = "http://<your_windows_pc_ip>:5000/upload"

# Define wake words
WAKE_WORDS = ["hi vision", "hey vision", "hello vision", "okay vision", "ok vision",
              "hi vn", "hey vn", "hello vn", "okay vn", "ok vn", "vn", "vision"]

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speaking rate
engine.setProperty('volume', 1.0)  # Adjust volume

# Function to play TTS audio
def play_tts(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("TTS Error:", e)

# Function to capture an image using fswebcam
def capture_image():
    image_path = "captured_image.jpg"
    os.system(f"fswebcam -r 640x480 --no-banner {image_path}")
    return image_path

# Function to send command & image to the server
def send_to_server(command, image_path):
    try:
        with open(image_path, "rb") as image_file:
            files = {"file": image_file}
            data = {"message": command}
            response = requests.post(SERVER_URL, files=files, data=data)
            if response.status_code == 200:
                response_text = response.json().get("response", "No response received")
                print(f"Server Response: {response_text}")
                play_tts(response_text)  # Speak the response
            else:
                print("Server Error:", response.status_code)
                play_tts("Error communicating with server.")
    except Exception as e:
        print("Error sending to server:", e)
        play_tts("Error sending data to server.")

# Function to listen for voice commands
def listen_for_command(recognizer):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        print("Listening for command...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio).lower()
            return command
        except sr.UnknownValueError:
            print("Could not understand the command.")
            return None
        except sr.RequestError:
            print("Speech recognition service is unavailable.")
            return None
        except Exception as e:
            print(f"Error during command listening: {e}")
            return None

# Function to listen for the wake word
def listen_for_wake_word():
    recognizer = sr.Recognizer()

    play_tts("Vision Boost Started...")

    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for wake word...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                command = recognizer.recognize_google(audio).lower()

                if command in WAKE_WORDS:
                    print("Wake word detected! Now listening for your command...")
                    play_tts("Wake word detected! Now listening for your command.")
                    command = listen_for_command(recognizer)

                    if command:
                        print(f"Detected Command: {command}")
                        play_tts("Processing command...")

                        # Capture image
                        image_path = capture_image()
                        print(f"Image captured: {image_path}")

                        # Send data to server
                        send_to_server(command, image_path)

            except sr.UnknownValueError:
                print("No wake word detected.")
            except sr.WaitTimeoutError:
                print("No speech detected within timeout.")
            except sr.RequestError:
                play_tts("Speech recognition failed. Exiting Vision Boost.")
                break
            except Exception as e:
                print(f"Error during wake word listening: {e}")

# Main function
def main():
    listen_for_wake_word()

if __name__ == "__main__":
    main()
