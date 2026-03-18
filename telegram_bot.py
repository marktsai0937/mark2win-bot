"""
Telegram Bot - 任務溝通平台 (雲端版)
支援 Webhook 部署 + 任務儲存

使用方式：
1. 本地測試：直接執行 python telegram_bot.py
2. 雲端部署：部署到 Render.com
"""

import os
import json
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 環境變數
TOKEN = os.environ.get("TELEGRAM_TOKEN", "8788838867:AAGF1Shv4JQgCxP6OHXzF8iBAOX6vEA4ZpY")

# 任務儲存
TASKS_FILE = "tasks.json"
LOG_FILE = "bot.log"

# 管理員 ID（只有我能發通知）
ADMIN_ID_FILE = "admin_id.txt"


def save_admin_id(user_id):
    """儲存管理員 ID"""
    with open(ADMIN_ID_FILE, 'w') as f:
        f.write(str(user_id))


def get_admin_id():
    """取得管理員 ID"""
    if os.path.exists(ADMIN_ID_FILE):
        with open(ADMIN_ID_FILE, 'r') as f:
            return f.read().strip()
    return None


def load_tasks():
    """載入任務"""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_tasks(tasks):
    """儲存任務"""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /start 命令"""
    await update.message.reply_text(
        "👋 你好！我是 mark2winTelegBot\n\n"
        "這是 Sisyphus 的溝通平台。\n"
        "你可以直接傳任務給我，我會記錄下來。\n\n"
        "可用命令：\n"
        "/start - 顯示歡迎訊息\n"
        "/tasks - 查看所有任務\n"
        "/help - 顯示幫助"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理 /help 命令"""
    await update.message.reply_text(
        "📖 幫助\n\n"
        "你可以：\n"
        "- 直接傳任務給我\n"
        "- 我會記錄並通知 Sisyphus\n"
        "- 任務完成後會回覆你\n\n"
        "命令：\n"
        "/tasks - 查看任務清單\n"
        "/clear - 清除所有任務"
    )


async def tasks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """查看任務"""
    tasks = load_tasks()
    if not tasks:
        await update.message.reply_text("📝 目前沒有任務")
    else:
        msg = "📝 任務清單：\n\n"
        for i, task in enumerate(tasks, 1):
            msg += f"{i}. {task}\n"
        await update.message.reply_text(msg)


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """清除任務"""
    save_tasks([])
    await update.message.reply_text("✅ 所有任務已清除")


async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """註冊管理員（設定誰可以收通知）"""
    user_id = update.effective_user.id
    save_admin_id(user_id)
    await update.message.reply_text(
        f"✅ 管理員已設定！\n"
        f"你的 ID: {user_id}\n\n"
        f"Sisyphus 完成任務後會通知你。"
    )


# === 以下是我（Sisyphus）用來通知你的功能 ===

async def notify_admin(application, message):
    """通知管理員"""
    admin_id = get_admin_id()
    if admin_id:
        try:
            await application.bot.send_message(
                chat_id=int(admin_id),
                text=message
            )
            return True
        except Exception as e:
            print(f"通知失敗: {e}")
            return False
    return False


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """處理收到的訊息"""
    user_name = update.effective_user.first_name or "User"
    user_message = update.message.text
    
    # 記錄
    log_msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {user_name}: {user_message}"
    print(log_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')
    
    # 儲存任務
    tasks = load_tasks()
    tasks.append(user_message)
    save_tasks(tasks)
    
    # 回覆確認
    await update.message.reply_text(
        f"✅ 任務已記錄！\n\n"
        f"內容：{user_message}\n\n"
        f"Sisyphus 會儘快處理並回覆你。"
    )


async def post_init(application: Update):
    """Bot 啟動後執行"""
    print("✅ Bot 啟動成功！")
    print(f"Token: {TOKEN[:10]}...")


# === API 功能：讓我可以讀取任務 ===
from telegram import Bot

async def get_tasks_api(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """API：讀取所有任務"""
    # 簡單密碼保護
    if len(context.args) > 0 and context.args[0] == "mark2win123":
        tasks = load_tasks()
        if not tasks:
            await update.message.reply_text("無任務")
        else:
            msg = "📝 任務清單：\n\n"
            for i, task in enumerate(tasks, 1):
                msg += f"{i}. {task}\n"
            await update.message.reply_text(msg)
    else:
        await update.message.reply_text("❌ 密碼錯誤")


async def delete_task_api(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """API：刪除指定任務"""
    if len(context.args) > 1 and context.args[0] == "mark2win123":
        try:
            index = int(context.args[1]) - 1
            tasks = load_tasks()
            if 0 <= index < len(tasks):
                deleted = tasks.pop(index)
                save_tasks(tasks)
                await update.message.reply_text(f"✅ 已刪除：{deleted}")
            else:
                await update.message.reply_text("❌ 編號無效")
        except:
            await update.message.reply_text("❌ 指令格式錯誤")
    else:
        await update.message.reply_text("❌ 密碼錯誤")


def main():
    """啟動 Bot"""
    print("=" * 50)
    print("  mark2winTelegBot 雲端版")
    print("=" * 50)
    
    # 建立 Application
    application = Application.builder().token(TOKEN).post_init(post_init).build()
    
    # 註冊命令處理器
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tasks", tasks_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("register", register_command))
    
    # API 命令（讓 Sisyphus 讀取任務）
    application.add_handler(CommandHandler("tasks_api", get_tasks_api))
    application.add_handler(CommandHandler("delete_task", delete_task_api))
    
    # 註冊訊息處理器
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # 判斷 Webhook 或 Polling
    webhook_url = os.environ.get("WEBHOOK_URL", "https://mark2win-bot.onrender.com")
    
    # Webhook 模式（雲端）
    print(f"\n🌐 Webhook 模式: {webhook_url}")
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=webhook_url,
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
