
import os
import re
import subprocess
import json
import urllib.request
from datetime import datetime

def build_urls():
    base = os.environ.get("BASE_URL", "https://zhifejizhanghao.github.io")
    
    # 1. Get changed _posts/*.md from last commit (or all if workflow_dispatch)
    event = os.environ.get("GITHUB_EVENT_NAME", "push")
    files = []
    if event == "workflow_dispatch":
        try:
            result = subprocess.run(["git", "ls-files", "_posts/*.md"], capture_output=True, text=True, check=True)
            files = [f for f in result.stdout.strip().split("\n") if f]
        except subprocess.CalledProcessError as e:
            print("Error listing files:", e)
            return []
    else:
        try:
            result = subprocess.run(["git", "diff", "--name-only", "--diff-filter=AM", "HEAD^", "HEAD", "--", "_posts/*.md"], capture_output=True, text=True, check=True)
            files = [f for f in result.stdout.strip().split("\n") if f]
        except subprocess.CalledProcessError as e:
            print("Error diffing files:", e)
            return []

    urls = []
    for f in files:
        if not os.path.isfile(f):
            continue
        try:
            with open(f, encoding="utf-8") as text:
                text_content = text.read()
                m = re.search(r"permalink:\s*(\S+)", text_content)
                if m:
                    url = base + m.group(1)
                else:
                    slug = os.path.basename(f).replace(".md", "")
                    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug)
                    url = base + "/articles/" + slug + "/"
                
                if url not in urls:
                    urls.append(url)
                    print("Post add:", url)
        except Exception as e:
            print(f"Error processing {f}: {e}")
            
    # 2. Sitemap fallback (live)
    try:
        with urllib.request.urlopen(base + "/sitemap.xml", timeout=15) as resp:
            sitemap = resp.read().decode("utf-8")
        for match in re.findall(r"https://[^<]+", sitemap):
            if "/articles/" in match and match not in urls:
                urls.append(match)
                print("Sitemap add:", match)
    except Exception as e:
        print("Sitemap fetch failed:", e)

    # 3. Cap and return
    urls = urls[:50]
    return urls

if __name__ == "__main__":
    url_list = build_urls()
    with open("/tmp/url_list.json", "w") as out:
        json.dump(url_list, out)
    print(f"Total unique URLs: {len(url_list)}")
