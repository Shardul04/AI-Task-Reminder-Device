import RPi.GPIO as GPIO
import threading
import time
from flask import Flask, request
import json
import os

LED_MIC = 22
LED_PROCESS = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_MIC, GPIO.OUT)
GPIO.setup(LED_PROCESS, GPIO.OUT)

GPIO.output(LED_MIC, 1)
GPIO.output(LED_PROCESS, 0)

app = Flask(__name__)

TASK_FILE = "tasks.json"

# Create tasks.json if it doesn't exist
if not os.path.exists(TASK_FILE):
    with open(TASK_FILE, "w") as f:
        json.dump([], f)

# ---------------- TASK API ----------------

@app.route("/task", methods=["POST"])
def receive_task():

    task = request.json

    with open(TASK_FILE, "r") as f:
        tasks = json.load(f)

    tasks.append(task)

    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

    return {"status": "task saved"}


# ---------------- LED API ----------------

@app.route("/led", methods=["POST"])
def led_control():

    data = request.json
    state = data.get("state")

    if state == "processing":

        GPIO.output(LED_PROCESS, 1)

    elif state == "listening":

        GPIO.output(LED_PROCESS, 0)

    elif state == "name":

        GPIO.output(LED_MIC, 1)
        GPIO.output(LED_PROCESS, 1)

        time.sleep(0.2)

        GPIO.output(LED_MIC, 0)
        GPIO.output(LED_PROCESS, 0)

    return {"status": "ok"}


# ---------------- MIC BREATHING ----------------

def mic_breathe():

    while True:

        GPIO.output(LED_MIC, 1)
        time.sleep(0.7)

        GPIO.output(LED_MIC, 0)
        time.sleep(0.7)


threading.Thread(target=mic_breathe, daemon=True).start()


# ---------------- SERVER START ----------------

app.run(host="0.0.0.0", port=5000)