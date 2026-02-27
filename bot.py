import os
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)

keyboard = [
    ["Канал"],
    ["Оформить"],
    ["Условия"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

telegram_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в Magic Salon",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Канал":
        await update.message.reply_text("https://t.me/ВАШ_КАНАЛ")

    elif text == "Оформить":
        await update.message.reply_text("Напишите ваше имя и номер телефона")

    elif text == "Условия":
        await update.message.reply_text("Условия обслуживания ...")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT, handle_message))

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "Bot is running"

if __name__ == "__main__":
    telegram_app.initialize()
    telegram_app.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
