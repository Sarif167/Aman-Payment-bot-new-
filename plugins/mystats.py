import pytz
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from info import ADMINS
from database.users_db import db

# ==========================================
# 📊 ᴀᴅᴍɪɴ sᴛᴀᴛs ᴅᴀsʜʙᴏᴀʀᴅ
# ==========================================
@Client.on_message(filters.private & filters.command("stats") & filters.user(ADMINS))
async def all_stats(client, message):
    msg = await message.reply_text("🔄 <b>ғᴇᴛᴄʜɪɴɢ ʙᴜsɪɴᴇss sᴛᴀᴛɪsᴛɪᴄs...</b>")
    
    try:
        now = datetime.now()
        total_users = await db.total_users()
        total_payments = await db.total_payments()
        total_amount = await db.total_amount()
        
        # sᴇᴘᴀʀᴀᴛᴇ ᴄᴏᴜɴᴛs ғᴏʀ ᴍᴏᴠɪᴇ ᴀɴᴅ ɪɴsᴛᴀ ᴠɪᴘs
        active_mov = await db.users.count_documents({"expiry_mov": {"$gt": now}})
        active_inst = await db.users.count_documents({"expiry_inst": {"$gt": now}})

        stats_text = (
            f"📊 <b>sᴜᴘᴇʀ ᴀᴅᴍɪɴ ᴅᴀsʜʙᴏᴀʀᴅ</b> 📊\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
            f"👥 <b>ᴛᴏᴛᴀʟ ᴜsᴇʀs:</b> <code>{total_users}</code>\n"
            f"🎬 <b>ᴍᴏᴠɪᴇ ᴠɪᴘ ᴜsᴇʀs:</b> <code>{active_mov}</code>\n"
            f"📸 <b>ɪɴsᴛᴀ ᴠɪᴘ ᴜsᴇʀs:</b> <code>{active_inst}</code>\n\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
            f"💰 <b>ᴛᴏᴛᴀʟ ᴘᴀʏᴍᴇɴᴛs:</b> <code>{total_payments}</code>\n"
            f"💸 <b>ᴛᴏᴛᴀʟ ʀᴇᴠᴇɴᴜᴇ:</b> <code>₹{total_amount}</code>\n\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
        )
        await msg.edit_text(stats_text)
    except Exception as e:
        await msg.edit_text(f"⚠️ <b>ᴇʀʀᴏʀ:</b> <code>{str(e)}</code>")

# ==========================================
# 👤 ᴜsᴇʀ ᴘʀᴏғɪʟᴇ & ᴘʟᴀɴs
# ==========================================
@Client.on_message(filters.command(["myplan", "profile"]) & filters.private)
async def user_profile_plan(client: Client, message: Message):
    user_id = message.from_user.id
    mention = message.from_user.mention
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz)
    
    msg = await message.reply_text("🔄 <b>ғᴇᴛᴄʜɪɴɢ ʏᴏᴜʀ ᴘʀᴏғɪʟᴇ...</b>")
    
    user_data = await db.get_user(user_id)
    reward_data = await db.rewards.find_one({"user_id": user_id})
    coins = reward_data.get("coins", 0) if reward_data else 0

    def get_status(expiry):
        if not expiry:
            return "❌ <b>ɪɴᴀᴄᴛɪᴠᴇ</b>"
        if expiry.tzinfo is None:
            expiry = pytz.utc.localize(expiry).astimezone(tz)
        else:
            expiry = expiry.astimezone(tz)
            
        if expiry > now:
            return f"✅ <b>ᴀᴄᴛɪᴠᴇ</b>\n╰ ⏰ ᴇɴᴅ: <code>{expiry.strftime('%d-%m-%Y %I:%M %p')}</code>"
        return "❌ <b>ᴇxᴘɪʀᴇᴅ</b>"

    mov_status = get_status(user_data.get("expiry_mov") if user_data else None)
    inst_status = get_status(user_data.get("expiry_inst") if user_data else None)

    profile_text = (
        f"👤 <b>ᴜsᴇʀ ᴘʀᴏғɪʟᴇ & ᴘʟᴀɴs</b> 👤\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🔹 <b>ɴᴀᴍᴇ:</b> {mention}\n"
        f"🔹 <b>ᴜsᴇʀ ɪᴅ:</b> <code>{user_id}</code>\n"
        f"🎁 <b>ʀᴇᴡᴀʀᴅ ᴘᴏɪɴᴛs:</b> <code>{coins}</code>\n\n"
        f"🎬 <b>ᴍᴏᴠɪᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴ:</b>\n{mov_status}\n\n"
        f"📸 <b>ɪɴsᴛᴀ ᴠɪᴘ ᴘʀᴇᴍɪᴜᴍ:</b>\n{inst_status}\n"
        f"━━━━━━━━━━━━━━━━━━━"
    )
    
    await msg.edit_text(
        text=profile_text
    )
    
