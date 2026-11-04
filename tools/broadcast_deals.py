"""
Broadcast Deals Generator for Radar Ofertas Brasil
Author: GabrielHFGoncalez
Objective: Convert top live deals into ready-to-post messages for Telegram, WhatsApp, Twitter/X and Discord
with Pix Direct Support and Affiliate links to drive immediate conversions.
"""

import json
from pathlib import Path
from datetime import datetime

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "live_deals_feed.json"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "broadcast_queue.md"

PIX_KEY = "99f7b8c7-6dcc-494a-ab2f-fa39c51f4bcd"
RADAR_URL = "https://gabrielhfgoncalez.github.io/radar-ofertas-brasil/"

def generate_broadcasts():
    if not DATA_PATH.exists():
        print(f"[-] Arquivo de ofertas nao encontrado em {DATA_PATH}")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        feed = json.load(f)

    items = feed.get("deals", [])
    if not items:
        print("[-] Nenhuma oferta no feed.")
        return

    # Filter deals with significant discount (> 15%) or top reviewed
    best_deals = sorted(items, key=lambda x: x.get("discount_pct", 0), reverse=True)[:8]

    now_str = datetime.now().strftime("%d/%m/%Y às %H:%M")
    
    content = f"# 🚀 Radar Ofertas Brasil — Pacote de Transmissão ({now_str})\n\n"
    content += f"🌐 **Acesse o radar completo em tempo real:** {RADAR_URL}\n"
    content += f"💰 **Chave Pix de Suporte:** `{PIX_KEY}`\n\n---\n\n"

    # 1. Telegram / WhatsApp Format
    content += "## 📱 1. Formato Telegram / WhatsApp / Grupos VIP\n\n```text\n"
    content += f"🔥 TOP OFERTAS TECH DO DIA — {now_str}\n"
    content += "Radar autônomo monitorando quedas reais de preço:\n\n"
    for idx, d in enumerate(best_deals, 1):
        title = d.get("title", "")[:60]
        price = f"R$ {d.get('current_price', 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        old_price = f"R$ {d.get('original_price', 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if d.get("original_price") else ""
        disc = f" (-{d.get('discount_pct')}%)" if d.get("discount_pct") else ""
        link = d.get("url", "")
        
        content += f"{idx}️⃣ {title}\n"
        if old_price:
            content += f"   De: ~{old_price}~ por APENAS: {price}{disc}\n"
        else:
            content += f"   Preço: {price}\n"
        content += f"   🔗 Link: {link}\n\n"
    
    content += f"⚡ Mais de 40 ofertas atualizadas em tempo real:\n👉 {RADAR_URL}\n"
    content += f"\n💡 Gosta do nosso serviço gratuito? Apoie com qualquer Pix: {PIX_KEY}\n"
    content += "```\n\n---\n\n"

    # 2. Twitter / X Thread Format
    content += "## 🐦 2. Formato Twitter / X Post Curto\n\n```text\n"
    content += f"🚨 Radar de Descontos Tech atualizado ({now_str})!\n\n"
    for d in best_deals[:3]:
        title = d.get("title", "")[:45]
        price = f"R$ {d.get('current_price', 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        disc = f" | {d.get('discount_pct')}% OFF" if d.get("discount_pct") else ""
        content += f"📦 {title}\n💰 {price}{disc}\n🔗 {d.get('url')}\n\n"
    content += f"Veja o radar completo sem anúncios: {RADAR_URL} 🚀\n"
    content += "```\n"

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[+] Transmissões geradas com sucesso em: {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_broadcasts()
