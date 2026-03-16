import os
import time
import random
import json
from dataclasses import dataclass
from datetime import datetime, timezone

# ---------- Config ----------
MODE = os.getenv("MODE", "direct")  # direct | http (http later)
PROFILE = os.getenv("PROFILE", "mixed")  # mixed | human | spray | brute_low | brute_burst
DURATION = int(os.getenv("DURATION_SECONDS", "180"))
SEED = int(os.getenv("SEED", "1337"))

# Human-ish traffic knobs
BASELINE_USERS = int(os.getenv("BASELINE_USERS", "40"))     # concurrent-ish population pool size
BASELINE_FAIL_RATE = float(os.getenv("BASELINE_FAIL_RATE", "0.12"))  # % of normal attempts that fail
PAGEVIEW_RATE = float(os.getenv("PAGEVIEW_RATE", "0.35"))   # fraction of sessions that do some "page hits" before login
MAX_EVENTS = int(os.getenv("MAX_EVENTS", "0"))  # 0 = unlimited

SERVICE = os.getenv("SERVICE", "secureworks")
ENV = os.getenv("ENV", "docker-desktop")

# Attack patterns (mixed mode)
SPRAY_PASSWORDS = os.getenv("SPRAY_PASSWORDS", "Winter2026!,Password1!").split(",")
COMMON_PASSWORDS = os.getenv("COMMON_PASSWORDS", "Password123!,Welcome1!,Qwerty123!,LetMeIn123!").split(",")

NORMAL_IPS = os.getenv("NORMAL_IPS", "198.51.100.10,198.51.100.11,198.51.100.12,198.51.100.13").split(",")
ATTACKER_IP = os.getenv("ATTACKER_IP", "203.0.113.66")
ATTACKER_IP_POOL = os.getenv("ATTACKER_IP_POOL", "203.0.113.66,203.0.113.67,203.0.113.68").split(",")

# Synthetic identities
VALID_USERNAME = os.getenv("VALID_USERNAME", "alice")
VALID_PASSWORD = os.getenv("VALID_PASSWORD", "Password123!")

# Build a bigger user pool so it looks real
DEFAULT_USERS = [
    "alice","bob","carol","dave","erin","frank","grace","heidi","ivan","judy",
    "mallory","oscar","peggy","trent","victor","wendy","yuki","zoe","nina","raj",
    "sara","liam","emma","noah","olivia","ava","mia","sophia","jack","lucas",
    "mason","elijah","isabella","amelia","harper","evelyn","abigail","luna","ella","aria"
]
USERNAMES = os.getenv("USERNAMES", ",".join(DEFAULT_USERS)).split(",")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7)",
]

PATHS_PRELOGIN = ["/", "/login", "/assets/app.css", "/assets/app.js", "/favicon.ico"]
LOGIN_PATH = os.getenv("LOGIN_PATH", "/api/login")

def now_rfc3339():
    return datetime.now(timezone.utc).isoformat()

def emit(event: dict):
    print(json.dumps(event), flush=True)

def clamp(n, lo, hi):
    return max(lo, min(hi, n))

def jittered_sleep(mean_s: float, jitter: float = 0.6):
    # lognormal-ish timing: humans have long tail pauses
    x = random.lognormvariate(mu=max(0.01, mean_s), sigma=jitter)
    time.sleep(clamp(x, 0.02, mean_s * 6))

@dataclass
class Session:
    session_id: str
    src_ip: str
    user_agent: str
    username: str
    # "human" behavior flags
    will_pageview: bool

def make_session(i: int, attacker: bool = False, ip_pool=None) -> Session:
    ip = random.choice(ip_pool) if ip_pool else (random.choice(ATTACKER_IP_POOL) if attacker else random.choice(NORMAL_IPS))
    ua = random.choice(USER_AGENTS)
    uname = random.choice(USERNAMES[:max(10, min(len(USERNAMES), BASELINE_USERS))])
    sid = f"sess-{i}-{random.randint(1000,9999)}"
    return Session(
        session_id=sid,
        src_ip=ip,
        user_agent=ua,
        username=uname,
        will_pageview=(random.random() < PAGEVIEW_RATE),
    )

def simulate_latency_ms(kind: str) -> int:
    # rough distributions
    if kind in ("spray", "brute_low", "brute_burst"):
        base = random.randint(40, 140)
    else:
        base = random.randint(60, 220)
    if random.random() < 0.04:  # occasional slow request
        base += random.randint(300, 1200)
    return base

def maybe_error_status() -> tuple[int, str]:
    # small background noise: 429/500 occasionally
    r = random.random()
    if r < 0.01:
        return 429, "rate_limited"
    if r < 0.02:
        return 500, "server_error"
    return 0, ""

# ---------- Event emitters ----------
def emit_page_hit(sess: Session, path: str, request_id: str):
    emit({
        "ts": now_rfc3339(),
        "event": "http_request",
        "method": "GET",
        "path": path,
        "status_code": 200,
        "latency_ms": simulate_latency_ms("page"),
        "username": sess.username,
        "src_ip": sess.src_ip,
        "user_agent": sess.user_agent,
        "session_id": sess.session_id,
        "request_id": request_id,
        "service": SERVICE,
        "env": ENV,
    })

