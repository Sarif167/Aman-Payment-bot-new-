import os
import random
import string
import hashlib
import pytz
from datetime import datetime, timedelta
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from info import ADMINS, CHANNEL_LINK, LOG_CHANNEL, TRIAL_PIC
from database.users_db import db
from utils import get_seconds

def hash_code(code):
    return hashlib.sha256(code.encode()).hexdigest()

def generate_pwzone_code():
    code_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return f"PWZONE{code_suffix}"

@Client.on_message(filters.command("code") & filters.user(ADMINS))
async def generate_code_cmd(client: Client, message: Message):
    args = message.command
    if len(args) < 2:
        return await message.reply_text(
            "⚠️ <b>Uꜱᴀɢᴇ:</b> <code>/code [duration] [count]</code>\n\n"
            "<b>Exᴀᴍᴘʟᴇꜱ:</b>\n"
            "👉 <code>/code 1month</code> (Gᴇɴᴇʀᴀᴛᴇꜱ 1 Cᴏᴅᴇ)\n"
            "👉 <code>/code 1week 5</code> (Gᴇɴᴇʀᴀᴛᴇꜱ 5 Cᴏᴅᴇꜱ)"
        )
    
    duration_str = args[1].lower()
    count = int(args[2]) if len(args) == 3 else 1

    if count > 50:
        return await message.reply_text("❌ Mᴀx 50 Cᴏᴅᴇꜱ Aʟʟᴏᴡᴇᴅ Aᴛ Oɴᴄᴇ.")

    premium_duration_seconds = get_seconds(duration_str)
    if not premium_duration_seconds:
        return await message.reply_text("❌ Iɴᴠᴀʟɪᴅ Dᴜʀᴀᴛɪᴏɴ (Uꜱᴇ: 1day, 1week, 1month).")

    msg = await message.reply_text(f"🔄 <b>Gᴇɴᴇʀᴀᴛɪɴɢ {count} Cᴏᴅᴇꜱ...</b>")
    codes = []
    
    for _ in range(count):
        code = generate_pwzone_code()
        await db.codes.insert_one({
            "code_hash": hash_code(code),
            "original_code": code,
            "plan_type": "premium",
            "duration": duration_str,
            "expires_in_sec": premium_duration_seconds,
            "used": False,
            "user_id": None,
            "used_at": None,
            "created_at": datetime.utcnow()
        })
        codes.append(f"🔹 <code>{code}</code>")
        
    codes_text = "\n".join(codes)
    
    await msg.edit_text(
        f"✅ <b>{count} Rᴇᴅᴇᴇᴍ Cᴏᴅᴇꜱ Gᴇɴᴇʀᴀᴛᴇᴅ!</b>\n\n"
        f"📦 <b>Pʟᴀɴ:</b> <code>Pʀᴇᴍɪᴜᴍ Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ</code>\n"
        f"⏳ <b>Dᴜʀᴀᴛɪᴏɴ:</b> <code>{duration_str}</code>\n\n"
        f"{codes_text}\n\n"
        f"👉 <b>Uꜱᴀɢᴇ:</b> <code>/redeem CODE</code>\n"
    )

@Client.on_message(filters.command("allcodes") & filters.user(ADMINS))
async def all_codes_cmd(client: Client, message: Message):
    msg_status = await message.reply_text("🔄 <b>Fᴇᴛᴄʜɪɴɢ Cᴏᴅᴇꜱ...</b>")
    all_codes = await db.codes.find({}).to_list(length=None)
    
    if not all_codes:
        return await msg_status.edit("⚠️ Nᴏ Cᴏᴅᴇꜱ Fᴏᴜɴᴅ Iɴ Dᴀᴛᴀʙᴀꜱᴇ.")
        
    if len(all_codes) > 10:
        file_path = "All_Redeem_Codes.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("📝 GENERATED REDEEM CODES LIST\n")
            f.write("================================\n\n")
            for code in all_codes:
                status = "Yes" if code.get("used") else "No"
                user_text = str(code.get("user_id")) if code.get("user_id") else "Not Redeemed"
                
                f.write(f"🔑 Code: {code.get('original_code')}\n")
                f.write(f"⌛ Duration: {code.get('duration')}\n")
                f.write(f"‼️ Used: {status}\n")
                f.write(f"🙎 User ID: {user_text}\n")
                f.write("--------------------------------\n")
                
        await message.reply_document(document=file_path, caption=f"📝 <b>Tᴏᴛᴀʟ Cᴏᴅᴇꜱ:</b> <code>{len(all_codes)}</code>")
        os.remove(file_path)
        await msg_status.delete()
    else:
        msg = "📝 <b>Gᴇɴᴇʀᴀᴛᴇᴅ Cᴏᴅᴇꜱ Dᴇᴛᴀɪʟꜱ:</b>\n\n"
        for code in all_codes:
            status = "Yᴇꜱ ✅" if code.get("used") else "Nᴏ ⭕"
            user_text = f"<code>{code.get('user_id')}</code>" if code.get("user_id") else "Nᴏᴛ Rᴇᴅᴇᴇᴍᴇᴅ"
            
            msg += (
                f"🔑 <b>Cᴏᴅᴇ:</b> <code>{code.get('original_code')}</code>\n"
                f"⌛ <b>Dᴜʀᴀᴛɪᴏɴ:</b> {code.get('duration')}\n"
                f"‼️ <b>Uꜱᴇᴅ:</b> {status}\n"
                f"🙎 <b>Uꜱᴇʀ:</b> {user_text}\n"
                f"──────────────────\n"
            )
        await msg_status.edit(msg)

