import os
import pytz
from datetime import date, datetime
from aiohttp import web
from pyrogram import Client, enums

from info import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, ADMINS
# Dhyan rahe ki check_expired_premium aapki route.py me save ho
from route import web_server, check_expired_premium 
from utils import temp

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="avbotzz",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins=dict(root="plugins"), # Yahan plugins folder set hai
            sleep_threshold=15,
            max_concurrent_transmissions=5,
        )

    async def start(self):
        await super().start()

        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        temp.B_LINK = me.mention
        self.username = '@' + me.username

        # ---------------- WEB SERVER & BACKGROUND TASKS ----------------
        app_instance = web_server()
        
        # Aapka Auto-Kick aur Reminder system yahan background me start ho gaya! 🚀
        self.loop.create_task(check_expired_premium(self)) 
        
        runner = web.AppRunner(app_instance)
        await runner.setup()

        port = int(os.environ.get("PORT", 8000))
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        # ---------------------------------------------------------------

        tz = pytz.timezone('Asia/Kolkata')
        today = date.today()
        now = datetime.now(tz)
        time_str = now.strftime("%H:%M:%S %p")

        print(f"{me.first_name} IS STARTED ⚡️ (Port: {port})")

        # -------- ADMIN NOTIFICATION --------
        curr_admins = ADMINS if isinstance(ADMINS, list) else [ADMINS]
        for admin in curr_admins:
            try:
                await self.send_message(
                    chat_id=admin,
                    text=f"<b>✨ {me.first_name} ɪs ɴᴏᴡ ᴏɴʟɪɴᴇ !</b>",
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception as e:
                print(f"Admin Notify Error ({admin}): {e}")

        # -------- LOG CHANNEL --------
        if LOG_CHANNEL:
            try:
                await self.send_message(
                    LOG_CHANNEL,
                    text=(
                        f"<b>🚀 ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ</b>\n"
                        "➖➖➖➖➖➖➖➖➖➖➖\n"
                        f"<b>📅 ᴅᴀᴛᴇ :</b> <code>{today}</code>\n"
                        f"<b>⏰ ᴛɪᴍᴇ :</b> <code>{time_str}</code>\n"
                        f"<b>🌍 ᴛɪᴍᴇᴢᴏɴᴇ :</b> <code>Asia/Kolkata</code>\n"
                        "➖➖➖➖➖➖➖➖➖➖➖"
                    ),
                    parse_mode=enums.ParseMode.HTML
                )
            except Exception as e:
                print(f"Log Channel Error: {e}")

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped. Bye!")


if __name__ == "__main__":
    app = Bot()
    app.run()
    
