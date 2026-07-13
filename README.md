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
- 🔍 Canlı arama + online/offline filtre · 📱 Responsive

## Teknoloji

Python 3 · Flask · python-telegram-bot (local) · SQLite · Jinja2 · vanilla CSS/JS

## Mimari — İki mod

Bot iki şekilde çalışabilir; ikisi de **aynı** `database.db`'yi kullanır:

| Mod | Ne zaman | Nasıl |
|---|---|---|
| **Polling** | Local geliştirme | `python bot.py` (ayrı process, python-telegram-bot) |
| **Webhook** | Canlı / production | Telegram, panelin `/webhook/<token>` route'una POST eder. Bot + panel **tek uygulama**, tek DB. |

> Production'da bot ve panel tek serviste çalışır → SQLite paylaşımı sorunsuz olur.

## Kurulum (local)

```bash
git clone <repo> && cd tg-whatsapp-bot
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # değerleri doldur (aşağıda)
```

### .env

| Değişken | Açıklama |
|---|---|
| `BOT_TOKEN` | BotFather token'ı |
| `PANEL_SECRET_KEY` | `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ADMIN_USERNAME` | Panel kullanıcı adı (varsayılan `admin`) |
| `ADMIN_PASSWORD_HASH` | `python -c "from werkzeug.security import generate_password_hash as g; print(g('yeni-sifre'))"` |

### Çalıştırma (local)

```bash
python panel.py     # panel → http://127.0.0.1:5000  (giriş: admin / admin123)
python bot.py       # bot (polling)  — ayrı terminal
```

> Not: Canlıda webhook kurduysan, local polling güncelleme alamaz.
> Local test için önce `python set_webhook.py delete` ile webhook'u kaldır.

---

## 🚀 Canlıya Alma — PythonAnywhere (ücretsiz, kartsız, 7/24)

> ⚠️ Netlify/Render **değil**. Netlify Flask çalıştıramaz; Render kart ister.
> PythonAnywhere free tier kart istemez ve 7/24 açık kalır. Bot + panel tek app
> olarak çalışır (webhook modu).

**0.** Kodu GitHub'a gönder: `git push`

**1.** [pythonanywhere.com](https://www.pythonanywhere.com) → **Create a Beginner account** (ücretsiz, kart yok).

**2.** Dashboard → **Consoles → Bash** aç ve repoyu çek:
```bash
git clone https://github.com/KULLANICI/tg-whatsapp-bot.git
cd tg-whatsapp-bot
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
> Private repo ise: `git clone https://<GITHUB_TOKEN>@github.com/KULLANICI/tg-whatsapp-bot.git`

**3.** `.env` oluştur:
```bash
nano .env      # BOT_TOKEN, PANEL_SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD_HASH gir
```
Parola hash'i için:
```bash
python -c "from werkzeug.security import generate_password_hash as g; print(g('yeni-sifre'))"
```

**4.** **Web** sekmesi → **Add a new web app** → **Manual configuration** → Python 3.10.

**5.** Web app ayarları:
- **Source code:** `/home/KULLANICI/tg-whatsapp-bot`
- **Working directory:** `/home/KULLANICI/tg-whatsapp-bot`
- **Virtualenv:** `/home/KULLANICI/tg-whatsapp-bot/venv`
- **WSGI configuration file** (linke tıkla, içeriği tamamen şununla değiştir):
```python
import os, sys
path = "/home/KULLANICI/tg-whatsapp-bot"
if path not in sys.path:
    sys.path.insert(0, path)
os.chdir(path)
from panel import app as application
```

**6.** Yeşil **Reload** butonuna bas. Panel açık:
`https://KULLANICI.pythonanywhere.com` (giriş: admin / parolan)

**7.** Webhook'u kaydet — Bash console'da:
```bash
cd ~/tg-whatsapp-bot && source venv/bin/activate
python set_webhook.py https://KULLANICI.pythonanywhere.com
```
Çıktıda `"url": ".../webhook/..."` göründüyse tamam.

**8.** Telegram'da bota **`/start`** yaz → çalışıyor 🎉

### Güncelleme
Kod değişince PA Bash'te `git pull`, sonra **Web sekmesi → Reload**.

### Free tier sınırları
- Günlük CPU kotası var (düşük trafikli destek botu için fazlasıyla yeterli).
- Hesap 3 ay girişsiz kalırsa dondurulur; giriş yapınca tekrar açılır.
- Dış bağlantı whitelist'lidir ama `api.telegram.org` whitelist'te → bot sorunsuz çalışır.

---

## Proje Yapısı

```
bot.py                    Telegram bot (local, polling)
panel.py                  Flask panel + auth + route'lar + /webhook
set_webhook.py            Webhook ayarla/sil/göster CLI
services/database.py      SQLite katmanı (CRUD + migration)
services/telegram_bot.py  Webhook mantığı (raw Telegram API)
templates/                base, login, dashboard, representatives, settings
static/css/style.css      SaaS tasarım sistemi
static/js/app.js          modal, toggle, sürükle-bırak, arama/filtre
```

Yol haritası için [ROADMAP.md](ROADMAP.md).
