import openpyxl
from database import conn, c
wb = openpyxl.load_workbook('ProxyStore_Backup.xlsx')

# USERS
ws = wb['Users_Balance']
c.execute("DELETE FROM users")
for r in ws.iter_rows(min_row=2, values_only=True):
    if not r or r[0] is None: continue
    try:
        c.execute("INSERT INTO users (user_id, balance) VALUES (%s,%s) ON CONFLICT (user_id) DO UPDATE SET balance=%s", (int(r[0]), float(r[1] or 0), float(r[1] or 0)))
    except:
        c.execute("INSERT OR REPLACE INTO users (user_id, balance) VALUES (?,?)", (int(r[0]), float(r[1] or 0)))
conn.commit()
print(f"Users {ws.max_row-1} restored")

# STOCK
ws = wb['Stock_Available']
c.execute("DELETE FROM stock")
for r in ws.iter_rows(min_row=2, values_only=True):
    if not r or not r[1] or not r[3]: continue
    try:
        c.execute("INSERT INTO stock (category, product_name, code, status) VALUES (%s,%s,%s,'available')", (str(r[1]), str(r[2]), str(r[3])))
    except:
        c.execute("INSERT INTO stock (category, product_name, code, status) VALUES (?,?,?,'available')", (str(r[1]), str(r[2]), str(r[3])))
conn.commit()
print(f"Stock {ws.max_row-1} restored")

from bot import bot
from handler import register_handlers
register_handlers(bot)
print("BOT OK")
bot.infinity_polling()
