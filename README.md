# 🕹️ The Adventure - Retro Game Remake with Raspberry Pi Pico Controller (based on The Adventure from Atari 2600 from '80)

This project is a Python-based remake of the classic retro game **"The Adventure"**, playable with a **custom-built controller** using a **Raspberry Pi Pico**, joystick, and two buttons.

---

## 🚀 Features

- 🎮 Retro-style gameplay inspired by *The Adventure*
- 🧠 Built with Python and Arduino IDE
- 🕹️ Custom controller using Raspberry Pi Pico:
  - 1x Analog Joystick (for movement)
  - 2x Buttons for interactions
- 🔌 USB HID support: Pico acts as a gamepad for your PC
- 💾 Open source and easy to expand

---

## 🧰 Hardware Requirements

- 1x Raspberry Pi Pico (or Pico W)
- 1x Analog joystick module (e.g., XY Joystick)
- 2x Push buttons
- Breadboard, jumper wires, resistors
- Optional: 3D-printed or custom-built controller enclosure

---
## 🛠️ How to Run

### 🎮 1. Download the Game  
Clone or download the game executable:  
```bash  
git clone https://github.com/QadamosssQ/TheAdventureGame/releases/download/Release/TheAdventureGame.exe  
```  

### 🧠 2. Set Up the Raspberry Pi Pico Controller  
#### a. Flash CircuitPython  
Download CircuitPython for your Pico:  
[Download UF2](https://downloads.circuitpython.org/bin/raspberry_pi_pico_w/pl/adafruit-circuitpython-raspberry_pi_pico_w-pl-9.2.7.uf2)  
- Plug in your Pico while holding the **BOOTSEL** button.  
- Copy the `.uf2` file to the Pico's memory.  

#### b. Install Adafruit HID Library  
- Download the `adafruit_hid` library from the [Adafruit Bundle](https://circuitpython.org/libraries).  
- Copy the `adafruit_hid` folder into the `/lib` directory on your Pico.  

#### c. Upload Controller Code  
- Copy your custom controller code and place it in the root directory of the Pico.  
- Make sure it's named `code.py` (CircuitPython will auto-run this).

### 🕹️ 3. Connect and Play  
- Plug the Pico into your PC via USB.  
- It should be recognized as a USB gamepad.  
- Launch `TheAdventureGame.exe` and start playing!

---



## 🔧 TODO
- expand levels
- improve data reading from joystick (little bugs)
- create sheme and real pcb for controller
- make 3d case for controller

