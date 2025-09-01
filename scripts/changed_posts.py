#!/usr/bin/env python3
"""
Git Changes Detection Script
Detects changed blog posts based on git diff.
"""
import subprocess
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_changed_posts():
    """
    Get list of changed blog post slugs from git diff.
    
    Returns:
        list: List of changed post slugs
    """
    try:
        # Look at last commit range; fallback to HEAD if shallow
        try:
            diff = subprocess.check_output(
                ["git", "diff", "--name-only", "HEAD~1", "HEAD"], 
                text=True,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            # Fallback for shallow repositories
            diff = subprocess.check_output(
                ["git", "show", "--name-only", "--pretty="], 
                text=True,
                stderr=subprocess.DEVNULL
            )
    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {e}")
        return []
    except FileNotFoundError:
        logger.error("Git not found in PATH")
        return []

    changed = set()
    for line in diff.splitlines():
        if line.startswith("posts/") and (
            line.endswith("/index.html") or line.endswith("/meta.json")
        ):
            parts = line.split("/")
            if len(parts) >= 3:
                changed.add(parts[1])

    return sorted(changed)


if __name__ == "__main__":
    changed_posts = get_changed_posts()
    print(json.dumps(changed_posts))
    
    if changed_posts:
        logger.info(f"Detected {len(changed_posts)} changed posts: {', '.join(changed_posts)}")
    else:
        logger.info("No changed posts detected")
