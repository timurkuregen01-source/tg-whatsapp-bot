from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from dotenv import load_dotenv
from services.database import init_db, get_representatives
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    representatives = get_representatives()

    keyboard = []

    for rep in representatives:

        emoji = "🟢" if rep["status"] else "🔴"

        keyboard.append([
            InlineKeyboardButton(
                f"{emoji} {rep['name']}",
                callback_data=f"rep_{rep['id']}"
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "🎰 *Amiral Destek Merkezi*\n\n"
        "Hoş geldiniz.\n\n"
        "Lütfen görüşmek istediğiniz temsilciyi seçiniz."
    )

    await update.message.reply_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


async def representative(update: Update, context: ContextTypes.DEFAULT_TYPE):

    representatives = get_representatives()

    query = update.callback_query
    await query.answer()

    rep_id = int(query.data.split("_")[1])

    rep = next(r for r in representatives if r["id"] == rep_id)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💬 WhatsApp'a Git",
                url=f"https://wa.me/{rep['phone']}"
            )
        ]
    ])

    status_text = "🟢 Online" if rep["status"] else "🔴 Offline"

    await query.edit_message_text(
        text=f"""👤 {rep['name']}

{status_text}

Temsilci ile görüşmek için aşağıdaki butona tıklayabilirsiniz.""",
        reply_markup=keyboard
    )


def main():

    init_db()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(representative))

    print("✅ Amiral Bot çalışıyor...")

    app.run_polling()


if __name__ == "__main__":
    main()