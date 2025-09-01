#!/usr/bin/env python3
"""
Blog Validation Script
Validates blog post structure and metadata.
"""
import json
import pathlib
import datetime
import sys
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ROOT = pathlib.Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "posts"


def validate_post(post_dir: pathlib.Path) -> Dict[str, Any]:
    """
    Validate a single blog post directory.
    
    Args:
        post_dir: Path to the post directory
        
    Returns:
        Dictionary with validation results
    """
    errors = []
    warnings = []
    slug = post_dir.name
    
    meta_file = post_dir / "meta.json"
    index_file = post_dir / "index.html"
    
    if not meta_file.exists():
        errors.append("Missing meta.json")
        return {"slug": slug, "errors": errors, "warnings": warnings}
    
    if not index_file.exists():
        errors.append("Missing index.html")
    
    try:
        with open(meta_file, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in meta.json: {e}")
        return {"slug": slug, "errors": errors, "warnings": warnings}
    
    required_fields = ["title", "date"]
    for field in required_fields:
        if field not in meta:
            errors.append(f"Missing required field '{field}' in meta.json")
    
    if "date" in meta:
        try:
            datetime.datetime.strptime(meta["date"], "%Y-%m-%d")
        except ValueError:
            errors.append(f"Invalid date format '{meta['date']}' (expected YYYY-MM-DD)")
    
    image_filename = meta.get("image", "cover.png")
    image_file = post_dir / image_filename
    if not image_file.exists():
        warnings.append(f"Missing image file: {image_filename}")
    
    if "title" in meta and len(meta["title"]) > 100:
        warnings.append("Title is very long (>100 characters)")
    
    if "description" in meta and len(meta["description"]) > 200:
        warnings.append("Description is very long (>200 characters)")
    
    if index_file.exists() and index_file.stat().st_size == 0:
        errors.append("index.html is empty")
    
    return {"slug": slug, "errors": errors, "warnings": warnings}


def validate_all_posts() -> bool:
    """
    Validate all blog posts.
    
    Returns:
        True if all posts are valid, False otherwise
    """
    if not POSTS_DIR.exists():
        logger.error(f"Posts directory not found: {POSTS_DIR}")
        return False
    
    post_dirs = [d for d in POSTS_DIR.iterdir() if d.is_dir()]
    
    if not post_dirs:
        logger.warning("No post directories found")
        return True
    
    all_valid = True
    
    for post_dir in post_dirs:
        result = validate_post(post_dir)
        
        if result["errors"]:
            all_valid = False
            logger.error(f"❌ {result['slug']}: {', '.join(result['errors'])}")
        
        if result["warnings"]:
            logger.warning(f"⚠️  {result['slug']}: {', '.join(result['warnings'])}")
        
        if not result["errors"] and not result["warnings"]:
            logger.info(f"✅ {result['slug']}: Valid")
    
    return all_valid


if __name__ == "__main__":
    logger.info("Starting blog validation...")
    
    if validate_all_posts():
        logger.info("✅ All posts are valid!")
        sys.exit(0)
    else:
        logger.error("❌ Some posts have errors!")
        sys.exit(1)
