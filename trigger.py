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
INTERVAL_SECONDS = 5 * 3600 + 50 * 60
KST = timezone(timedelta(hours=9))
USE_KST_ANCHOR = os.environ.get("USE_KST_ANCHOR", "false").lower() == "true"


def next_fire_time_anchored() -> datetime:
    current = datetime.now(KST)
    anchor = current.replace(hour=10, minute=0, second=0, microsecond=0)

    if current < anchor:
        return anchor

    elapsed = (current - anchor).total_seconds()
    periods_passed = int(elapsed // INTERVAL_SECONDS) + 1
    return anchor + timedelta(seconds=INTERVAL_SECONDS * periods_passed)


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
    if USE_KST_ANCHOR:
        target = next_fire_time_anchored()
        logger.info("KST anchor mode: first trigger at %s KST", target.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        target = datetime.now(KST) + timedelta(seconds=INTERVAL_SECONDS)
        logger.info("Immediate mode: first trigger at %s KST", target.strftime("%Y-%m-%d %H:%M:%S"))

    while True:
        now = datetime.now(KST)
        wait = (target - now).total_seconds()
        if wait > 0:
            logger.info("Sleeping %.1fs until %s KST", wait, target.strftime("%H:%M:%S"))
            time.sleep(int(wait))

        fire()
        target = target + timedelta(seconds=INTERVAL_SECONDS)
        logger.info("Next trigger at %s KST", target.strftime("%Y-%m-%d %H:%M:%S"))