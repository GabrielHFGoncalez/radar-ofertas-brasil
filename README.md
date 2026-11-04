# 📡 Radar Ofertas Brasil — Rastreador Inteligente de Preços & Deals Tech

> **Sistema 100% Autônomo** de monitoramento de ofertas e rastreamento de quedas de preço nos maiores e-commerces do Brasil (Mercado Livre, Amazon, Magalu, Kabum).

🌐 **Aplicação Web Ao Vivo:** [https://gabrielhfgoncalez.github.io/radar-ofertas-brasil/](https://gabrielhfgoncalez.github.io/radar-ofertas-brasil/)  
📊 **Feed JSON Atualizado (API Livre):** `https://raw.githubusercontent.com/GabrielHFGoncalez/radar-ofertas-brasil/main/data/live_deals_feed.json`

---

## ⚡ Como Funciona a Autonomia

1. **GitHub Actions Cron:** A cada 6 horas (`0 */6 * * *`), um container Linux na nuvem do GitHub executa `tools/deals_radar_engine.py`.
2. **Extração Multicanal:** O script rastreia 6 categorias estratégicas de tecnologia (Notebooks, Smartphones, GPUs, Smart TVs, Monitores Gamer e Consoles).
3. **Commit Automático:** O arquivo `data/live_deals_feed.json` é atualizado e commitado automaticamente pelo bot.
4. **Deploy Serverless Instantâneo:** O GitHub Pages recompila a aplicação estática com 0 intervenção humana e $0.00 de custo de servidor.

---

## 💳 Apoio & Monetização

- **Chave Pix de Apoio:** `99f7b8c7-6dcc-494a-ab2f-fa39c51f4bcd` (Beneficiário: GABRIEL, São Paulo)
- **GitHub Sponsors:** [sponsors/GabrielHFGoncalez](https://github.com/sponsors/GabrielHFGoncalez)
- **Acesso Comercial B2B:** Feed para bots de ofertas e e-commerces por R$ 29/mês via Pix.

---

Criado e mantido de forma 100% automatizada por [@GabrielHFGoncalez](https://github.com/GabrielHFGoncalez).
