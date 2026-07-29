from Crypto.Cipher import AES
import json
import time
import uuid

SECRET_KEY = b"ThisIsA16ByteKey"
MAX_AGE_SECONDS = 5
MAX_FAILED_ATTEMPTS = 3
LOCKOUT_SECONDS = 10
LOG_FILE = "access_log.txt"

failed_attempts = 0
lockout_until = 0
used_request_ids = {}


def encrypt_message(command):
    payload = {
        "command": command,
        "timestamp": int(time.time()),
        "request_id": str(uuid.uuid4())
    }

    cipher = AES.new(SECRET_KEY, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(json.dumps(payload).encode())

    return cipher.nonce + tag + ciphertext


def remove_expired_request_ids():
    current_time = time.time()
    expired_ids = [
        request_id
        for request_id, timestamp in used_request_ids.items()
        if current_time - timestamp > MAX_AGE_SECONDS
    ]

    for request_id in expired_ids:
        del used_request_ids[request_id]


def decrypt_message(encrypted_message):
    try:
        nonce = encrypted_message[:16]
        tag = encrypted_message[16:32]
        ciphertext = encrypted_message[32:]

        cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)

        payload = json.loads(decrypted.decode())
        command = payload["command"]
        timestamp = payload["timestamp"]
        request_id = payload["request_id"]

        current_time = time.time()
        age = current_time - timestamp

        if age > MAX_AGE_SECONDS:
            return None, "REJECTED: message too old"

        remove_expired_request_ids()

        if request_id in used_request_ids:
            return None, "REJECTED: replayed message"

        used_request_ids[request_id] = current_time
        return command, "ACCEPTED"

    except Exception:
        return None, "REJECTED: invalid or altered message"


def write_log(result_text):
    readable_time = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{readable_time}] {result_text}\n")


def try_command(encrypted_attempt):
    global failed_attempts, lockout_until

    current_time = time.time()

    if current_time < lockout_until:
        wait_time = round(lockout_until - current_time, 1)
        result = f"BLOCKED: lockout active. Try again in {wait_time}s"
        write_log(result)
        return result

    command, status = decrypt_message(encrypted_attempt)

    if status == "ACCEPTED" and command == "unlock":
        failed_attempts = 0
        result = "UNLOCKED"
        write_log(result)
        return result

    if status == "ACCEPTED" and command == "lock":
        failed_attempts = 0
        result = "LOCKED"
        write_log(result)
        return result

    failed_attempts += 1

    if failed_attempts >= MAX_FAILED_ATTEMPTS:
        lockout_until = current_time + LOCKOUT_SECONDS
        result = f"REJECTED ({failed_attempts}/{MAX_FAILED_ATTEMPTS}) — LOCKED OUT for {LOCKOUT_SECONDS}s"
    else:
        result = f"REJECTED ({failed_attempts}/{MAX_FAILED_ATTEMPTS})"

    write_log(f"{result} | {status}")
    return result


if __name__ == "__main__":
    unlock_attempt = encrypt_message("unlock")
    lock_attempt = encrypt_message("lock")

    print("Unlock test:", try_command(unlock_attempt))
    print("Lock test:", try_command(lock_attempt))
    print("Replay test:", try_command(lock_attempt))