# AI Voice Task Reminder Device

An AI-powered voice task reminder system that uses a **laptop's built-in microphone** to capture voice input, sends audio chunks to a **Raspberry Pi Zero 2 WH**, and uses **Whisper-based speech recognition** to convert spoken instructions into structured tasks and deadlines.

The project combines **embedded Linux, Python, speech recognition, network communication, hardware interfacing, and a physical task-management device** into a single system.

---

##  Features

- 🎤 Voice input using a laptop's built-in microphone
- 📡 Audio transmission from laptop to Raspberry Pi
- 🧩 Chunk-based audio processing
- 🧠 Speech-to-text using Whisper
- 📋 Automatic task extraction
- ⏰ Deadline extraction from spoken instructions
- 🖥️ OLED display for task information
- 🔘 Physical buttons for device interaction
- 🔊 Audio output through an external speaker
- 🐍 Python-based implementation
- 🌐 Flask-based communication
- 🔋 Battery-powered Raspberry Pi
- 📦 Custom 3D-printed enclosure

---

# System Architecture

The system is divided into two main parts:

### 1. Laptop

The laptop acts as the **voice input device**.

Its built-in microphone captures the user's speech and the audio is divided into chunks before being sent to the Raspberry Pi over the network.

### 2. Raspberry Pi

The Raspberry Pi acts as the **embedded processing and task-management device**.

It receives the audio chunks, processes them using Whisper, extracts task and deadline information, and manages the resulting tasks.

```text
┌──────────────────────────────┐
│            LAPTOP            │
│                              │
│    Built-in Microphone       │
│             │                │
│             ▼                │
│      Audio Recording         │
│             │                │
│             ▼                │
│       Audio Chunks           │
└─────────────┬────────────────┘
              │
              │ Network
              │
              ▼
┌──────────────────────────────┐
│      RASPBERRY PI ZERO 2 WH  │
│                              │
│      Receive Audio Chunks    │
│               │              │
│               ▼              │
│       Whisper Processing      │
│               │              │
│               ▼              │
│      Task & Deadline         │
│          Extraction          │
│               │              │
│        ┌──────┴──────┐       │
│        ▼             ▼       │
│   OLED Display    Task System│
│        │                     │
│        ▼                     │
│     Speaker                  │
└──────────────────────────────┘
