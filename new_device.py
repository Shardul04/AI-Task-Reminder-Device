import os
import json
import time
import RPi.GPIO as GPIO
from datetime import datetime
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from PIL import ImageFont

TASK_FILE = "tasks.json"

BUTTON_A = 17
BUTTON_B = 27
BUZZER_PIN = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# PWM speaker setup
speaker = GPIO.PWM(BUZZER_PIN, 2000)

serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

font = ImageFont.load_default()

selected_index = 0
scroll_offset = 0
last_b_press = 0

def speak_task(text):

    os.system(f'pico2wave -w speech.wav "Reminder {text}"')
    os.system("aplay speech.wav")

def load_tasks():
    try:
        with open(TASK_FILE, "r") as f:
            tasks = json.load(f)

        active = []

        for t in tasks:
            if not t.get("completed", False):
                active.append(t)

        return active

    except:
        return []


def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def mark_completed(index):

    try:

        with open(TASK_FILE, "r") as f:
            tasks = json.load(f)

        count = -1

        for task in tasks:

            if not task.get("completed", False):
                count += 1

            if count == index:
                task["completed"] = True
                break

        save_tasks(tasks)

    except:
        pass


def show_popup(text):

    with canvas(device) as draw:

        draw.text((20, 0), "REMINDER", fill="white", font=font)

        words = text.split()

        line1 = " ".join(words[:3])
        line2 = " ".join(words[3:6])

        draw.text((0, 25), line1, fill="white", font=font)
        draw.text((0, 45), line2, fill="white", font=font)

    speak_task(text)

    time.sleep(4)


while True:

    tasks = load_tasks()

    now = datetime.now()

    # reminder engine
    for task in tasks:

        if task.get("notified"):
            continue

        try:

            deadline = datetime.strptime(
                task["date"] + " " + task["time"],
                "%d-%m-%y %H:%M"
            )

            if now >= deadline:

                print("REMINDER:", task["task"])

                show_popup(task["task"])

                task["notified"] = True

                save_tasks(tasks)

        except:
            pass


    # navigation button
    if GPIO.input(BUTTON_A) == 0:

        selected_index += 1

        if selected_index >= len(tasks):
            selected_index = 0
            scroll_offset = 0

        if selected_index >= scroll_offset + 3:
            scroll_offset += 1

        time.sleep(0.2)


    # complete button
    if GPIO.input(BUTTON_B) == 0:

        press_time = time.time()

        if press_time - last_b_press > 0.4:

            mark_completed(selected_index)

            last_b_press = press_time

        while GPIO.input(BUTTON_B) == 0:
            time.sleep(0.01)


    # display tasks
    try:

        with canvas(device) as draw:

            draw.text((0, 0), "Tasks:", fill="white", font=font)

            visible = tasks[scroll_offset:scroll_offset + 3]

            y = 12

            for i, task in enumerate(visible):

                real_index = scroll_offset + i

                name = task.get("task", "unknown")
                time_text = task.get("time", "--:--")

                serial = real_index + 1

                if real_index == selected_index:

                    draw.rectangle(
                        (0, y - 1, 127, y + 20),
                        outline="white",
                        fill=None
                    )

                draw.text(
                    (2, y),
                    f"{serial}.{name[:18]}",
                    fill="white",
                    font=font
                )

                y += 10


                date_text = task.get("date", "--").split("-")[0] + "-" + task.get("date", "--").split("-")[1]
                draw.text(
                    (8, y),
                    time_text,
                    fill="white",
                    font=font
                )

                # date (right side)
                draw.text(
                   (90, y),   # adjust if needed
                   date_text,
                   fill="white",
                   font=font
                )



                y += 12

    except Exception as e:
        print("OLED glitch", e)

    time.sleep(0.15)