
# Hardware Connections

This document describes the GPIO and hardware connections used in the AI Voice Task Reminder Device.

---

## OLED Display

The OLED display communicates with the Raspberry Pi using the I²C interface.

| OLED Pin | Raspberry Pi Pin | GPIO |
|---|---|---|
| VCC | Pin 1 | 3.3V |
| GND | Pin 6 | GND |
| SDA | Pin 3 | GPIO2 |
| SCL | Pin 5 | GPIO3 |

---

## LEDs

### LED A — Microphone Status LED

| LED Pin | Raspberry Pi |
|---|---|
| Long leg (+) | GPIO22 (Pin 15) |
| Short leg (-) | GND (Pin 14) |

### LED B — Processing Status LED

| LED Pin | Raspberry Pi |
|---|---|
| Long leg (+) | GPIO23 (Pin 16) |
| Short leg (-) | GND (Pin 14 or any GND) |

---

## Buttons

### Button A — Navigation / Meeting

| Button Pin | Raspberry Pi |
|---|---|
| One side | GPIO17 (Pin 11) |
| Other side | GND (Pin 9) |

### Button B — Select / Manual Mode

| Button Pin | Raspberry Pi |
|---|---|
| One side | GPIO27 (Pin 13) |
| Other side | GND (Pin 9) |

---

## Speaker

The Raspberry Pi audio output is connected to the speaker through the audio amplifier.

| Function | Raspberry Pi |
|---|---|
| Audio Left | GPIO13 |
| Ground | GND |
| Power | 5V |


## MIC
-----------MIC----------
| Mic Pin | Raspberry Pi |
| ------- | ------------ |
| VDD     | 3.3V         |
| GND     | GND          |
| SCK     | GPIO18       |
| WS      | GPIO19       |
| SD      | GPIO20       |
| L/R     | GND          |
