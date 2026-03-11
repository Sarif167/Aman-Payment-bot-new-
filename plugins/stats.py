from datetime import datetime
from pyrogram import Client, filters
from info import ADMINS
from database.users_db import db

@Client.on_message(filters.private & filters.command("stats") & filters.user(ADMINS))
async def all_stats(client, message):
    msg = await message.reply_text("🔄 **Fᴇᴛᴄʜɪɴɢ Bᴜꜱɪɴᴇꜱꜱ Sᴛᴀᴛɪꜱᴛɪᴄꜱ...**")
    
    try:
        total_users = await db.total_users()
        total_payments = await db.total_payments()
        total_amount = await db.total_amount()

        current_time = datetime.now()
        active_premium = await db.users.count_documents({"expiry_time": {"$gt": current_time}})
        unused_codes = await db.codes.count_documents({"used": False})

        stats_text = (
            f"📊 **Sᴜᴘᴇʀ Aᴅᴍɪɴ Dᴀꜱʜʙᴏᴀʀᴅ** 📊\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
            f"👥 **Tᴏᴛᴀʟ Uꜱᴇʀꜱ:** `{total_users}`\n"
            f"👑 **Aᴄᴛɪᴠᴇ VIP Uꜱᴇʀꜱ:** `{active_premium}`\n\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
            f"💰 **Tᴏᴛᴀʟ Pᴀʏᴍᴇɴᴛꜱ:** `{total_payments}`\n"
            f"🪙 **Tᴏᴛᴀʟ Rᴇᴠᴇɴᴜᴇ:** `₹{total_amount}`\n\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
            f"🎟️ **Uɴᴜꜱᴇᴅ Rᴇᴅᴇᴇᴍ Cᴏᴅᴇꜱ:** `{unused_codes}`\n"
        )
        await msg.edit_text(stats_text)

    except Exception as e:
        await msg.edit_text(f"⚠️ **Eʀʀᴏʀ:** `{str(e)}`")
        
