import io
import pytz
from datetime import datetime, timedelta
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils import get_seconds
from info import ADMINS, LOG_CHANNEL, CHANNEL_LINK, TRIAL_PIC
from database.users_db import db

# ==========================================
# 👑 ADD PREMIUM (WITH PHOTO & BUTTON)
# ==========================================
@Client.on_message(filters.command("addpremium") & filters.user(ADMINS))
async def manual_add_premium(client: Client, message: Message):
    if len(message.command) != 3:
        return await message.reply_text(
            "⚠️ <b>ᴡʀᴏɴɢ ғᴏʀᴍᴀᴛ!</b>\n\n"
            "<b>ᴜsᴀɢᴇ:</b> <code>/addpremium [user_id] [time]</code>\n"
            "<b>ᴇxᴀᴍᴘʟᴇ:</b> <code>/addpremium 123456789 1month</code>"
        )
    
    try:
        user_id = int(message.command[1])
        time_str = message.command[2]
        seconds = get_seconds(time_str)

        if seconds <= 0:
            return await message.reply_text("❌ <b>ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇ!</b> ᴜsᴇ: <code>1day</code>, <code>1week</code>, <code>1month</code>.")
            
        user_data = await db.get_user(user_id) or {"id": user_id}
        current_expiry = user_data.get("expiry_time")
        
        if current_expiry and current_expiry.tzinfo:
            current_expiry = current_expiry.replace(tzinfo=None)
            
        if current_expiry and current_expiry > datetime.now():
            new_expiry = current_expiry + timedelta(seconds=seconds)
        else:
            new_expiry = datetime.now() + timedelta(seconds=seconds)
            
        user_data["expiry_time"] = new_expiry
        await db.update_user(user_data)
        
        try:
            tg_user = await client.get_users(user_id)
            mention = tg_user.mention
        except Exception:
            mention = f"ᴜsᴇʀ {user_id}"
            
        tz = pytz.timezone("Asia/Kolkata")
        expiry_str = new_expiry.astimezone(tz).strftime("%d-%m-%Y ᴀᴛ %I:%M:%S %p")
        
        btn = None
        try:
            invite_link = await client.create_chat_invite_link(
                chat_id=CHANNEL_LINK,
                member_limit=1,
                expire_date=datetime.now() + timedelta(minutes=5)
            )
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("✨ ᴊᴏɪɴ ᴠɪᴘ ᴄʜᴀɴɴᴇʟ ✨", url=invite_link.invite_link)]])
        except Exception:
            pass

        # Admin Message
        await message.reply_text(
            f"✅ <b>ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ</b>\n\n"
            f"👤 <b>ᴜsᴇʀ:</b> {mention}\n"
            f"🆔 <b>ɪᴅ:</b> <code>{user_id}</code>\n"
            f"⌛ <b>ᴇxᴘɪʀʏ:</b> <code>{expiry_str}</code>"
        )
        
        # User Message with Photo
        try:
            await client.send_photo(
                chat_id=user_id,
                photo=TRIAL_PIC,
                caption=(
                    f"👋 <b>ʜᴇʏ {mention},</b>\n\n"
                    f"🎉 <b>ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ʜᴀs ʙᴇᴇɴ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ʙʏ ᴀᴅᴍɪɴ!</b> ✨\n\n"
                    f"⏳ <b>ᴀᴄᴄᴇss ᴛɪᴍᴇ:</b> <code>{time_str}</code>\n"
                    f"⌛ <b>ɴᴇᴡ ᴇxᴘɪʀʏ:</b> <code>{expiry_str}</code>\n\n"
                    f"⚠️ <b>ʟɪɴᴋ ᴇxᴘɪʀᴇs ɪɴ 5 ᴍɪɴᴜᴛᴇs!</b>"
                ),
                reply_markup=btn,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            await message.reply_text("⚠️ <i>ɴᴏᴛᴇ: ᴄᴏᴜʟᴅ ɴᴏᴛ ᴅᴍ ᴜsᴇʀ.</i>")

        await client.send_message(
            chat_id=LOG_CHANNEL, 
            text=f"🆕 <b>#ᴘʀᴇᴍɪᴜᴍ_ᴀᴅᴅᴇᴅ</b>\n\n👤 {mention}\n⏳ ᴛɪᴍᴇ: <code>{time_str}</code>\n👮 ʙʏ: {message.from_user.mention}"
        )
            
    except Exception as e:
        await message.reply_text(f"❌ <b>ᴇʀʀᴏʀ:</b> <code>{e}</code>")

# ==========================================
# 🗑️ REMOVE PREMIUM
# ==========================================
@Client.on_message(filters.command("removepremium") & filters.user(ADMINS))
async def manual_remove_premium(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("⚠️ <b>ᴜsᴀɢᴇ:</b> <code>/removepremium [user_id]</code>")
    
    try:
        user_id = int(message.command[1])
        user_data = await db.get_user(user_id)
        if user_data:
            user_data["expiry_time"] = None
            await db.update_user(user_data)
        else:
            return await message.reply_text("❌ <b>ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ!</b>")

        try:
            await client.ban_chat_member(chat_id=CHANNEL_LINK, user_id=user_id)
            await client.unban_chat_member(chat_id=CHANNEL_LINK, user_id=user_id)
        except: pass

        await message.reply_text(f"✅ <b>ᴘʀᴇᴍɪᴜᴍ ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.</b>")
        try:
            await client.send_message(user_id, "⚠️ <b>ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ.</b>")
        except: pass

    except Exception as e:
        await message.reply_text(f"❌ <b>ᴇʀʀᴏʀ:</b> <code>{e}</code>")

# ==========================================
# 👑 PREMIUM USER LIST
# ==========================================
@Client.on_message(filters.command("premium_user") & filters.user(ADMINS))
async def premium_users_list(client: Client, message: Message):
    msg = await message.reply_text("🔄 <b>ғᴇᴛᴄʜɪɴɢ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs...</b>")
    current_time = datetime.now()
    premium_users = []
    
    users = await db.get_all_users()
    async for user in users:
        expiry = user.get("expiry_time")
        if expiry and expiry.replace(tzinfo=None) > current_time:
            premium_users.append({"id": user["id"], "name": user.get("name", "ᴜɴᴋɴᴏᴡɴ")})

    if not premium_users:
        return await msg.edit_text("❌ <b>ɴᴏ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs.</b>")

    if len(premium_users) <= 10:
        text = f"👑 <b>ᴛᴏᴛᴀʟ ᴘʀᴇᴍɪᴜᴍ: {len(premium_users)}</b>\n\n"
        for u in premium_users:
            text += f"👤 <b>ɴᴀᴍᴇ:</b> {u['name']}\n🆔 <b>ɪᴅ:</b> <code>{u['id']}</code>\n➖➖➖➖➖➖\n"
        await msg.edit_text(text)
    else:
        file_content = f"ᴛᴏᴛᴀʟ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs: {len(premium_users)}\n"
        for i, u in enumerate(premium_users, 1):
            file_content += f"{i}. {u['name']} [{u['id']}]\n"
            
        with io.BytesIO(str.encode(file_content)) as out_file:
            out_file.name = "Premium_Users.txt"
            await message.reply_document(document=out_file, caption=f"👑 <b>ᴛᴏᴛᴀʟ ᴘʀᴇᴍɪᴜᴍ:</b> <code>{len(premium_users)}</code>")
            await msg.delete()
        