@Client.on_message(filters.command("delete_redeem") & filters.user(ADMINS))
async def delete_redeem_cmd(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("❌ Uꜱᴀɢᴇ: <code>/delete_redeem CODE</code>")
    input_code = message.command[1].strip().upper()
    result = await db.codes.delete_one({"code_hash": hash_code(input_code)})
    if result.deleted_count == 1:
        await message.reply_text(f"✅ Cᴏᴅᴇ <code>{input_code}</code> Dᴇʟᴇᴛᴇᴅ Sᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ.")
    else:
        await message.reply_text("❌ Cᴏᴅᴇ Nᴏᴛ Fᴏᴜɴᴅ.")

@Client.on_message(filters.command("clearcodes") & filters.user(ADMINS))
async def clear_codes_cmd(client: Client, message: Message):
    result = await db.codes.delete_many({})
    await message.reply_text(f"✅ Aʟʟ <b>{result.deleted_count}</b> Cᴏᴅᴇꜱ Hᴀᴠᴇ Bᴇᴇɴ Rᴇᴍᴏᴠᴇᴅ.")

async def process_redeem(client, message, code):
    try:
        user_id = message.from_user.id
        user_name = message.from_user.mention

        # 1. Fetch Code Data
        code_data = await db.codes.find_one({"code_hash": hash_code(code)})
        if not code_data:
            return await message.reply_text("🚫 <b>ɪɴᴠᴀʟɪᴅ ᴏʀ ᴇxᴘɪʀᴇᴅ ᴄᴏᴅᴇ.</b>")
        if code_data.get('used'):
            return await message.reply_text("🚫 <b>ᴛʜɪs ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ ʜᴀs ᴀʟʀᴇᴀᴅʏ ʙᴇᴇɴ ᴜsᴇᴅ.</b>")

        duration_str = code_data['duration']
        seconds = code_data['expires_in_sec']

        # 2. Fetch User Data
        user_data = await db.get_user(user_id) or {"id": user_id, "name": message.from_user.first_name}
        current_time = datetime.now()
        tz = pytz.timezone("Asia/Kolkata")
        
        current_expiry = user_data.get("expiry_time")
        if current_expiry and current_expiry.tzinfo:
            current_expiry = current_expiry.replace(tzinfo=None)
            
        # Already Premium Check
        if current_expiry and current_expiry > current_time:
            return await message.reply_text("✨ <b>ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ᴘᴜʀᴄʜᴀsᴇᴅ ᴏᴜʀ sᴜʙsᴄʀɪᴘᴛɪᴏɴ! ᴇɴᴊᴏʏ ʏᴏᴜʀ ʙᴇɴᴇғɪᴛs..</b>")
            
        new_expiry = current_time + timedelta(seconds=seconds)
        user_data["expiry_time"] = new_expiry
        
        # 3. Generate VIP Link & Button
        btn = None
        try:
            invite_link = await client.create_chat_invite_link(
                chat_id=CHANNEL_LINK, 
                member_limit=1, 
                expire_date=current_time + timedelta(minutes=5)
            )
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("✨ ᴊᴏɪɴ ᴠɪᴘ ᴄʜᴀɴɴᴇʟ ✨", url=invite_link.invite_link)]])
        except Exception:
            pass

        # 4. Update Database
        await db.update_user(user_data)
        await db.codes.update_one(
            {"_id": code_data["_id"]},
            {"$set": {"used": True, "user_id": user_id, "user_name": message.from_user.first_name, "used_at": current_time}}
        )

        expiry_str = new_expiry.astimezone(tz).strftime("%d-%m-%Y ᴀᴛ %I:%M:%S %p") 
        
        success_caption = (
            f"🎉 <b>ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs! ᴄᴏᴅᴇ ʀᴇᴅᴇᴇᴍᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ</b>\n\n"
            f"📦 <b>ᴘʟᴀɴ:</b> <code>ᴘʀᴇᴍɪᴜᴍ sᴜʙsᴄʀɪᴘᴛɪᴏɴ</code>\n"
            f"⏳ <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> <code>{duration_str}</code>\n"
            f"📅 <b>ɴᴇᴡ ᴇxᴘɪʀʏ:</b> <code>{expiry_str}</code>\n\n"
            f"👉 <i>ᴛʏᴘᴇ /myplan ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴛᴀᴛᴜs.</i>"
        )

        await message.reply_photo(
            photo=TRIAL_PIC,
            caption=success_caption,
            reply_markup=btn,
            parse_mode=enums.ParseMode.HTML
        )

        # 6. Log to Admin Channel
        log_text = (
            f"🎟️ <b>#ᴄᴏᴅᴇ_ʀᴇᴅᴇᴇᴍᴇᴅ</b>\n\n"
            f"👤 <b>ᴜsᴇʀ:</b> {user_name} [<code>{user_id}</code>]\n"
            f"🔑 <b>ᴄᴏᴅᴇ:</b> <code>{code}</code>\n"
            f"⏳ <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> <code>{duration_str}</code>\n"
            f"🕒 <b>ʀᴇᴅᴇᴇᴍᴇᴅ ᴀᴛ:</b> {current_time.astimezone(tz).strftime('%d-%m-%Y %I:%M %p')}"
        )
        await client.send_message(LOG_CHANNEL, text=log_text)

    except Exception as e:
        await message.reply_text(f"❌ <b>ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ:</b> <code>{str(e)}</code>")
        

@Client.on_message(filters.command("redeem") & filters.private)
async def redeem_command_handler(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("⚠️ <b>Uꜱᴀɢᴇ:</b> <code>/redeem YOUR_CODE</code>")
    code = message.command[1].strip().upper()
    await process_redeem(client, message, code)

@Client.on_message(filters.regex(r"^PWZONE[A-Z0-9]{10}$") & filters.private)
async def redeem_regex_handler(client: Client, message: Message):
    code = message.text.strip().upper()
    await process_redeem(client, message, code)
    
