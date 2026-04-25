from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.users_db import db
from info import LOG_CHANNEL, PAYMENT_UN_PIC, SUPPORT, ADMINS

# ==========================================
# 📩 ᴜɴɪᴠᴇʀsᴀʟ ʟᴏɢɢᴇʀ & sᴄʀᴇᴇɴsʜᴏᴛ ʜᴀɴᴅʟᴇʀ
# ==========================================
@Client.on_message(filters.private & ~filters.user(ADMINS))
async def universal_handler(client: Client, message: Message):
    user_id = message.from_user.id
    user_mention = message.from_user.mention

    # 1. Skip Commands (Starting with /)
    if message.text and message.text.startswith("/"):
        return

    # 2. Check for Payment Screenshot (If it's a Photo)
    if message.photo:
        payment_data = await db.get_payment_state(user_id)
        if payment_data:
            return await process_payment_screenshot(client, message, payment_data)

    # 3. Universal Logging (For everything else: Text, Media, etc.)
    log_header = (
        f"📩 <b>ɴᴇᴡ ᴍᴇssᴀɢᴇ ʀᴇᴄᴇɪᴠᴇᴅ</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>ᴜsᴇʀ:</b> {user_mention}\n"
        f"🆔 <b>ɪᴅ:</b> <code>{user_id}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━"
    )

    try:
        # User ka message log channel mein copy karega user info ke saath
        await message.copy(
            chat_id=LOG_CHANNEL,
            caption=log_header
        )
    except Exception as e:
        print(f"ʟᴏɢ ᴇʀʀᴏʀ: {e}")

# ==========================================
# 📸 ᴘᴀʏᴍᴇɴᴛ sᴄʀᴇᴇɴsʜᴏᴛ ᴘʀᴏᴄᴇssᴏʀ (ɪɴᴛᴇʀɴᴀʟ)
# ==========================================
async def process_payment_screenshot(client, message, data):
    user_id = message.from_user.id
    amount = data.get("amount", 0)
    premium_duration = data.get("premium_duration", "ᴜɴᴋɴᴏᴡɴ")
    pay_type = data.get("pay_type", "ɴ/ᴀ")

    # Purane messages delete karein
    try:
        await client.delete_messages(message.chat.id, [data["photo_id"], data["text_id"]])
    except: pass
        
    await db.del_payment_state(user_id)
    
    # User Notification
    user_caption = (
        f"🔄 <b>ᴘᴀʏᴍᴇɴᴛ ᴜɴᴅᴇʀ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ</b>\n\n"
        f"💰 <b>ᴘʀɪᴄᴇ:</b> <code>₹{amount}</code>\n"
        f"⏳ <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> <code>{premium_duration}</code>\n"
        f"📂 <b>ᴛʏᴘᴇ:</b> <code>{pay_type.upper()}</code>\n\n"
        f"<i>ʏᴏᴜʀ ᴘᴀʏᴍᴇɴᴛ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ʙᴇɪɴɢ ʀᴇᴠɪᴇᴡᴇᴅ ʙʏ ᴀᴅᴍɪɴ. ✅</i>"
    )
    await message.reply_photo(
        photo=PAYMENT_UN_PIC,
        caption=user_caption,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ℹ️ sᴜᴘᴘᴏʀᴛ", url=SUPPORT)]])
    )

    # Admin Log with Buttons
    admin_caption = (
        f"🆕 <b>ɴᴇᴡ ᴘᴀʏᴍᴇɴᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ</b>\n\n"
        f"👤 <b>ᴜsᴇʀ:</b> {message.from_user.mention}\n"
        f"🆔 <b>ɪᴅ:</b> <code>{user_id}</code>\n"
        f"📂 <b>ᴘᴀʏ ᴛʏᴘᴇ:</b> <code>{pay_type.upper()}</code>\n"
        f"💳 <b>ᴀᴍᴏᴜɴᴛ:</b> <code>₹{amount}</code>\n"
        f"⏳ <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> <code>{premium_duration}</code>"
    )
    btns = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ ᴀᴘᴘʀᴏᴠᴇ", callback_data=f"approve_{user_id}_{amount}_{pay_type}")],[
        InlineKeyboardButton("❌ ʀᴇᴊᴇᴄᴛ", callback_data=f"reject_{user_id}_{amount}")
    ]])
    await client.send_photo(chat_id=LOG_CHANNEL, photo=message.photo.file_id, caption=admin_caption, reply_markup=btns)

# ==========================================
# 🛑 ᴄᴀɴᴄᴇʟ ᴘᴀʏᴍᴇɴᴛ ᴄᴏᴍᴍᴀɴᴅ
# ==========================================
@Client.on_message(filters.command("cancel") & filters.private)
async def cancel_payment(client: Client, message: Message):
    user_id = message.from_user.id
    data = await db.get_payment_state(user_id)
    
    if data:
        amount = data.get("amount", 0)
        pay_type = data.get("pay_type", "mov")
        try:
            await client.delete_messages(message.chat.id, [data["photo_id"], data["text_id"]])
        except: pass
            
        await db.del_payment_state(user_id)
        
        btns = InlineKeyboardMarkup([[
            InlineKeyboardButton("🏠 ᴍᴀɪɴ ᴍᴇɴᴜ", callback_data="start"),
            InlineKeyboardButton("🔄 ʀᴇsᴛᴀʀᴛ", callback_data=f"pay_{pay_type}_{amount}")
        ]])
        await message.reply_text("❌ <b>ᴘᴀʏᴍᴇɴᴛ ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ.</b>", reply_markup=btns)
    else:
        await message.reply_text("<b>ɴᴏ ᴀᴄᴛɪᴠᴇ ᴘᴀʏᴍᴇɴᴛ ᴛᴏ ᴄᴀɴᴄᴇʟ.</b>")
        
