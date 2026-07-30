# Gesture-Secured IoT Smart Lock with Cybersecurity Hardening

## What This Project Is

This project is a smart lock that you unlock and lock using nothing but your hand — an open palm tells it to unlock, a closed fist tells it to lock. But underneath that simple gesture is a fully engineered security system: every single command your hand generates is encrypted, timestamped, checked for tampering, and logged before it's ever allowed to move the physical lock.

The idea behind this project was to treat a hand gesture the same way any serious system treats a password — as a credential that needs real protection, not just a fun trigger. Alongside the computer vision and hardware side, this project builds a genuine cybersecurity layer: encryption to stop eavesdroppers, replay protection to stop recorded-and-reused attacks, and a lockout system to stop brute-force guessing — the same principles that protect real logins and real locks in industry systems.

---

## How the Whole System Works, Start to Finish

**1. Seeing the gesture.**
A webcam feed is processed frame-by-frame using MediaPipe, a hand-tracking library that maps 21 precise points across your hand. By comparing each fingertip's position against the knuckle below it, the system determines how many fingers are extended. Five fingers extended means an open palm; zero extended means a closed fist.

**2. Turning the gesture into a command.**
A clear open palm or closed fist is converted into a simple instruction: "unlock" or "lock." A short cooldown prevents the same gesture from firing repeatedly while your hand stays still.

**3. Securing the command before it goes anywhere.**
Before the command goes anywhere, it passes through a dedicated security module (`security_lock_v2.py`) that:
- **Encrypts it** using AES-GCM, an authenticated encryption mode that both scrambles the message and detects if it has been tampered with.
- **Attaches a unique request ID and timestamp** to every message, so even identical commands can never be captured and replayed later — each one only works once, within a 5-second freshness window.
- **Tracks failed attempts**, locking out further tries for a cooldown period after three consecutive failures.
- **Logs everything**, success or failure, with a timestamp, to `access_log.txt`.

**4. Acting on the command.**
Once a command clears all security checks, it's sent to an ESP32 microcontroller (wiring defined in `diagram.json`, firmware in `sketch.ino`), which drives a servo motor acting as the physical lock — rotating to represent unlocking or locking.

---

## Features

- Real-time hand gesture detection using MediaPipe and OpenCV.
- AES-GCM authenticated encryption — detects both eavesdropping and tampering, not just scrambling data.
- Replay-attack protection using unique request IDs plus timestamp freshness checks.
- Brute-force lockout after 3 consecutive failed attempts.
- Full access logging with timestamps for every attempt.
- ESP32 + servo motor hardware simulation representing the physical lock.

---

## Technologies Used

| Component | Technology |
|---|---|
| Gesture recognition | Python, OpenCV, MediaPipe |
| Encryption | PyCryptodome (AES-GCM) |
| Microcontroller firmware | Arduino C++ (ESP32Servo library) |
| Hardware simulation | Wokwi (ESP32 + Servo Motor) |
| Version control | Git and GitHub |

---

## Project Structure

- gesture_test.py — Webcam gesture recognition and command dispatch
- security_lock_v2.py — Cybersecurity module: AES-GCM encryption, replay protection (via unique request IDs), lockout, and logging
- access_log.txt — Auto-generated log of every unlock/lock attempt
- diagram.json — Circuit diagram of the ESP32 and servo wiring
- sketch.ino — ESP32 firmware controlling the servo-based lock (in Wokwi project)
- security-plan.md — Design notes explaining the cybersecurity approach
- README.md — This file

---

## Running It Yourself

Requirements: Python 3.11 (MediaPipe currently isn't compatible with the newest Python releases), pip, a webcam.

---

To view the ESP32 hardware simulation, open the project on Wokwi (wokwi.com) using the included `diagram.json` and `sketch.ino` files.

---

## Security Design Rationale

This project treats a gesture the same way a password should be treated: as a secret that must be protected in transit, not just at the point of input. Three realistic attack scenarios are explicitly defended against:

- **Network sniffing** — mitigated via AES-GCM encryption of every command.
- **Replay attacks** — mitigated via unique request IDs and timestamp verification.
- **Brute-force guessing** — mitigated via a failed-attempt counter and temporary lockout.

Full design notes are documented in `security-plan.md`.

---

## Project Status

- [x] Gesture recognition (open palm / closed fist detection)
- [x] AES-GCM encryption of commands
- [x] Replay-attack protection (unique request IDs + timestamps)
- [x] Failed-attempt lockout
- [x] Access logging
- [x] ESP32 + servo lock hardware simulation

---

## Author

Built by Angana Saini, combining a cybersecurity background with newly learned computer vision and embedded systems skills.
