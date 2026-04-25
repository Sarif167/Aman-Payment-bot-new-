import logging, pytz
from aiohttp import web
from datetime import datetime, timedelta
from asyncio import sleep
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_db import db
from info import (
    LOG_CHANNEL, END_PIC, EXPIRE_SOON_PIC, 
    CHANNEL_LINK_MOV, CHANNEL_LINK_INST
)

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.Response(text="sᴜʙsᴄʀɪᴘᴛɪᴏɴ ʙᴏᴛ ʀᴜɴɴɪɴɢ ✅")

def web_server():
    app = web.Application(client_max_size=30000000)
    app.add_routes(routes)
    return app 

REMINDER_TIMES = [
    ("𝟷𝟶 ᴍɪɴᴜᴛᴇs", timedelta(minutes=10)),
    ("𝟷 ʜᴏᴜʀ", timedelta(hours=1)),
    ("𝟷 ᴅᴀʏ", timedelta(days=1))
]

async def check_expired_premium(client):
    while True:
        now = datetime.now()
        
        for category, channel, expiry_key in [
            ("🎬 ᴍᴏᴠɪᴇ", CHANNEL_LINK_MOV, "expiry_mov"),
            ("📸 ɪ狀sᴛᴀ", CHANNEL_LINK_INST, "expiry_inst")
        ]:
            # 1. ʜᴀɴᴅʟᴇ ᴇxᴘɪʀᴇᴅ ᴜsᴇʀs
            expired_users = await db.users.find({expiry_key: {"$lt": now}}).to_list(None)
            
            for user in expired_users:
                u_id = user["id"]
                try:
                    await db.users.update_one({"id": u_id}, {"$unset": {expiry_key: ""}})
                    
                    try:
                        await client.ban_chat_member(channel, u_id)
                        await client.unban_chat_member(channel, u_id)
                    except: pass

                    btns = InlineKeyboardMarkup([
                        [InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ", url="https://t.me/premiumuseronly_Bot")]
                    ])

                    await client.send_photo(
                        chat_id=u_id,
                        photo=END_PIC,
                        caption=f"<b>ʜᴇʏ,\n\nʏᴏᴜʀ {category} Aapka premium access expire ho gaya hai aur aapko VIP channel se remove kar diya gaya hai.</b>",
                        reply_markup=btns
                    )

                    await client.send_message(LOG_CHANNEL, f"<b>#ᴇxᴘɪʀᴇᴅ_ᴋɪᴄᴋᴇᴅ\n\nᴜsᴇʀ: <code>{u_id}</code>\nᴄᴀᴛᴇɢᴏʀʏ: {category}</b>")
                except Exception as e:
                    logging.error(f"ᴇxᴘɪʀʏ ᴇʀʀᴏʀ: {e}")
                await sleep(0.5)

            # 2. ʜᴀɴᴅʟᴇ ʀᴇᴍɪɴᴅᴇʀs
            for label, delta in REMINDER_TIMES:
                reminder_key = f"rem_{expiry_key}_{label.replace(' ', '_')}"
                upcoming = now + delta
                
                users_to_remind = await db.users.find({
                    expiry_key: {"$gt": now, "$lt": upcoming},
                    reminder_key: {"$exists": False}
                }).to_list(None)

                for user in users_to_remind:
                    u_id = user["id"]
                    try:
                        await client.send_photo(
                            u_id,
                            photo=EXPIRE_SOON_PIC,
                            caption=f"<b>ʜᴇʏ,\n\nʏᴏᴜʀ {category} Aapka premium kuch hi samay me expire ho jayega {label}.\nVIP me rehne ke liye abhi renew karein!</b>"
                        )
                        await db.users.update_one({"id": u_id}, {"$set": {reminder_key: True}})
                    except: pass
                    await sleep(0.5)

        await sleep(60)
        
