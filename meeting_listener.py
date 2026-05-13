import sounddevice as sd
import queue
import whisper
import numpy as np
import requests
import re
from datetime import datetime, timedelta

#API_URL = "http://10.40.81.206:5000/task"
#LED_API = "http://10.40.81.206:5000/led"

API_URL = "http://10.106.225.206:5000/task"
LED_API = "http://10.106.225.206:5000/led"

# Load Whisper model
model = whisper.load_model("small")

# Audio configuration
samplerate = 16000
duration = 8

sd.default.samplerate = samplerate
sd.default.channels = 1

NAME_VARIATIONS = [
    "mike",
    "miche",
    "bike",
    "myke",
    "maik",
    "mik",
    "mikeh",
    "mikel",
    "mikey",
    "mikie",
    "miike",
    "mic",
    "bikee",
    "mikh",
    "mikee",
    "maike",
    "miak",
    "mic",
    "mikeee",
    "mikay",
    "my",
]
last_task_text = ""

print("🎤 AI Meeting Listener started...")

def extract_task(text):

    now = datetime.now()
    date = now
    task_time = now + timedelta(hours=1)

    # -------- detect tomorrow --------
    if "tomorrow" in text:
        date = now + timedelta(days=1)
        task_time = task_time.replace(day=date.day)

    # -------- detect "in X minutes" --------
    minute_match = re.search(r"in (\d+) minute", text)
    if minute_match:
        mins = int(minute_match.group(1))
        task_time = now + timedelta(minutes=mins)

    # -------- detect "in one minute" --------
    if "in one minute" in text:
        task_time = now + timedelta(minutes=1)

    # -------- detect specific time --------
    time_match = re.search(r"(?:by|at) (\d+)\s?(am|pm)?", text)

    if time_match:

        hour = int(time_match.group(1))
        meridian = time_match.group(2)

        if meridian == "pm" and hour < 12:
            hour += 12

        if meridian == "am" and hour == 12:
            hour = 0

        task_time = task_time.replace(hour=hour, minute=0)

    # -------- task extraction --------
    task = ""

    patterns = [
        r"shardul (.+)",
        r"you will (.+)",
        r"please (.+)",
        r"submit (.+)",
        r"complete (.+)"
    ]

    for p in patterns:
        match = re.search(p, text)
        if match:
            task = match.group(1)
            break

    if task == "":
        task = text.replace("shardul", "").strip()

    task_json = {
        "task": task,
        "time": task_time.strftime("%H:%M"),
        "date": task_time.strftime("%d-%m-%y"),
        "notified": False,
        "task_completed": False
    }

    return task_json

while True:

    print("🎧 Listening...")
    requests.post(LED_API, json={"state": "listening"})

    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    audio = np.squeeze(audio)

    # now we are processing speech
    requests.post(LED_API, json={"state": "processing"})

    try:
        result = model.transcribe(audio, language="en", fp16=False)
    except:
        continue

    text = result["text"].lower().strip()

    if not text:
        continue

    # remove short nonsense phrases
    if len(text.split()) < 3:
        continue

    print("Heard:", text)

    # check if any variation of the name is detected
    if not any(name in text for name in NAME_VARIATIONS):
        continue

    print("📌 Name detected")
    requests.post(LED_API, json={"state": "name"})

    task = extract_task(text)

    # avoid duplicate tasks
    if task["task"] == last_task_text:
        continue

    last_task_text = task["task"]

    print("📋 Task extracted:", task)

    try:
        requests.post(API_URL, json=task)
        print("✅ Task sent to device")
    except:
        print("❌ Failed to send task")