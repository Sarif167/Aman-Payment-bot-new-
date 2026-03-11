import logging
from aiohttp import web
from datetime import datetime, timedelta
from asyncio import sleep
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_db import db
from info import CHANNEL_LINK, LOG_CHANNEL, END_PIC, EXPIRE_SOON_PIC, SUPPORT

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(text="𝚇𝙿 sᴜʙsᴄʀɪᴘᴛɪᴏɴ ʙᴏᴛ ʀᴜɴɴɪɴɢ ✅")

def web_server():
    app = web.Application(client_max_size=30000000)
    app.add_routes(routes)
    return app 

# Reminder intervals fixed
REMINDER_TIMES = [
    ("10 ᴍɪɴᴜᴛᴇs", timedelta(minutes=10)),
    ("50 ᴍɪɴᴜᴛᴇs", timedelta(minutes=50)),
    ("1 ᴅᴀʏ", timedelta(days=1)) # 'day' fixed to 'days'
]

async def check_expired_premium(client):
    while True:
        now = datetime.utcnow()
        
        # 1. HANDLE EXPIRED USERS (Auto-Kick)
        expired_users = await db.get_expired(now)
        for user in expired_users:
            user_id = user["id"]
            try:
                await db.remove_premium_access(user_id)
                unset_flags = {f"reminder_{label}_sent": "" for label, _ in REMINDER_TIMES}
                await db.users.update_one({"id": user_id}, {"$unset": unset_flags})
                
                tg_user = await client.get_users(user_id)
                
                # Kick from VIP Channel
                try:
                    await client.ban_chat_member(chat_id=CHANNEL_LINK, user_id=user_id)
                    await client.unban_chat_member(chat_id=CHANNEL_LINK, user_id=user_id)
                except:
                    pass

                # Buttons for Expiry Message
                expiry_buttons = InlineKeyboardMarkup([
                    [InlineKeyboardButton("✨ ʀᴇɴᴇᴡ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ✨", callback_data="subscription")],
                    [InlineKeyboardButton("📢 ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs", url="https://t.me/TenxHubBackup"), InlineKeyboardButton("📜 ᴏᴡɴᴇʀ", url="https://t.me/xp_prajwal")]
                ])

                await client.send_photo(
                    chat_id=user_id,
                    photo=END_PIC,
                    caption=f"<b>ʜᴇʏ {tg_user.mention},\n\nʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ʜᴀs ᴇxᴘɪʀᴇᴅ ᴀɴᴅ ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴛʜᴇ ᴠɪᴘ ᴄʜᴀɴɴᴇʟ.\n\nᴛᴀᴘ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ʀᴇɴᴇᴡ ɴᴏᴡ!</b>",
                    reply_markup=expiry_buttons
                )

                await client.send_message(
                    LOG_CHANNEL,
                    f"<b>#ᴘʀᴇᴍɪᴜᴍ_ᴇxᴘɪʀᴇᴅ_ᴋɪᴄᴋᴇᴅ\n\nᴜsᴇʀ: {tg_user.mention}\nɪᴅ: <code>{user_id}</code></b>"
                )
            except Exception as e:
                logging.error(f"Expiry Error for {user_id}: {e}")
            await sleep(0.5)

        # 2. HANDLE REMINDERS (Before Expiry)
        for label, delta in REMINDER_TIMES:
            reminder_users = await db.get_expiring_soon(label, delta)
            for user in reminder_users:
                user_id = user["id"]
                try:
                    tg_user = await client.get_users(user_id)

                    await client.send_photo(
                        user_id,
                        photo=EXPIRE_SOON_PIC,
                        caption=f"<b>ʜᴇʏ {tg_user.mention},\n\nʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴡɪʟʟ ᴇxᴘɪʀᴇ ɪɴ {label}.\n\nʀᴇɴᴇᴡ ɴᴏᴡ ᴛᴏ ᴀᴠᴏɪᴅ ɢᴇᴛᴛɪɴɢ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴠɪᴘ!</b>"
                    )

                    await client.send_message(
                        chat_id=LOG_CHANNEL,
                        caption=f"<b>#ʀᴇᴍɪɴᴅᴇʀ_sᴇɴᴛ ({label})\n\nᴜsᴇʀ: {tg_user.mention}\nɪᴅ: <code>{user_id}</code></b>"
                    )
                except Exception as e:
                    logging.error(f"Reminder Error for {user_id}: {e}")
                await sleep(0.5)
                
        await sleep(30) # Loop interval to save CPU
