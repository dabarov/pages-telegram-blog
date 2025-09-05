#!/usr/bin/env python3
"""
Static Site Builder
Builds index.html, RSS feed, and sitemap from blog posts.
"""

import datetime
import html
import json
import logging
import pathlib
import xml.etree.ElementTree as ET
from typing import Any

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

ROOT = pathlib.Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "posts"
SITE_DESC = "Minimal static blog with GitHub Actions cross-posting to Telegram."


def load_posts() -> list[dict[str, Any]]:
    """
    Load and validate all blog posts from the posts directory.

    Returns:
        List of post dictionaries sorted by date (newest first)
    """
    items = []

    for meta_file in POSTS_DIR.glob("*/meta.json"):
        try:
            data = json.loads(meta_file.read_text(encoding="utf-8"))
            slug = meta_file.parent.name

            required_fields = ["title", "date"]
            for field in required_fields:
                if field not in data:
                    logger.error(f"Missing required field '{field}' in {meta_file}")
                    continue

            try:
                datetime.datetime.strptime(data["date"], "%Y-%m-%d")
            except ValueError:
                logger.error(f"Invalid date format in {meta_file}: {data['date']}")
                continue

            if not (meta_file.parent / "index.html").exists():
                logger.warning(f"Missing index.html for post: {slug}")

            image_file = data.get("image", "cover.png")
            if not (meta_file.parent / image_file).exists():
                logger.warning(f"Missing image file {image_file} for post: {slug}")

            items.append(
                {
                    "slug": slug,
                    "title": data["title"],
                    "desc": data.get("description", ""),
                    "date": data["date"],
                    "image": image_file,
                }
            )

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {meta_file}: {e}")
            continue
        except Exception as e:
            logger.error(f"Error processing {meta_file}: {e}")
            continue

    items.sort(key=lambda x: x["date"], reverse=True)
    logger.info(f"Loaded {len(items)} valid posts")
    return items


def render_index(posts: list[dict[str, Any]]) -> str:
    """
    Render the main index.html page.

    Args:
        posts: List of post dictionaries

    Returns:
        HTML string for the index page
    """
    cards = "\n".join(
        f"""      <article class="card">
        <a href="posts/{p["slug"]}/">
          <img src="posts/{p["slug"]}/{p["image"]}" alt="">
          <h2>{html.escape(p["title"])}</h2>
          <p>{html.escape(p["desc"])}</p>
          <p class="date">{p["date"]}</p>
        </a>
      </article>"""
        for p in posts
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>My Blog</title>
  <meta name="description" content="{html.escape(SITE_DESC)}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta property="og:type" content="website">
  <meta property="og:title" content="My Blog">
  <meta property="og:image" content="assets/img/og-default.png">
  <link rel="stylesheet" href="assets/css/site.css">
  <link rel="alternate" type="application/rss+xml" title="RSS" href="feed.xml">
</head>
<body>
  <header>
    <h1><a href="./">My Blog</a></h1>
    <nav>
      <a href="feed.xml">RSS</a>
      <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme" title="Toggle theme">🌙</button>
    </nav>
  </header>
  <script src="assets/js/theme.js"></script>
  <main>
    <section class="grid">
{cards}
    </section>
  </main>
  <footer>© {datetime.date.today().year} · RSS: <a href="feed.xml">feed.xml</a></footer>
</body>
</html>"""


def write_feed(posts: list[dict[str, Any]]) -> None:
    """
    Generate RSS feed XML file.

    Args:
        posts: List of post dictionaries
    """
    rss = ET.Element("rss", attrib={"version": "2.0"})
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "My Blog"
    ET.SubElement(channel, "link").text = "/"
    ET.SubElement(channel, "description").text = SITE_DESC
    for p in posts:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = p["title"]
        ET.SubElement(item, "link").text = f"/posts/{p['slug']}/"
        guid = ET.SubElement(item, "guid", attrib={"isPermaLink": "true"})
        guid.text = f"/posts/{p['slug']}/"
        yyyy, mm, dd = p["date"].split("-")
        dt = datetime.datetime(int(yyyy), int(mm), int(dd))
        ET.SubElement(item, "pubDate").text = dt.strftime("%a, %d %b %Y 00:00:00 +0000")
        ET.SubElement(item, "description").text = p["desc"]
    xml = ET.tostring(rss, encoding="utf-8", xml_declaration=True)
    (ROOT / "feed.xml").write_bytes(xml)


def write_sitemap(posts: list[dict[str, Any]]) -> None:
    """
    Generate sitemap.xml file.

    Args:
        posts: List of post dictionaries
    """
    urlset = ET.Element(
        "urlset", attrib={"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    )

    def add(loc: str) -> None:
        u = ET.SubElement(urlset, "url")
        ET.SubElement(u, "loc").text = loc

    add("/")
    for p in posts:
        add(f"/posts/{p['slug']}/")
    xml = ET.tostring(urlset, encoding="utf-8", xml_declaration=True)
    (ROOT / "sitemap.xml").write_bytes(xml)


def main() -> None:
    """Main function to build all site files."""
    try:
        posts = load_posts()

        if not posts:
            logger.warning("No valid posts found!")

        index_path = ROOT / "index.html"
        index_html = render_index(posts)
        # Normalize line endings to LF to satisfy mixed-line-ending hook
        index_html = index_html.replace("\r\n", "\n").replace("\r", "\n")
        with open(index_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(index_html)
        logger.info(f"Generated {index_path}")

        write_feed(posts)
        logger.info(f"Generated {ROOT / 'feed.xml'}")

        write_sitemap(posts)
        logger.info(f"Generated {ROOT / 'sitemap.xml'}")

    except Exception as e:
        logger.error(f"Build failed: {e}")
        raise


if __name__ == "__main__":
    main()
