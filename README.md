# ⚓ Amiral Support Bot

Telegram destek sistemi + Flask yönetim paneli. Kullanıcı Telegram botuna `/start`
der, temsilci listesini görür, seçtiği temsilcinin WhatsApp sohbetine yönlenir.
Tüm temsilci yönetimi web panelinden yapılır.

## Özellikler

- 🤖 **Telegram bot** — temsilci seç → `wa.me` yönlendirme
- 🖥️ **SaaS yönetim paneli** — sidebar, dashboard, temsilci kartları
- 🔐 **Admin login** — hash'li parola (werkzeug), session tabanlı
- ⚡ **Anlık online/offline toggle** — kart üzerinde tek tık
- ✋ **Sürükle-bırak sıralama**
- 🔍 Canlı arama + online/offline filtre
- 📱 Responsive / mobil uyumlu

## Teknoloji

Python 3 · Flask · python-telegram-bot · SQLite · Jinja2 · vanilla CSS/JS

## Kurulum

```bash
git clone <repo>
cd tg-whatsapp-bot

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # değerleri doldur (aşağıya bak)
```

### .env ayarları

| Değişken | Açıklama |
|---|---|
| `BOT_TOKEN` | BotFather'dan alınan token |
| `PANEL_SECRET_KEY` | Flask oturum anahtarı — `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ADMIN_USERNAME` | Panel kullanıcı adı (varsayılan `admin`) |
| `ADMIN_PASSWORD_HASH` | Parola **hash'i** — `python -c "from werkzeug.security import generate_password_hash as g; print(g('yeni-sifre'))"` |

## Çalıştırma

```bash
python panel.py     # panel → http://127.0.0.1:5000  (varsayılan giriş: admin / admin123)
python bot.py       # Telegram botu (ayrı terminal)
```

Panel ve bot **aynı `database.db`** dosyasını paylaşır; panelden yapılan değişiklik
bota anında yansır.

## Canlıya Alma (Deploy)

> ⚠️ **Netlify kullanılamaz.** Netlify yalnızca statik site barındırır; Flask sunucusu,
> SQLite ve 7/24 çalışan bot Netlify'da **çalışmaz**. Python'u çalıştıran bir platform gerekir.

**Önerilen: [Render](https://render.com) (ücretsiz, Python 7/24)**

Panel'i canlıya alıp public link almak için repo'daki [`render.yaml`](render.yaml) hazır:
Render → *New → Blueprint* → repo'yu bağla → `ADMIN_PASSWORD_HASH`'i gir → deploy.

### Bot + veritabanı notu

Panel (web) ve bot (worker) **aynı** veritabanına bağlanmalı. İki ayrı Render servisi
SQLite dosyasını paylaşamaz. Seçenekler:

1. **Şimdilik:** sadece paneli Render'a al (link için), botu kendi bilgisayarında/VPS'te çalıştır.
2. **Kalıcı (v3.0.0):** SQLite → **PostgreSQL** — panel ve bot aynı hosted DB'ye bağlanır,
   bot webhook moduna geçer. Bkz. [ROADMAP.md](ROADMAP.md).

## Proje Yapısı

```
bot.py                  Telegram bot
panel.py                Flask panel + auth + route'lar
services/database.py    SQLite katmanı (CRUD + migration)
templates/              base, login, dashboard, representatives, settings
static/css/style.css    SaaS tasarım sistemi
static/js/app.js        modal, toggle, sürükle-bırak, arama/filtre
```

Yol haritası için [ROADMAP.md](ROADMAP.md).
