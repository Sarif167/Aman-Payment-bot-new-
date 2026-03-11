from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.users_db import db
from info import LOG_CHANNEL, PAYMENT_UN_PIC, SUPPORT

@Client.on_message(filters.photo & filters.private)
async def handle_screenshot(client: Client, message: Message):
    user_id = message.from_user.id
    data = await db.get_payment_state(user_id)
    
    if data:
        amount = data.get("amount", 0)
        premium_duration = data.get("premium_duration", "Uɴᴋɴᴏᴡɴ")
        
        try:
            await client.delete_messages(
                chat_id=message.chat.id, 
                message_ids=[data["photo_id"], data["text_id"]]
            )
        except Exception:
            pass
            
        await db.del_payment_state(user_id)
        
        user_caption = (
            f"🔄 <b>Pᴀʏᴍᴇɴᴛ Uɴᴅᴇʀ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ</b>\n\n"
            f"📄 <b>Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ Dᴇᴛᴀɪʟꜱ:</b>\n"
            f"💰 <b>Pʀɪᴄᴇ:</b> <code>₹{amount}</code>\n"
            f"⏳ <b>Dᴜʀᴀᴛɪᴏɴ:</b> <code>{premium_duration}</code>\n"
            f"📄 <b>Tʏᴘᴇ:</b> <code>Pᴜʀᴄʜᴀꜱᴇ</code>\n\n"
            f"<i>Yᴏᴜʀ ᴘᴀʏᴍᴇɴᴛ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ʙᴇɪɴɢ ʀᴇᴠɪᴇᴡᴇᴅ ʙʏ ᴛʜᴇ ᴀᴅᴍɪɴ. 🧑‍💻 Pʟᴇᴀꜱᴇ ᴡᴀɪᴛ ᴡʜɪʟᴇ ᴡᴇ ᴠᴇʀɪꜰʏ ʏᴏᴜʀ ᴛʀᴀɴꜱᴀᴄᴛɪᴏɴ. "
            f"Wᴇ ᴡɪʟʟ ɴᴏᴛɪꜰʏ ʏᴏᴜ ꜱʜᴏʀᴛʟʏ ᴏɴᴄᴇ ɪᴛ'ꜱ ᴀᴘᴘʀᴏᴠᴇᴅ. ✅</i>\n\n"
            f"Tʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ʏᴏᴜʀ ᴘᴀᴛɪᴇɴᴄᴇ! 💎"
        )

        user_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("ℹ️ Nᴇᴇᴅ Hᴇʟᴘ / Sᴜᴘᴘᴏʀᴛ", url=SUPPORT)]
        ])

        try:
            await message.reply_photo(
                photo=PAYMENT_UN_PIC,
                caption=user_caption,
                reply_markup=user_buttons,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            pass

        admin_caption = (
            f"🆕 <b>Nᴇᴡ Pᴀʏᴍᴇɴᴛ Vᴇʀɪꜰɪᴄᴀᴛɪᴏɴ</b>\n\n"
            f"👤 <b>Uꜱᴇʀ:</b> {message.from_user.mention}\n"
            f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
            f"💳 <b>Aᴍᴏᴜɴᴛ:</b> <code>₹{amount}</code>\n"
            f"⏳ <b>Dᴜʀᴀᴛɪᴏɴ:</b> <code>{premium_duration}</code>\n"
            f"📦 <b>Cᴀᴛᴇɢᴏʀʏ:</b> Pʀᴇᴍɪᴜᴍ Sᴜʙꜱᴄʀɪᴘᴛɪᴏɴ\n\n"
            f"👇 <i>Pʟᴇᴀꜱᴇ ᴠᴇʀɪꜰʏ ᴛʜᴇ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ᴀɴᴅ ᴛᴀᴋᴇ ᴀᴄᴛɪᴏɴ.</i>"
        )
        
        admin_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"✅ Aᴘᴘʀᴏᴠᴇ ₹{amount}", callback_data=f"approve_{user_id}_{amount}")],
            [InlineKeyboardButton("❌ Rᴇᴊᴇᴄᴛ", callback_data=f"reject_{user_id}_{amount}")]
        ])

        try:
            await client.send_photo(
                chat_id=LOG_CHANNEL,
                photo=message.photo.file_id,
                caption=admin_caption,
                reply_markup=admin_buttons,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            pass

@Client.on_message(filters.command("cancel") & filters.private)
async def cancel_payment(client: Client, message: Message):
    user_id = message.from_user.id
    data = await db.get_payment_state(user_id)
    
    if data:
        amount = data.get("amount", 0)
        try:
            await client.delete_messages(
                chat_id=message.chat.id, 
                message_ids=[data["photo_id"], data["text_id"]]
            )
        except Exception:
            pass
            
        await db.del_payment_state(user_id)
        
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🏠 Mᴀɪɴ Mᴇɴᴜ", callback_data="start"),
                InlineKeyboardButton("🔄 Rᴇꜱᴛᴀʀᴛ", callback_data=f"pay_{amount}")
            ]
        ])
        
        await message.reply_text(
            "❌ <b>Pᴀʏᴍᴇɴᴛ Pʀᴏᴄᴇꜱꜱ Cᴀɴᴄᴇʟʟᴇᴅ.</b>\n\n<i>Wʜᴀᴛ ᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ ᴅᴏ ɴᴇxᴛ?</i>",
            reply_markup=buttons,
            parse_mode=enums.ParseMode.HTML
        )
        