def emit_auth_attempt(sess: Session, scenario: str, success: bool, reason: str, request_id: str):
    noisy_status, noisy_reason = maybe_error_status()
    if noisy_status:
        status = noisy_status
        result = "error"
        reason = noisy_reason
    else:
        status = 200 if success else 401
        result = "success" if success else "fail"

    emit({
        "ts": now_rfc3339(),
        "event": "auth_attempt",
        "result": result,
        "reason": reason,
        "status_code": status,
        "username": sess.username,
        "src_ip": sess.src_ip,
        "user_agent": sess.user_agent,
        "path": LOGIN_PATH,
        "latency_ms": simulate_latency_ms(scenario),
        "request_id": request_id,
        "session_id": sess.session_id,
        "scenario": scenario,
        "service": SERVICE,
        "env": ENV,
    })

# ---------- Mixed traffic scheduler ----------
def run_mixed(duration_s: int):
    # We create a population of "normal" sessions and reuse them over time.
    normal_sessions = [make_session(i, attacker=False) for i in range(1, 1 + BASELINE_USERS)]

    # Attackers: one IP for brute burst + rotating IPs for spray
    brute_burst_ip = ATTACKER_IP
    spray_ips = ATTACKER_IP_POOL

    start = time.time()
    end = start + duration_s
    sent = 0
    rid = 0

    emit({
        "ts": now_rfc3339(),
        "event": "traffic_gen_start",
        "mode": MODE,
        "profile": PROFILE,
        "duration_seconds": duration_s,
        "seed": SEED,
        "service": SERVICE,
        "env": ENV,
        "notes": "mixed=human baseline + password spray + brute bursts",
    })

    # Attack timing: spray runs continuously but slow; brute happens in bursts.
    next_spray = start
    next_brute_burst = start + random.randint(15, 35)

    while time.time() < end:
        now = time.time()

        # --- 1) Baseline human-ish traffic (most of the time) ---
        # choose a session; sometimes they browse first; then attempt auth
        sess = random.choice(normal_sessions)
        rid += 1
        request_id = f"tg-{rid}"
        if sess.will_pageview and random.random() < 0.25:
            emit_page_hit(sess, random.choice(PATHS_PRELOGIN), request_id + "-pv")
            jittered_sleep(mean_s=0.2, jitter=0.5)

        # normal login: mostly success, sometimes fail
        success = True
        reason = "ok"
        if random.random() < BASELINE_FAIL_RATE:
            success = False
            reason = "bad_password"

        # bias some true successes toward VALID_USERNAME so it looks like real staff user
        if success and random.random() < 0.35:
            sess.username = VALID_USERNAME

        emit_auth_attempt(sess, "human", success, reason, request_id)
        sent += 1

        # human think time between actions
        jittered_sleep(mean_s=0.35, jitter=0.8)

        # --- 2) Password spray (slow + steady) ---
        if now >= next_spray:
            rid += 1
            spray_user = random.choice(USERNAMES)
            spray_sess = Session(
                session_id=f"spray-{random.randint(1000,9999)}",
                src_ip=random.choice(spray_ips),
                user_agent=random.choice(USER_AGENTS),
                username=spray_user,
                will_pageview=False,
            )
            # spray tries 1-2 common passwords across many users; always fail in our sim
            emit_auth_attempt(spray_sess, "spray", False, "bad_password", f"tg-{rid}")
            sent += 1

            # next spray event in ~1.5–5 seconds
            next_spray = now + random.uniform(1.5, 5.0)

        # --- 3) Brute bursts (short fast spikes) ---
        if now >= next_brute_burst:
            # burst for ~8–15 seconds, at ~6–12 rps
            burst_seconds = random.uniform(8, 15)
            burst_rps = random.uniform(6, 12)
            burst_end = time.time() + burst_seconds

            while time.time() < burst_end and time.time() < end:
                rid += 1
                brute_sess = Session(
                    session_id=f"brute-{random.randint(1000,9999)}",
                    src_ip=brute_burst_ip,
                    user_agent=random.choice(USER_AGENTS),
                    username=VALID_USERNAME,
                    will_pageview=False,
                )
                emit_auth_attempt(brute_sess, "brute", False, "bad_password", f"tg-{rid}")
                sent += 1
                time.sleep(1.0 / burst_rps)

                if MAX_EVENTS and sent >= MAX_EVENTS:
                    break

            # next burst in 25–60 seconds (looks realistic)
            next_brute_burst = time.time() + random.uniform(25, 60)

        if MAX_EVENTS and sent >= MAX_EVENTS:
            break

    emit({
        "ts": now_rfc3339(),
        "event": "traffic_gen_end",
        "sent": sent,
        "service": SERVICE,
        "env": ENV,
    })

def main():
    random.seed(SEED)
    run_mixed(DURATION)

if __name__ == "__main__":
    main()