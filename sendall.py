from telethon.sync import TelegramClient
import sqlite3, aiocron , asyncio, time
import sys
sys.path.append('../')
import confi as config
# ======================= client ===========================
api_id = config.api_id
api_hash = config.api_hash
owner = config.owner
twofanew = config.twofanew
token = config.token
bot = TelegramClient('sendall_1', api_id, api_hash)
bot.start(bot_token=token)
# =========================== database ======================
conn = sqlite3.connect("../data.db")
cursor = conn.cursor()
# =========================== functions ======================
def query(query):
    result = cursor.execute(query)
    conn.commit()
    return result


# =========================== sendall ======================
@aiocron.crontab('*/1 * * * *')
async def sendall():
    sendallstatus = cursor.execute(f"SELECT `text` FROM `setting` WHERE `type` = 'sendallstatus'").fetchone()[0]
    sendalltext = cursor.execute(f"SELECT `text` FROM `setting` WHERE `type` = 'sendalltext'").fetchone()[0]
    forwardallstatus = cursor.execute(f"SELECT `text` FROM `setting` WHERE `type` = 'forwardallstatus'").fetchone()[0]
    forwardallmsgid = cursor.execute(f"SELECT `text` FROM `setting` WHERE `type` = 'forwardallmsgid'").fetchone()[0]
    if sendallstatus == "ON":
        query(f"UPDATE `setting` SET `text` = 'NULL' WHERE `type` = 'sendalltext'")
        query(f"UPDATE `setting` SET `text` = 'NULL' WHERE `type` = 'sendallstatus'")
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        await bot.send_message(owner,"✅ارسال پیام همگانی شروع شد") 
        for row in rows:
            userid = row[0]
            try:
                time.sleep(1)
                await bot.send_message(int(userid),sendalltext)
            except Exception as e:
                print(f"error: '{e}'")
                if input('inuput:'):
                    exit()
                else:
                    continue

        await bot.send_message(owner,"✅ارسال پیام همگانی پایان یافت") 
    if forwardallstatus == "ON":
        query(f"UPDATE `setting` SET `text` = 'NULL' WHERE `type` = 'forwardallmsgid'")
        query(f"UPDATE `setting` SET `text` = 'NULL' WHERE `type` = 'forwardallstatus'")
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        await bot.send_message(owner,"✅ارسال فروارد همگانی شروع شد") 
        for row in rows:
            userid = row[0]
            try:
                time.sleep(1)
                await bot.forward_messages(entity=int(userid),messages=int(forwardallmsgid),from_peer=owner)
            except:
                continue  
        await bot.send_message(owner,"✅ارسال فروارد همگانی پایان یافت")         
# =================================================
loop = asyncio.get_event_loop()
loop.run_forever()
sendall.start()
asyncio.get_event_loop().run_forever()
bot.run_until_disconnected()
