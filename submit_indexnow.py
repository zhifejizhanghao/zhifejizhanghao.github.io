import json
import os
import urllib.request
import urllib.error

BASE_URL = os.environ.get("BASE_URL", "https://zhifejizhanghao.github.io")
KEY = os.environ.get("INDEXNOW_KEY", "4a38f28dc5714ebea70c452cdd7003d6")
HOST = "zhifejizhanghao.github.io"

with open("/tmp/url_list.json", encoding="utf-8") as f:
    urls = json.load(f)

if not urls:
    print("No URLs to submit.")
    raise SystemExit(0)

payload = {
    "host": HOST,
    "key": KEY,
    "keyLocation": f"{BASE_URL}/{KEY}.txt",
    "urlList": urls,
}
body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

print(f"Submitting {len(urls)} URLs to IndexNow...")
for u in urls:
    print("  -", u)

req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=body,
    headers={"Content-Type": "application/json; charset=utf-8"},
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        code = resp.status
        print(f"HTTP {code}")
        if code not in (200, 202):
            print("Unexpected status from IndexNow")
            raise SystemExit(1)
except urllib.error.HTTPError as e:
    print(f"HTTPError {e.code}: {e.reason}")
    print(e.read().decode("utf-8", "replace")[:1000])
    raise SystemExit(1)

print("IndexNow submission complete.")
