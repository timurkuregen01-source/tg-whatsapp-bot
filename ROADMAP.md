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

## 🔜 v3.0.0 — Canlıya Alma (Production) — EN SON, SAĞLAM

- [ ] Paneli **Render**'a deploy → public link (`render.yaml` hazır)
- [ ] SQLite → **PostgreSQL** migration (panel + bot aynı DB'yi paylaşsın)
- [ ] Bot: polling → **webhook** moduna geçiş, 7/24 çalışma
- [ ] Production `.env` (güçlü SECRET_KEY, admin parolası)

> ⚠️ **Netlify değil.** Netlify statik site barındırır; Flask + SQLite + bot çalışmaz.
> Doğru adres Render / Railway. Detay [README.md](README.md).

---

## ❌ Kapsam dışı (istenmedi)

- Çoklu yönetici / rol sistemi
- Avatar / profil fotoğrafı yükleme
- İstatistik & raporlama (gelişmiş grafikler, sayaçlar)

## 🧹 Teknik Borç (fırsat buldukça)

- [ ] Basit test suite (`tests/` — smoke testleri repo'ya alınabilir)
- [ ] CLAUDE.md (proje mimarisi notları)
