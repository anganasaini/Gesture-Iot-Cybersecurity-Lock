# Cybersecurity Plan — Gesture IoT Lock

This file explains the 4 security features we will add to the gesture-controlled smart lock, once the camera (gesture) and ESP32 (lock) parts are both working and connected.

---

## 1. Encryption (hide the message)

**Problem:** Right now, if someone captures the WiFi traffic between your laptop and ESP32, they can read the plain word "unlock" — like a postcard anyone can read.

**Fix:** Scramble ("encrypt") the message using a shared secret key before sending it. Only something holding the same key (your ESP32) can unscramble ("decrypt") it.

**Method:** AES encryption — a standard, well-tested method used across the industry. We are not inventing our own encryption.

---

## 2. Replay Protection (stop "recorded" attacks)

**Problem:** Even with encryption, if someone just copies and resends the *exact same* scrambled message later, it would still work — like replaying a recorded voice password.

**Fix:** Attach a timestamp or a one-time random number (called a "nonce") to every unlock request.
- The ESP32 checks: "Have I seen this exact number before?" or "Is this timestamp too old (e.g. older than 5 seconds)?"
- If either is true, it rejects the request — even if the encrypted message itself is technically correct.

---

## 3. Lockout After Failed Attempts

**Problem:** Without this, someone could try gesture combinations endlessly until they guess correctly.

**Fix:**
- Track failed attempts.
- After 3 wrong attempts in a row, the ESP32 refuses to check any new attempts for a cooldown period (e.g. 30 seconds).
- This mirrors how phone PIN locks work.

---

## 4. Logging (proof of what happened)

**Fix:** Every unlock attempt — successful or failed — gets recorded with:
- Timestamp
- Result (success/failure)
- (Optional later) which gesture sequence was attempted

This log is what lets you demonstrate, like a real security investigation, exactly what happened and when — useful both for your project demo and for catching intrusion attempts.

---

## One-Sentence Summary

> Every unlock request must be encrypted, timestamped, and only accepted once — with failed attempts logged and penalized.

---

## Status

- [x] Camera gesture recognition working (done — see gesture_test.py)
- [ ] ESP32 lock simulation working (waiting on Wokwi server availability)
- [ ] Gesture to ESP32 connection (not started)
- [x] Encryption added (done — see security_lock.py)
- [x] Replay protection added (done — see security_lock.py)
- [x] Lockout after failed attempts added (done — see security_lock.py)
- [ ] Logging added (not started)
- [ ] Final GitHub push and README write-up (not started)

Come back to this checklist and update it as each part is completed.