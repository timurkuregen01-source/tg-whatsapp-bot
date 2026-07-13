"""Webhook modunda Telegram bot mantığı.

Polling yerine Telegram güncellemeleri panele POST edilir; burada işlenir.
python-telegram-bot'a bağımlı DEĞİL — sadece stdlib (urllib) ile Telegram
Bot API'sini çağırır. Böylece PythonAnywhere gibi WSGI ortamlarında
(async/event-loop derdi olmadan) sorunsuz çalışır.
"""

import os
import json
import urllib.request
import urllib.error

from services.database import get_representatives

API_BASE = "https://api.telegram.org/bot{token}/{method}"

WELCOME_TEXT = (
    "🎰 *Amiral Destek Merkezi*\n\n"
    "Hoş geldiniz.\n\n"
    "Lütfen görüşmek istediğiniz temsilciyi seçiniz."
)


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


def _start_keyboard():
    rows = []
    for rep in get_representatives():
        emoji = "🟢" if rep["status"] else "🔴"
        rows.append([{
            "text": f"{emoji} {rep['name']}",
            "callback_data": f"rep_{rep['id']}",
        }])
    return {"inline_keyboard": rows}


def _send_start(chat_id):
    _call("sendMessage", {
        "chat_id": chat_id,
        "text": WELCOME_TEXT,
        "parse_mode": "Markdown",
        "reply_markup": _start_keyboard(),
    })


def _send_representative(chat_id, message_id, rep_id):
    rep = next((r for r in get_representatives() if r["id"] == rep_id), None)
    if rep is None:
        return
    status_text = "🟢 Online" if rep["status"] else "🔴 Offline"
    text = (
        f"👤 {rep['name']}\n\n{status_text}\n\n"
        "Temsilci ile görüşmek için aşağıdaki butona tıklayabilirsiniz."
    )
    keyboard = {"inline_keyboard": [[{
        "text": "💬 WhatsApp'a Git",
        "url": f"https://wa.me/{rep['phone']}",
    }]]}
    _call("editMessageText", {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "reply_markup": keyboard,
    })


def handle_update(update):
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
