import os
import threading
import asyncio
from dotenv import load_dotenv
from flask import Flask
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load token
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- COURSE COMMANDS ---
COURSE_LINKS = {
    "apnacollege": "https://t.me/c/2556988393/2",
    "gate": "https://t.me/c/2556988393/7",
    "codewithharry": "https://t.me/c/2556988393/55",
    "gmat": "https://t.me/c/2556988393/53",
    "devops": "https://t.me/c/2556988393/52",
    "timemanagement": "https://t.me/c/2556988393/51",
    "frenchspoken": "https://t.me/c/2556988393/50",
    "mysirg": "https://t.me/c/2556988393/49",
    "financewithsharan": "https://t.me/c/2556988393/48",
    "codebasic": "https://t.me/c/2556988393/47",
    "codingseekho": "https://t.me/c/2556988393/46",
    "uiux": "https://t.me/c/2556988393/45",
    "appdevelopment": "https://t.me/c/2556988393/44",
    "csir": "https://t.me/c/2556988393/43",
    "rrbje": "https://t.me/c/2556988393/41",
    "tapacademy": "https://t.me/c/2556988393/40",
    "pornaddiction": "https://t.me/c/2556988393/39",
    "almabetter": "https://t.me/c/2556988393/38",
    "excel": "https://t.me/c/2556988393/37",
    "wscube": "https://t.me/c/2556988393/36",
    "cuet": "https://t.me/c/2556988393/35",
    "jee": "https://t.me/c/2556988393/34",
    "btech": "https://t.me/c/2556988393/33",
    "dhruvrathee": "https://t.me/c/2556988393/32",
    "ankurwarikoo": "https://t.me/c/2556988393/31",
    "krishnaik": "https://t.me/c/2556988393/30",
    "nimcet": "https://t.me/c/2556988393/29",
    "sanketsingh": "https://t.me/c/2556988393/28",
    "fraz": "https://t.me/c/2556988393/27",
    "harkiratsingh": "https://t.me/c/2556988393/26",
    "trading": "https://t.me/c/2556988393/25",
    "udemy": "https://t.me/c/2556988393/24",
    "cat": "https://t.me/c/2556988393/23",
    "ezsnippet": "https://t.me/c/2556988393/21",
    "botmaking": "https://t.me/c/2556988393/20",
    "scaler": "https://t.me/c/2556988393/19",
    "techburner": "https://t.me/c/2556988393/18",
    "canva": "https://t.me/c/2556988393/17",
    "wordpress": "https://t.me/c/2556988393/16",
    "campusx": "https://t.me/c/2556988393/15",
    "banking": "https://t.me/c/2556988393/14",
    "durgasoft": "https://t.me/c/2556988393/13",
    "anujbhaiya": "https://t.me/c/2556988393/12",
    "rbrsir": "https://t.me/c/2556988393/11",
    "abdulbari": "https://t.me/c/2556988393/10",
    "sheriyians": "https://t.me/c/2556988393/9",
    "rohitnegi": "https://t.me/c/2556988393/8",
    "hiteshchaudhary": "https://t.me/c/2556988393/6",
    "procoder": "https://t.me/c/2556988393/5",
    "akshaysaini": "https://t.me/c/2556988393/4",
    "lovebabber": "https://t.me/c/2556988393/3"
}


# --- COURSE HANDLER ---
async def send_course_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.split()[0]
    command = text[1:].split('@')[0].lower()
    link = COURSE_LINKS.get(command)

    if link:
        bot_msg = await update.message.reply_text(
            f"📚 *{command}* course link:\n👉 {link}", parse_mode="Markdown")
    else:
        bot_msg = await update.message.reply_text(
            "❌ Course not found! Use /help to see available courses.")

    context.application.create_task(delete_messages_later(update, bot_msg))


async def delete_messages_later(update: Update, bot_msg):
    await asyncio.sleep(30)
    try:
        await update.message.delete()
        await bot_msg.delete()
    except Exception as e:
        print(f"⚠️ Delete error: {e}")


# --- HELP COMMAND ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = "\n".join(f"/{cmd}" for cmd in COURSE_LINKS)
    await update.message.reply_text(
        f"📘 *Available Courses:*\n\n{commands}\n\nUse any command to get the link.",
        parse_mode="Markdown")


# --- UNKNOWN COMMAND HANDLER ---
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Invalid command! Use /help to see valid ones.")


# --- Flask Server ---
flask_app = Flask("")


@flask_app.route("/")
def home():
    return "🤖 Bot is Alive!"


def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)


# --- Telegram App Build ---
app = ApplicationBuilder().token(
    BOT_TOKEN).post_init(lambda app: app.bot.set_my_commands([
        BotCommand(command=cmd, description=f"Get {cmd} course")
        for cmd in COURSE_LINKS
    ] + [BotCommand(command="help", description="Show all available courses")])
                         ).build()

# Register command handlers
for cmd in COURSE_LINKS:
    app.add_handler(CommandHandler(cmd, send_course_link))

app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.COMMAND,
                               unknown_command))  # Handle all unknown commands


# --- Runner ---
def run_telegram():
    app.run_polling()


if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_telegram()
