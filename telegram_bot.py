"""
Telegram Bot - 简化版
"""

import os
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8788838867:AAGF1Shv4JQgCxP6OHXzF8iBAOX6vEA4ZpY"

TASKS_FILE = "tasks.json"
ADMIN_FILE = "admin_id.txt"


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 你好！我是 mark2winTelegBot\n\n傳任務給我，我會記錄下來。")


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    with open(ADMIN_FILE, 'w') as f:
        f.write(str(user_id))
    await update.message.reply_text(f"✅ 已設定！你會收到通知。")


async def tasks_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if not tasks:
        await update.message.reply_text("📝 無任務")
    else:
        msg = "📝 任務：\n\n"
        for i, t in enumerate(tasks, 1):
            msg += f"{i}. {t}\n"
        await update.message.reply_text(msg)


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    tasks = load_tasks()
    tasks.append(user_message)
    save_tasks(tasks)
    await update.message.reply_text(f"✅ 已記錄：{user_message}")


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("tasks", tasks_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    
    webhook_url = "https://mark2win-bot.onrender.com"
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=webhook_url
    )


if __name__ == "__main__":
    main()
