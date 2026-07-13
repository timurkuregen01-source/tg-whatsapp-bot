"""Webhook modunda Telegram bot mantığı.

Polling yerine Telegram güncellemeleri panele POST edilir; burada işlenir.
python-telegram-bot'a bağımlı DEĞİL — sadece stdlib (urllib) ile Telegram
Bot API'sini çağırır. Böylece PythonAnywhere gibi WSGI ortamlarında
(async/event-loop derdi olmadan) sorunsuz çalışır.

Banner, Telegram'a doğrudan yüklenir (multipart). URL üzerinden çektirmeyiz;
böylece sunucu yavaş/uykuda olsa da görsel garanti gider. İlk yüklemeden sonra
Telegram'ın verdiği file_id önbelleğe alınır, tekrar yükleme yapılmaz.
"""

import os
import json
import html
import urllib.request
import urllib.error

from services.database import get_representatives

API_BASE = "https://api.telegram.org/bot{token}/{method}"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANNER_FILE = os.path.join(BASE_DIR, "static", "img", "banner.png")

WELCOME_TEXT = (
    "👋 <b>Amiral Destek Merkezi</b>'ne hoş geldiniz!\n\n"
    "🎰 Size en hızlı şekilde yardımcı olmak için buradayız.\n\n"
    "Görüşmek istediğiniz temsilciyi aşağıdan seçin 👇\n"
    "🟢 Müsait   🔴 Meşgul"
)

# İlk yüklemeden sonra Telegram'ın döndürdüğü banner file_id burada tutulur.
_banner_file_id = None


def _token():
    return os.getenv("BOT_TOKEN", "")


def _call(method, payload):
    """Telegram Bot API'sine JSON POST atar, cevabı dict döner."""
    url = API_BASE.format(token=_token(), method=method)
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": e.read().decode("utf-8", "ignore")}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _call_multipart(method, fields, file_field, filename, file_bytes,
                    content_type="image/png"):
    """Dosya (banner) yüklemek için multipart/form-data POST."""
    boundary = "----AmiralBoundaryZx7Qk9Lm2Wp"
    parts = []
    for k, v in fields.items():
        parts.append(("--" + boundary + "\r\n").encode())
        parts.append(
            ('Content-Disposition: form-data; name="%s"\r\n\r\n' % k).encode()
        )
        parts.append(str(v).encode("utf-8") + b"\r\n")
    parts.append(("--" + boundary + "\r\n").encode())
    parts.append((
        'Content-Disposition: form-data; name="%s"; filename="%s"\r\n'
        % (file_field, filename)
    ).encode())
    parts.append(("Content-Type: %s\r\n\r\n" % content_type).encode())
    parts.append(file_bytes + b"\r\n")
    parts.append(("--" + boundary + "--\r\n").encode())
    body = b"".join(parts)

    url = API_BASE.format(token=_token(), method=method)
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "multipart/form-data; boundary=" + boundary,
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": e.read().decode("utf-8", "ignore")}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _read_banner():
    try:
        with open(BANNER_FILE, "rb") as f:
            return f.read()
    except Exception:
        return None


def _start_keyboard():
    rows = []
    for rep in get_representatives():
        emoji = "🟢" if rep["status"] else "🔴"
        rows.append([{
            "text": f"{emoji} {rep['name']}",
            "callback_data": f"rep_{rep['id']}",
        }])
    return {"inline_keyboard": rows}


def _send_start(chat_id, base_url=None):
    global _banner_file_id
    keyboard = _start_keyboard()

    # 1) Daha önce yüklendiyse file_id ile hızlıca gönder.
    if _banner_file_id:
        res = _call("sendPhoto", {
            "chat_id": chat_id,
            "photo": _banner_file_id,
            "caption": WELCOME_TEXT,
            "parse_mode": "HTML",
            "reply_markup": keyboard,
        })
        if res.get("ok"):
            return
        _banner_file_id = None  # geçersiz olmuş, yeniden yükle

    # 2) Banner'ı doğrudan yükle (multipart) ve file_id'yi önbelleğe al.
    data = _read_banner()
    if data:
        res = _call_multipart("sendPhoto", {
            "chat_id": chat_id,
            "caption": WELCOME_TEXT,
            "parse_mode": "HTML",
            "reply_markup": json.dumps(keyboard),
        }, "photo", "banner.png", data)
        if res.get("ok"):
            try:
                _banner_file_id = res["result"]["photo"][-1]["file_id"]
            except (KeyError, IndexError, TypeError):
                pass
            return

    # 3) Görsel gönderilemezse düz metne düş (bot yine de cevap verir).
    _call("sendMessage", {
        "chat_id": chat_id,
        "text": WELCOME_TEXT,
        "parse_mode": "HTML",
        "reply_markup": keyboard,
    })


def _send_representative(chat_id, message_id, rep_id):
    rep = next((r for r in get_representatives() if r["id"] == rep_id), None)
    if rep is None:
        return
    status_text = "🟢 <b>Müsait</b>" if rep["status"] else "🔴 <b>Meşgul</b>"
    name = html.escape(rep["name"])
    text = (
        f"👤 <b>{name}</b>\n\n"
        f"Durum: {status_text}\n\n"
        "Aşağıdaki butondan WhatsApp üzerinden hemen yazabilirsiniz 👇"
    )
    keyboard = {"inline_keyboard": [[{
        "text": "💬 WhatsApp'tan Yaz",
        "url": f"https://wa.me/{rep['phone']}",
    }]]}
    _call("editMessageText", {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": keyboard,
    })


def handle_update(update, base_url=None):
    """Tek bir Telegram webhook update'ini işler."""
    if not isinstance(update, dict):
        return

    if "message" in update:
        msg = update["message"]
        text = msg.get("text", "") or ""
        chat_id = msg.get("chat", {}).get("id")
        if chat_id and text.startswith("/start"):
            _send_start(chat_id)

    elif "callback_query" in update:
        cq = update["callback_query"]
        _call("answerCallbackQuery", {"callback_query_id": cq.get("id")})
        data = cq.get("data", "") or ""
        msg = cq.get("message", {})
        chat_id = msg.get("chat", {}).get("id")
        message_id = msg.get("message_id")
        if data.startswith("rep_") and chat_id and message_id:
            try:
                rep_id = int(data.split("_")[1])
            except (IndexError, ValueError):
                return
            _send_representative(chat_id, message_id, rep_id)


# ----------------------------------------------------------- webhook yönetimi -
def set_webhook(base_url):
    """base_url örn: https://kullaniciadi.pythonanywhere.com"""
    hook = base_url.rstrip("/") + "/webhook/" + _token()
    return _call("setWebhook", {
        "url": hook,
        "allowed_updates": ["message", "callback_query"],
    })


def delete_webhook():
    return _call("deleteWebhook", {"drop_pending_updates": False})


def webhook_info():
    return _call("getWebhookInfo", {})
