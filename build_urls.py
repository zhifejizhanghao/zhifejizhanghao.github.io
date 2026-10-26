"""Collect IndexNow URLs for posts published today only.

Rule (per user): only submit articles whose publish date is TODAY.
- On push: look at _posts/*.md changed in the last commit, keep those whose
  filename date prefix (YYYY-MM-DD-) equals today's date (Asia/Shanghai).
- On workflow_dispatch: same filter applied to all tracked _posts files.
Historical posts, edited old posts, and full-sitemap dumps are never submitted.
"""

import json
import os
import re
import subprocess
from datetime import datetime, timezone, timedelta

BASE_URL = os.environ.get("BASE_URL", "https://zhifejizhanghao.github.io")
CST = timezone(timedelta(hours=8))


def today_str() -> str:
    return datetime.now(CST).strftime("%Y-%m-%d")


def list_changed_posts() -> list:
    event = os.environ.get("GITHUB_EVENT_NAME", "push")
    if event == "workflow_dispatch":
        cmd = ["git", "ls-files", "_posts/*.md"]
    else:
        cmd = [
            "git", "diff", "--name-only", "--diff-filter=AM",
            "HEAD^", "HEAD", "--", "_posts/*.md",
        ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("git command failed:", e)
        return []
    return [f for f in result.stdout.strip().split("\n") if f]


def post_date_of(path: str):
    """Return YYYY-MM-DD for a post: front-matter date first, filename prefix as fallback."""
    name = os.path.basename(path)
    m = re.match(r"(\d{4}-\d{2}-\d{2})-", name)
    if m:
        return m.group(1)
    try:
        with open(path, encoding="utf-8") as fh:
            head = fh.read(2000)
    except OSError:
        return None
    m = re.search(r"^date:\s*['\"]?(\d{4}-\d{2}-\d{2})", head, re.M)
    return m.group(1) if m else None


def url_of(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return ""
    m = re.search(r"permalink:\s*(\S+)", text)
    if m:
        perm = m.group(1).strip().strip("'\"")
        return BASE_URL + perm if perm.startswith("/") else BASE_URL + "/" + perm
    slug = os.path.basename(path)[:-3]
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug)
    return f"{BASE_URL}/articles/{slug}/"


def main() -> None:
    today = today_str()
    print(f"Today (Asia/Shanghai): {today}")

    files = list_changed_posts()
    print(f"Changed post files: {len(files)}")

    urls = []
    for f in files:
        if not f or not os.path.isfile(f):
            continue
        d = post_date_of(f)
        if d != today:
            print(f"SKIP (date {d} != {today}): {f}")
            continue
        u = url_of(f)
        if u and u not in urls:
            urls.append(u)
            print(f"ADD: {u}")

    urls = urls[:50]
    with open("/tmp/url_list.json", "w", encoding="utf-8") as out:
        json.dump(urls, out)
    print(f"TODAY_URL_COUNT={len(urls)}")


if __name__ == "__main__":
    main()
