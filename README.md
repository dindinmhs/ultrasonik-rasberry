# Ultrasonic Sensor Raspberry Pi Client

Client untuk membaca sensor ultrasonik HC-SR04 dan mengirim data ke server.

## Setup

1. Clone repository:
```bash
git clone https://github.com/dindinmhs/ultrasonik-rasberry.git
cd ultrasonik_rasberry
```

2. Install dependencies:
```bash
pip install RPi.GPIO requests
```

3. Atur server URL di `client.py`:
```python
SERVER_URL = "http://192.168.1.100:5000"  # Ganti dengan IP server Anda
```

4. Jalankan client:
```bash
python client.py
```

## Konfigurasi Pin

- TRIG_PIN: GPIO 23
- ECHO_PIN: GPIO 24

## Interval

- Realtime: 1 detik
- Store: 60 detik
