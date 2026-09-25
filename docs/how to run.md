ssh <username>@<raspberry-pi-hostname>
cd ai_reminder_device
source venv/bin/activate
python task_receiver.py
python new_device.py

//for manual entries
from task_manager import *
add_task("Voice test", "2026-03-07 16:04")

//to kill all the process
pkill -f python

// to test sound
aplay /usr/share/sounds/alsa/Front_Center.wav
alsamixer


//to run on laptop 
python voice_to_task.py
venv\Scripts\activate