"""Telegram webhook'unu ayarla / sil / göster.

Kullanım:
  python set_webhook.py https://KULLANICIADI.pythonanywhere.com   # webhook'u ayarla
  python set_webhook.py delete                                    # webhook'u sil (local polling için)
  python set_webhook.py                                           # mevcut durumu göster

Not: PythonAnywhere free tier'da bunu Bash console'dan çalıştır — api.telegram.org
whitelist'te olduğu için sorunsuz çalışır.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from services.telegram_bot import set_webhook, delete_webhook, webhook_info


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None

    if arg is None:
        print("Mevcut webhook bilgisi:")
        print(webhook_info())
        print("\nAyarlamak için: python set_webhook.py https://KULLANICIADI.pythonanywhere.com")
        return

    if arg.lower() == "delete":
        print("Webhook siliniyor...")
        print(delete_webhook())
        return

    if not arg.startswith("https://"):
        print("❌ URL https:// ile başlamalı. Örn: https://kullaniciadi.pythonanywhere.com")
        sys.exit(1)

    print(f"Webhook ayarlanıyor → {arg}/webhook/<token>")
    print(set_webhook(arg))
    print("\nDoğrulama:")
    print(webhook_info())


if __name__ == "__main__":
    main()
