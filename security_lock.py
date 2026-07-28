from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time

SECRET_KEY = b'ThisIsA16ByteKey'
MAX_AGE_SECONDS = 5
MAX_FAILED_ATTEMPTS = 3
LOCKOUT_SECONDS = 10

failed_attempts = 0
lockout_until = 0

def encrypt_message(message):
    timestamp = str(int(time.time()))
    full_message = f"{message}|{timestamp}"
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    padded_message = pad(full_message.encode(), AES.block_size)
    return cipher.encrypt(padded_message)

def decrypt_message(encrypted_message):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    decrypted_padded = cipher.decrypt(encrypted_message)
    full_message = unpad(decrypted_padded, AES.block_size).decode()
    message, timestamp = full_message.split("|")
    age = int(time.time()) - int(timestamp)

    if age > MAX_AGE_SECONDS:
        return None, "REJECTED: message too old"
    return message, "ACCEPTED"

def try_unlock(encrypted_attempt, correct_message="unlock"):
    global failed_attempts, lockout_until

    current_time = time.time()

    if current_time < lockout_until:
        wait_time = round(lockout_until - current_time, 1)
        return f"BLOCKED: too many failed attempts. Try again in {wait_time}s"

    message, status = decrypt_message(encrypted_attempt)

    if status == "ACCEPTED" and message == correct_message:
        failed_attempts = 0
        return "UNLOCKED"
    else:
        failed_attempts += 1
        if failed_attempts >= MAX_FAILED_ATTEMPTS:
            lockout_until = current_time + LOCKOUT_SECONDS
            return f"WRONG ({failed_attempts}/{MAX_FAILED_ATTEMPTS}) — LOCKED OUT for {LOCKOUT_SECONDS}s"
        else:
            return f"WRONG ({failed_attempts}/{MAX_FAILED_ATTEMPTS})"

if __name__ == "__main__":
    wrong_attempt = encrypt_message("wronggesture")
    correct_attempt = encrypt_message("unlock")

    print("Attempt 1 (wrong):", try_unlock(wrong_attempt))
    print("Attempt 2 (wrong):", try_unlock(wrong_attempt))
    print("Attempt 3 (wrong):", try_unlock(wrong_attempt))
    print("Attempt 4 (correct, but should be blocked):", try_unlock(correct_attempt))