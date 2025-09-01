#!/usr/bin/env python3
"""
Health Check Script
Performs basic health checks on the blog system.
"""

import logging
import pathlib
import sys

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

ROOT = pathlib.Path(__file__).resolve().parents[1]


def check_file_exists(file_path: pathlib.Path, description: str) -> bool:
    """Check if a file exists and log the result."""
    if file_path.exists():
        logger.info(f"✅ {description}: {file_path}")
        return True
    else:
        logger.error(f"❌ {description}: {file_path} (missing)")
        return False


def check_directory_exists(dir_path: pathlib.Path, description: str) -> bool:
    """Check if a directory exists and log the result."""
    if dir_path.exists() and dir_path.is_dir():
        logger.info(f"✅ {description}: {dir_path}")
        return True
    else:
        logger.error(f"❌ {description}: {dir_path} (missing)")
        return False


def health_check() -> bool:
    """
    Perform comprehensive health check.

    Returns:
        True if all checks pass, False otherwise
    """
    logger.info("Starting health check...")

    all_checks_passed = True

    required_files = [
        (ROOT / "index.html", "Main index page"),
        (ROOT / "feed.xml", "RSS feed"),
        (ROOT / "sitemap.xml", "Sitemap"),
        (ROOT / "robots.txt", "Robots.txt"),
        (ROOT / "assets" / "css" / "site.css", "Site CSS"),
        (ROOT / "requirements.txt", "Python requirements"),
    ]

    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False

    required_dirs = [
        (ROOT / "posts", "Posts directory"),
        (ROOT / "assets", "Assets directory"),
        (ROOT / "scripts", "Scripts directory"),
        (ROOT / ".github" / "workflows", "GitHub workflows"),
    ]

    for dir_path, description in required_dirs:
        if not check_directory_exists(dir_path, description):
            all_checks_passed = False

    posts_dir = ROOT / "posts"
    if posts_dir.exists():
        post_count = len(list(posts_dir.glob("*/")))
        logger.info(f"📝 Found {post_count} blog posts")

        if post_count == 0:
            logger.warning("⚠️  No blog posts found")

    scripts = [
        ROOT / "scripts" / "build_index.py",
        ROOT / "scripts" / "changed_posts.py",
        ROOT / "scripts" / "telegram_post.py",
        ROOT / "scripts" / "validate.py",
    ]

    for script in scripts:
        if script.exists():
            logger.info(f"🐍 Script available: {script.name}")
        else:
            logger.error(f"❌ Missing script: {script.name}")
            all_checks_passed = False

    return all_checks_passed


if __name__ == "__main__":
    if health_check():
        logger.info("✅ All health checks passed!")
        sys.exit(0)
    else:
        logger.error("❌ Some health checks failed!")
        sys.exit(1)
