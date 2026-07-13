# 🗺️ Amiral Support Bot — Yol Haritası

Telegram destek botu + Flask yönetim paneli. Kullanıcı bota `/start` der → temsilci
listesini görür → seçtiği temsilcinin WhatsApp sohbetine yönlenir. Tüm temsilci
yönetimi web panelinden yapılır.

**Teknoloji:** Python 3 · python-telegram-bot · Flask · SQLite · Jinja2 · vanilla CSS/JS

---

## ✅ v2.0.0 — Modern Yönetim Paneli (TAMAMLANDI)

- [x] Bootstrap kaldırıldı → custom SaaS tasarım sistemi (`static/css/style.css`)
- [x] Sabit Sidebar + modern Topbar + mobil hamburger menü
- [x] Dashboard: istatistik kartları + son eklenenler
- [x] Temsilci kartları (avatar, durum rozeti, WhatsApp/Düzenle/Sil)
- [x] Tam CRUD + Ekle/Düzenle/Sil modal'ları
- [x] Canlı arama + Online/Offline filtre
- [x] Flash toast bildirimleri, responsive tasarım

## ✅ v2.1.0 — Admin Login (TAMAMLANDI)

- [x] Hash'li parola ile admin girişi (werkzeug)
- [x] Session tabanlı oturum + `@login_required` korumalı route'lar
- [x] Gerçek logout, `.env` tabanlı gizli anahtar & admin bilgileri
- [x] `.env.example`, `database.db` git takibinden çıkarıldı

## ✅ v2.2.0 — Temsilci Toggle & Sıralama (TAMAMLANDI)

- [x] Kart üzerinde **anlık online/offline toggle** (AJAX, sayfa yenilemesiz)
- [x] **Sürükle-bırak** ile temsilci sıralama (`sort_order` + migration)
- ~~Avatar/profil foto yükleme~~ (istenmedi)

---

## 🔄 v3.0.0 — Canlıya Alma (PythonAnywhere · ücretsiz · kartsız · 7/24)

Kod tarafı hazır, geriye tek manuel adım kaldı:

- [x] Bot **webhook** moduna geçti (`services/telegram_bot.py` + panel `/webhook/<token>`)
- [x] Bot + panel **tek uygulama** → aynı SQLite'ı paylaşıyor (bulut "iki servis" sorunu çözüldü)
- [x] `set_webhook.py` (webhook ayarla/sil/göster) + PythonAnywhere WSGI hazır
- [ ] **Senin adımın:** PythonAnywhere hesabı aç → dosyaları yükle → web app kur → webhook'u ayarla
      (adım adım [README.md](README.md))
- [ ] Production `.env` (güçlü PANEL_SECRET_KEY, gerçek admin parolası)

> ✅ PythonAnywhere free: kart yok, 7/24 açık. SQLite tek app'te sorunsuz.
> Netlify Flask çalıştıramaz; Render kart ister. (Render'ı yine de denemek istersen
> `render.yaml` repoda duruyor.) İleride yük artarsa PostgreSQL'e geçiş opsiyonel.

---

## ❌ Kapsam dışı (istenmedi)

- Çoklu yönetici / rol sistemi
- Avatar / profil fotoğrafı yükleme
- İstatistik & raporlama (gelişmiş grafikler, sayaçlar)

## 🧹 Teknik Borç (fırsat buldukça)

- [ ] Basit test suite (`tests/` — smoke testleri repo'ya alınabilir)
- [ ] CLAUDE.md (proje mimarisi notları)
