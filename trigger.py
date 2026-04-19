import os
import time
import logging
from datetime import datetime, timezone, timedelta
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

TRIGGER_URL = os.environ["TRIGGER_URL"]
TRIGGER_TOKEN = os.environ["TRIGGER_TOKEN"]
KST = timezone(timedelta(hours=9))
SCHEDULED_TIMES = (
    (7, 5),
    (12, 5),
    (17, 5),
    (22, 3),
)


def next_fire_time(current: datetime) -> datetime:
    candidate_day = current
    for _ in range(8):
        if candidate_day.weekday() != 5:
            for hour, minute in SCHEDULED_TIMES:
                candidate = candidate_day.replace(hour=hour, minute=minute, second=0, microsecond=0)
                if current < candidate:
                    return candidate
        candidate_day = (candidate_day + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    raise RuntimeError("Could not find a valid fire time")


def fire():
    headers = {
        "Authorization": f"Bearer {TRIGGER_TOKEN}",
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "experimental-cc-routine-2026-04-01",
        "Content-Type": "application/json",
    }
    payload = {"text": "optional extra turn appended to the session"}

    try:
        resp = requests.post(TRIGGER_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        logger.info("Triggered successfully: %s", resp.status_code)
    except requests.RequestException as e:
        logger.error("Trigger failed: %s", e)


if __name__ == "__main__":
    target = next_fire_time(datetime.now(KST))
    logger.info("Fixed KST schedule mode: first trigger at %s KST", target.strftime("%Y-%m-%d %H:%M:%S"))

    while True:
        now = datetime.now(KST)
        wait = (target - now).total_seconds()
        if wait > 0:
            logger.info("Sleeping %.1fs until %s KST", wait, target.strftime("%H:%M:%S"))
            time.sleep(max(1, wait))

        fire()
        target = next_fire_time(datetime.now(KST))
        logger.info("Next trigger at %s KST", target.strftime("%Y-%m-%d %H:%M:%S"))
