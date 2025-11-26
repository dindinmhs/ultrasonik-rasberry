import RPi.GPIO as GPIO
import time
import requests
from datetime import datetime
import threading

SERVER_URL = "http://192.168.1.100:5000"

TRIG_PIN = 23
ECHO_PIN = 24

REALTIME_INTERVAL = 1
STORE_INTERVAL = 60

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    pulse_start = time.time()
    pulse_end = time.time()
    timeout = time.time() + 1

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def send_realtime(distance):
    try:
        data = {
            'distance': distance,
            'timestamp': datetime.now().isoformat()
        }
        response = requests.post(
            f"{SERVER_URL}/api/realtime",
            json=data,
            timeout=5
        )
        if response.status_code == 200:
            print(f"[REALTIME] Sent: {distance} cm")
        else:
            print(f"[REALTIME] Error: {response.status_code}")
    except Exception as e:
        print(f"[REALTIME] Exception: {e}")

def send_store(distance):
    try:
        data = {
            'distance': distance,
            'timestamp': datetime.now().isoformat()
        }
        response = requests.post(
            f"{SERVER_URL}/api/store",
            json=data,
            timeout=5
        )
        if response.status_code == 200:
            print(f"[STORE] Saved: {distance} cm")
        else:
            print(f"[STORE] Error: {response.status_code}")
    except Exception as e:
        print(f"[STORE] Exception: {e}")

def realtime_loop():
    while True:
        distance = measure_distance()
        if distance is not None and 2 < distance < 400:
            send_realtime(distance)
        time.sleep(REALTIME_INTERVAL)

def store_loop():
    while True:
        distance = measure_distance()
        if distance is not None and 2 < distance < 400:
            send_store(distance)
        time.sleep(STORE_INTERVAL)

def main():
    print("Starting sensor monitoring...")
    print(f"Server: {SERVER_URL}")
    print(f"Realtime interval: {REALTIME_INTERVAL}s")
    print(f"Store interval: {STORE_INTERVAL}s")
    
    realtime_thread = threading.Thread(target=realtime_loop, daemon=True)
    store_thread = threading.Thread(target=store_loop, daemon=True)
    
    realtime_thread.start()
    store_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping sensor monitoring...")
        GPIO.cleanup()

if __name__ == "__main__":
    main()