#!/usr/bin/env python3
"""
Telegram Bot Post Script
Posts blog content to Telegram channel with images.
"""

import json
import logging
import os
import pathlib
import sys

import requests

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

try:
    BOT = os.environ["TELEGRAM_BOT_TOKEN"]
    CHAT = os.environ["TELEGRAM_CHAT_ID"]
except KeyError as e:
    logger.error(f"Missing required environment variable: {e}")
    sys.exit(1)

ROOT = pathlib.Path(__file__).resolve().parents[1]


def post_slug(slug: str) -> bool:
    """
    Post a blog post to Telegram channel.

    Args:
        slug: The blog post slug/directory name

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        meta_path = ROOT / "posts" / slug / "meta.json"

        if not meta_path.exists():
            logger.error(f"Meta file not found: {meta_path}")
            return False

        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in meta file {meta_path}: {e}")
            return False

        image_filename = meta.get("image", "cover.png")
        img_path = ROOT / "posts" / slug / image_filename

        if not img_path.exists():
            logger.error(f"Image file not found: {img_path}")
            return False

        url = f"/posts/{slug}/"
        caption = meta.get("telegram_message") or f"{meta['title']}\n{url}"

        with open(img_path, "rb") as f:
            response = requests.post(
                f"https://api.telegram.org/bot{BOT}/sendPhoto",
                data={"chat_id": CHAT, "caption": caption},
                files={"photo": f},
                timeout=30,
            )

        response.raise_for_status()
        logger.info(f"Successfully posted {slug} to Telegram")
        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to post {slug} to Telegram: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error posting {slug}: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.info("No slugs provided; nothing to post.")
        sys.exit(0)

    success_count = 0
    total_count = len(sys.argv[1:])

    for slug in sys.argv[1:]:
        if post_slug(slug):
            success_count += 1

    logger.info(f"Posted {success_count}/{total_count} posts successfully")

    if success_count < total_count:
        sys.exit(1)
