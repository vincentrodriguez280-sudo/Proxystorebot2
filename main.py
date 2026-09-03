from bot import bot
from handler import register_handlers
from backup import create_backup_excel, get_db_file_if_sqlite
from config import ADMIN_ID
import threading
import time
import os

register_handlers(bot)

# ========== BACKUP COMMAND ==========
@bot.message_handler(commands=["backup"])
def backup_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Access Denied - Only Admin can backup")
        return
    bot.reply_to(message, "⏳ Backup create hocche...")
    try:
        # Excel backup
        excel_file = create_backup_excel()
        if excel_file:
            bot.send_document(ADMIN_ID, excel_file, caption=f"FULL BACKUP\n\nUsers + Balance, Orders, Stock Available + Used, Referrals\nTime: {excel_file.name}\n\nEi file diye onno Railway te restore korte parben.")
        
        # SQLite file if exists
        db_file = get_db_file_if_sqlite()
        if db_file:
            with open(db_file, 'rb') as f:
                bot.send_document(ADMIN_ID, f, caption="SQLite DB file proxystore.db")
        
        bot.send_message(ADMIN_ID, "Backup Done! File gulo save kore rakhen.")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"Backup error: {e}")
        print(f"Backup error: {e}")

def auto_backup_loop():
    while True:
        try:
            time.sleep(12 * 60 * 60)  # 12 hours
            print("Auto backup running...")
            excel_file = create_backup_excel()
            if excel_file:
                bot.send_document(ADMIN_ID, excel_file, caption=f"AUTO BACKUP 12h - {excel_file.name} - Auto save kore rakhen")
        except Exception as e:
            print(f"Auto backup error: {e}")
            time.sleep(60)

# Start auto backup in background thread
backup_thread = threading.Thread(target=auto_backup_loop, daemon=True)
backup_thread.start()

print("✅ ProxyStore BOT Started with Backup System")
print("Commands: /backup - manual backup, Auto backup every 12h")
bot.infinity_polling(timeout=30, skip_pending=True)
