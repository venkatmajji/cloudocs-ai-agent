import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from urllib.parse import urljoin, urlparse
from tqdm import tqdm
import json
import time
import os

# Optional: For emoji-safe output on Windows
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Base domain
BASE_URL = "https://learn.microsoft.com"
START_PATH = "/en-us/azure/key-vault/general/basic-concepts"

# Azure Services to crawl
ALLOWED_SERVICES = [
    "/en-us/azure/key-vault/",
    "/en-us/azure/app-service/",
    "/en-us/azure/storage/",
    "/en-us/azure/aks/",
    "/en-us/azure/azure-functions/",
    "/en-us/azure/ai-services/"
]

SERVICE_MAP = {
    "/en-us/azure/key-vault/": "key-vault",
    "/en-us/azure/app-service/": "app-service",
    "/en-us/azure/storage/": "storage",
    "/en-us/azure/aks/": "aks",
    "/en-us/azure/azure-functions/": "azure-functions",
    "/en-us/azure/ai-services/": "ai-services"
}

visited = set()
collected_docs = []

def is_valid_link(link):
    parsed = urlparse(link)
    path = parsed.path
    if not any(path.startswith(service) for service in ALLOWED_SERVICES):
        return False
    if any(x in link for x in ["mailto:", ".pdf", "#"]):
        return False
    return True

def get_service_tag(url):
    for prefix, tag in SERVICE_MAP.items():
        if prefix in url:
            return tag
    return "unknown"

def scrape_page(full_url):
    try:
        res = requests.get(full_url, timeout=10)
        if res.status_code != 200:
            print(f"❌ Failed to fetch {full_url}")
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        title_tag = soup.find("h1")
        content_blocks = soup.find_all(["p", "h2", "h3", "pre", "ul", "ol"])
        content = "\n\n".join(md(str(tag)) for tag in content_blocks)

        service_tag = get_service_tag(full_url)

        return {
            "title": title_tag.get_text(strip=True) if title_tag else "No Title",
            "url": full_url,
            "service": service_tag,
            "content": content,
        }

    except Exception as e:
        print(f"❌ Error scraping {full_url}: {e}")
        return None

def crawl(start_path, max_pages=100):
    queue = [start_path]
    print(f"[INFO] Starting crawl from {BASE_URL}{start_path}\n")

    with tqdm(total=max_pages) as pbar:
        while queue and len(visited) < max_pages:
            current = queue.pop(0)
            full_url = urljoin(BASE_URL, current)
            if full_url in visited:
                continue

            visited.add(full_url)
            print(f"[INFO] Crawling: {full_url}")

            doc = scrape_page(full_url)
            if doc:
                collected_docs.append(doc)
                pbar.update(1)

            try:
                soup = BeautifulSoup(requests.get(full_url).text, 'html.parser')
                for a_tag in soup.find_all("a", href=True):
                    href = a_tag['href']
                    href = href.split("?")[0].split("#")[0]  # Clean
                    normalized_href = urljoin(current, href)

                    if is_valid_link(normalized_href):
                        if normalized_href not in visited and normalized_href not in queue:
                            queue.append(normalized_href)
            except Exception as e:
                print(f"⚠️ Error parsing links on {full_url}: {e}")

            time.sleep(1)

    os.makedirs("../docs", exist_ok=True)
    with open("../docs/azure_core_docs.json", "w", encoding="utf-8") as f:
        json.dump(collected_docs, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Crawl complete. Total pages scraped: {len(collected_docs)}")

if __name__ == "__main__":
    crawl(start_path=START_PATH, max_pages=100)
