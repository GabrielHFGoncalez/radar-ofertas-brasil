import httpx
from bs4 import BeautifulSoup
import re
import json
import datetime
from pathlib import Path

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

CATEGORIES = [
    {"slug": "notebook", "name": "Notebooks & Laptops", "icon": "laptop"},
    {"slug": "smartphone", "name": "Smartphones & Celulares", "icon": "smartphone"},
    {"slug": "placa-de-video", "name": "Placas de Vídeo (GPUs)", "icon": "cpu"},
    {"slug": "smart-tv", "name": "Smart TVs", "icon": "tv"},
    {"slug": "monitor-gamer", "name": "Monitores Gamer", "icon": "monitor"},
    {"slug": "console-de-video-game", "name": "Consoles & Games", "icon": "gamepad-2"}
]

def clean_price_val(price_str: str):
    if not price_str:
        return None
    cleaned = re.sub(r"[^\d,\.]", "", price_str)
    if not cleaned:
        return None
    if "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    elif cleaned.count(".") > 1:
        parts = cleaned.split(".")
        cleaned = "".join(parts[:-1]) + "." + parts[-1]
    try:
        return float(cleaned)
    except ValueError:
        return None

def scrape_category(slug: str, cat_name: str, limit: int = 15):
    url = f"https://www.buscape.com.br/search?q={slug}"
    print(f"[*] Scraping category: {cat_name} ({url})...")
    try:
        r = httpx.get(url, headers=HEADERS, follow_redirects=True, timeout=12)
        if r.status_code != 200:
            print(f"[!] Warning: HTTP {r.status_code} for {slug}")
            return []
        
        soup = BeautifulSoup(r.text, 'html.parser')
        articles = soup.find_all('article', class_=re.compile(r'Root_OrqProductCard'))
        items = []
        for art in articles[:limit]:
            a_tag = art.find('a', class_=re.compile(r'ClickableArea'))
            if not a_tag:
                continue
            h2 = a_tag.find('h2')
            title = h2.get_text(strip=True) if h2 else ''
            href = a_tag.get('href', '')
            link = f"https://www.buscape.com.br{href}" if href.startswith('/') else href
            
            price_tag = art.find('strong')
            price_str = price_tag.get_text(strip=True) if price_tag else ''
            price_float = clean_price_val(price_str)
            
            img = art.find('img')
            img_url = img.get('src') if img else ''
            if not img_url and img:
                img_url = img.get('data-src', '')
                
            rating_tag = art.find('span', class_=re.compile(r'Rating'))
            rating = rating_tag.get_text(strip=True) if rating_tag else None
            
            if title and price_float:
                items.append({
                    "id": f"{slug}_{len(items)+1}",
                    "category": cat_name,
                    "category_slug": slug,
                    "title": title,
                    "price_str": price_str,
                    "price": price_float,
                    "url": link,
                    "image_url": img_url or "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&auto=format&fit=crop&q=60",
                    "rating": rating,
                    "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
                })
        print(f"    -> Extracted {len(items)} products.")
        return items
    except Exception as e:
        print(f"[!] Error scraping {slug}: {e}")
        return []

def run_radar():
    all_products = []
    for cat in CATEGORIES:
        prods = scrape_category(cat["slug"], cat["name"], limit=12)
        all_products.extend(prods)
        
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    feed_path = out_dir / "live_deals_feed.json"
    
    feed_data = {
        "status": "success",
        "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_deals": len(all_products),
        "categories": [c["name"] for c in CATEGORIES],
        "deals": all_products
    }
    
    with open(feed_path, "w", encoding="utf-8") as f:
        json.dump(feed_data, f, indent=2, ensure_ascii=False)
        
    print(f"\n[+] SUCCESS! Total {len(all_products)} products saved to {feed_path}")
    return feed_data

if __name__ == "__main__":
    run_radar()
