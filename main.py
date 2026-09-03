import os, openpyxl
from database import conn, c, USE_POSTGRES, create_user
try:
    wb = openpyxl.load_workbook('ProxyStore_Backup.xlsx')
    ws = wb['Users_Balance']
    c.execute("DELETE FROM users")
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or row[0] is None: continue
        uid=int(row[0]); bal=float(row[1] or 0)
        create_user(uid)
        if USE_POSTGRES:
            c.execute("UPDATE users SET balance=%s WHERE user_id=%s",(bal,uid))
        else:
            c.execute("UPDATE users SET balance=? WHERE user_id=?",(bal,uid))
    conn.commit()
    print(f"RESTORED {ws.max_row-1} USERS")
except Exception as e:
    print(e)

from bot import bot
from handler import register_handlers
register_handlers(bot)
print("BOT Started")
bot.infinity_polling()
