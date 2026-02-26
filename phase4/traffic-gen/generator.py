import os
import time
import random
import httpx
import json

TARGET_URL = os.getenv("TARGET_URL", "http://app.default.svc.cluster.local:8080/login")
SCENARIO = os.getenv("SCENARIO", "normal")
DURATION = int(os.getenv("DURATION_SECONDS", "120"))
RPS = float(os.getenv("RPS", "2"))

USERNAMES = ["alice", "bob", "carol", "dave", "erin"]
PASSWORDS = ["Password123!", "Welcome1!", "Qwerty123!"]

ATTACKER_IP = "203.0.113.66"
NORMAL_IPS = ["198.51.100.10", "198.51.100.11", "198.51.100.12"]

def send_request(client, username, password, ip):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-Forwarded-For": ip
    }

    payload = {
        "username": username,
        "password": password
    }

    try:
        response = client.post(TARGET_URL, json=payload, headers=headers)
        print(json.dumps({
            "event": "auth_attempt",
            "username": username,
            "src_ip": ip,
            "status_code": response.status_code
        }))
    except Exception as e:
        print(json.dumps({
            "event": "error",
            "error": str(e)
        }))

def main():
    interval = 1.0 / RPS
    end_time = time.time() + DURATION

    with httpx.Client(timeout=5) as client:
        while time.time() < end_time:
            if SCENARIO == "brute":
                username = "alice"
                password = random.choice(PASSWORDS)
                ip = ATTACKER_IP
            else:
                username = random.choice(USERNAMES)
                password = random.choice(PASSWORDS)
                ip = random.choice(NORMAL_IPS)

            send_request(client, username, password, ip)
            time.sleep(interval)

if __name__ == "__main__":
    main()
    