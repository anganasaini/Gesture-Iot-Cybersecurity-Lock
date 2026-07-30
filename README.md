# Gesture-Secured IoT Smart Lock with Cybersecurity Hardening

## What This Project Is

This project is a smart lock that you unlock and lock using nothing but your hand — an open palm tells it to unlock, a closed fist tells it to lock. But underneath that simple gesture is a fully engineered security system: every single command your hand generates is encrypted, timestamped, checked for tampering, and logged before it's ever allowed to move the physical lock.

The idea behind this project was to treat a hand gesture the same way any serious system treats a password — as a credential that needs real protection, not just a fun trigger. Alongside the computer vision and hardware side, this project builds a genuine cybersecurity layer: encryption to stop eavesdroppers, replay protection to stop recorded-and-reused attacks, and a lockout system to stop brute-force guessing — the same principles that protect real logins and real locks in industry systems.

The result is a complete, working, end-to-end pipeline: your hand is seen by a webcam, interpreted as a command, secured, transmitted, and finally acted on by a physical ESP32-controlled servo lock — all working together live, not just as separate demo pieces.

---

## How the Whole System Works, Start to Finish

**1. Seeing the gesture.**
A webcam feed is processed frame-by-frame using MediaPipe, a hand-tracking library that maps 21 precise points across your hand (fingertips, knuckles, palm). By comparing the position of each fingertip against the knuckle below it, the system determines how many fingers are extended. Five fingers extended means an open palm; zero extended means a closed fist. Everything in between is ignored, so accidental hand movements don't trigger anything.

**2. Turning the gesture into a command.**
Once a clear open palm or closed fist is detected, it's converted into a simple instruction: "unlock" or "lock." A short cooldown prevents the same gesture from firing the same command dozens of times a second while your hand stays still.

**3. Securing the command before it goes anywhere.**
This is the part that separates this project from a typical gesture demo. Before the command is sent anywhere, it passes through a dedicated security module that:
- **Encrypts it** using AES, so if anyone were intercepting network traffic, all they'd see is unreadable scrambled data — never the actual word "unlock."
- **Timestamps it**, so if an attacker captured that encrypted message and tried replaying it later to fake an unlock, the system checks the age of the message and rejects anything older than five seconds.
- **Tracks failed attempts**, locking out further tries for a cooldown period after three consecutive failures — the same defensive principle used by banking apps and phone lock screens against brute-force guessing.
- **Logs everything**, success or failure, with an exact timestamp, so there's a complete auditable history of every access attempt the system has ever seen.

**4. Acting on the command.**
Once a command clears all of these security checks, it's sent live to an ESP32 microcontroller, which drives a servo motor acting as the physical lock. An "unlock" command rotates the servo to represent the lock opening; a "lock" command rotates it back to represent the lock closing — a real, physically observable reaction to what started as nothing more than a hand gesture in front of a webcam.

---

## Why This Matters

Anyone can build a gesture that toggles an LED. What this project demonstrates instead is an understanding of the full picture: that any input used to control access — whether it's a password, a fingerprint, or a hand gesture — is only as trustworthy as the channel it travels through. The cybersecurity layer here isn't decorative; it directly defends against three realistic, well-known attack patterns: traffic sniffing, replay attacks, and brute force — the same categories that show up in real-world access control systems.

---

## Features

- Real-time hand gesture detection using MediaPipe and OpenCV, tracking 21 hand landmarks per frame to classify open-palm vs closed-fist gestures.
- AES-encrypted command transmission, so packet sniffing on the network reveals only unreadable ciphertext, never the real command.
- Replay-attack protection through timestamping, rejecting any captured-and-resent command older than 5 seconds, even if it decrypts successfully.
- Brute-force lockout, enforcing a temporary cooldown after 3 consecutive failed attempts, mirroring standard account lockout policy.
- Full access logging, recording every attempt (successful, failed, or blocked) with a timestamp for a complete audit trail.
- A live, working gesture-to-lock pipeline where hand gestures directly and immediately control the physical ESP32 + servo lock mechanism.

---

## Architecture

Webcam feeds into Gesture Recognition (Python + MediaPipe), which produces a command: "unlock" or "lock." That command passes into the Cybersecurity Layer (Python + AES), which encrypts the command, attaches a timestamp, checks the replay window, checks the failed-attempt lockout, and logs the attempt. The verified command is then sent live to the ESP32 + Servo Motor, which moves the servo to the locked (0 degrees) or unlocked (90 degrees) position — physically reflecting the original hand gesture in real time.

---

## Technologies Used

| Component | Technology |
|---|---|
| Gesture recognition | Python, OpenCV, MediaPipe |
| Encryption | PyCryptodome (AES) |
| Microcontroller firmware | Arduino C++ (ESP32Servo library) |
| Hardware | ESP32 microcontroller and servo motor |
| Version control | Git and GitHub |

---

## Project Structure

- gesture_test.py — Webcam gesture recognition and live command dispatch
- security_lock.py — Encryption, replay protection, lockout, and logging module
- access_log.txt — Auto-generated log of every unlock/lock attempt
- diagram.json — Circuit diagram of the ESP32 and servo wiring
- sketch.ino — ESP32 firmware controlling the servo-based lock
- security-plan.md — Full design notes explaining the cybersecurity approach
- README.md — This file

---

## Running It Yourself

Requirements: Python 3.11 (MediaPipe currently isn't compatible with the newest Python releases), pip, and a webcam.

---

---

## Security Design Rationale

This project deliberately treats a gesture the same way a password should be treated: as a secret that must be protected in transit, not just at the point of input. The three attack scenarios explicitly defended against are:

- **Network sniffing** — mitigated via AES encryption of every command.
- **Replay attacks** — mitigated via timestamp verification, rejecting any message older than a defined freshness window.
- **Brute-force guessing** — mitigated via a failed-attempt counter and temporary lockout, following the same principle as standard account lockout policies.

Full design notes are documented in security-plan.md.

---

## Project Status

Every planned component of this project is complete and working: gesture recognition, AES encryption, replay protection, failed-attempt lockout, access logging, the ESP32 servo lock, and the live connection tying gesture input directly to the physical lock's behavior.

- [x] Gesture recognition (open palm / closed fist detection)
- [x] AES encryption of commands
- [x] Replay-attack protection
- [x] Failed-attempt lockout
- [x] Access logging
- [x] ESP32 + servo lock hardware
- [x] Live network bridge connecting gesture recognition directly to the ESP32
- [x] Full deployment complete

---

## Author

Built by Angana Saini, combining a cybersecurity background with newly learned computer vision and embedded systems skills — an exploration of what it actually takes to make a "cool gesture demo" trustworthy enough to call a real access control system.