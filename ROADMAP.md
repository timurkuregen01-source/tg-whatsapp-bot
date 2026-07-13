# 🗺️ Amiral Support Bot — Yol Haritası

Telegram destek botu + Flask yönetim paneli. Kullanıcı bota `/start` der → temsilci
listesini görür → seçtiği temsilcinin WhatsApp sohbetine yönlenir. Tüm temsilci
yönetimi web panelinden yapılır.

**Teknoloji:** Python 3 · python-telegram-bot · Flask · SQLite · Jinja2 · vanilla CSS/JS

---

## ✅ v2.0.0 — Modern Yönetim Paneli (TAMAMLANDI)

- [x] Bootstrap kaldırıldı → custom SaaS tasarım sistemi (`static/css/style.css`)
- [x] Sabit Sidebar (Dashboard · Temsilciler · İstatistik · Ayarlar · Çıkış)
- [x] Modern Topbar + mobil hamburger menü
- [x] Dashboard: istatistik kartları + son eklenenler
- [x] Temsilci kartları (avatar, durum rozeti, WhatsApp/Düzenle/Sil)
- [x] Tam CRUD (`services/database.py` + `panel.py` route'ları)
- [x] Ekle / Düzenle / Sil modal'ları (vanilla JS)
- [x] Canlı arama + Online/Offline filtre
- [x] Flash toast bildirimleri
- [x] Responsive / mobil uyumlu
- [x] `created_at` sütunu + migration guard
- [x] Ölü JSON dosyaları ve boş template'ler temizlendi

---

## 🔜 v2.1.0 — Kimlik & Güvenlik

- [ ] Admin **login** sistemi (session tabanlı, `@login_required` decorator)
- [ ] "Çıkış" menüsünü gerçek logout'a bağla
- [ ] `SECRET_KEY`'i `.env`'den zorunlu oku (dev fallback'i kaldır)
- [ ] `git rm --cached database.db` → veritabanını git takibinden çıkar
- [ ] `requirements.txt` sürümlerini pinle (`flask==3.1.3` vb.)
- [ ] `.env.example` dosyası ekle

## 🔜 v2.2.0 — Temsilci Zenginleştirme

- [ ] Panelden **anlık online/offline** toggle butonu (kart üzerinde)
- [ ] Profil fotoğrafı / avatar yükleme (`static/img/`)
- [ ] Temsilci sıralama (drag & drop veya öncelik alanı)
- [ ] Telefon numarası format doğrulama (ülke kodu kontrolü)

## 🔜 v2.3.0 — Çoklu Yönetici & Yetki

- [ ] Birden fazla admin kullanıcı + roller (owner / editor)
- [ ] Kullanıcı yönetimi sayfası
- [ ] **Audit log** (kim, ne zaman, hangi temsilciyi değiştirdi)

## 🔜 v2.4.0 — İstatistik & Raporlama

- [ ] Temsilci başına **tıklanma/yönlendirme sayacı** (bot tarafında logla)
- [ ] Dashboard grafikleri (Chart yerine hafif SVG/canvas)
- [ ] Tarih aralığı filtreli raporlar

## 🔜 v3.0.0 — Yayına Alma (Production)

- [ ] Polling → **webhook** moduna geçiş
- [ ] Render / Railway deploy + 7/24 çalışma
- [ ] SQLite → PostgreSQL migration opsiyonu
- [ ] Telegram **Mini App** (panel botun içinde açılsın)
- [ ] README + kurulum dokümantasyonu

---

## 🧹 Teknik Borç (fırsat buldukça)

- [ ] `database.db` git takibinden çıkarılacak (yukarıda)
- [ ] `requirements.txt` sürüm pinleme
- [ ] Basit test suite (`tests/` — CRUD + route smoke testleri)
- [ ] CLAUDE.md (proje mimarisi notları)
